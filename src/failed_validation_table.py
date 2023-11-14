import os
from datetime import datetime
import pandas as pd
import inquirer


# select a table from the organ list provided
questions = [
	inquirer.List('organ',
                message="Which table should be selected?",
                choices=['Anatomical_Systems', 'Fallopian_tube', 'Lung', 'Muscular_System', 'Placenta', 'Spleen', 'Blood', 'Heart', 'Lymph_node', 'Ovary', 'Prostate', 'Thymus', 'Blood_vasculature', 'Kidney', 'Lymph_vasculature', 'Palatine_Tonsil', 'Skeleton', 'Trachea', 'Bone-Marrow', 'Knee', 'Main_Bronchus', 'Pancreas', 'Skin', 'Ureter', 'Brain', 'Large_intestine', '', 'Peripheral_nervous_system', 'Small_intestine', 'Urinary_bladder', 'Eye', 'Liver', 'Mammary_Gland', '', 'Spinal_Cord', 'Uterus'],
            ),
]
answers = inquirer.prompt(questions)
print (answers["organ"])

organ_table = answers["organ"]

# Split the table from the repository into three tables (AS-AS, CT-CT, AS-CT)
def split_report(report):
	report_as = report[report['s'].str.contains('UBERON') & report['o'].str.contains('UBERON')]
	report_ct = report[report['s'].str.contains('CL') & report['o'].str.contains('CL')]
	report_ct_as = report[report['s'].str.contains('CL') & report['o'].str.contains('UBERON')]

	return report_as, report_ct, report_ct_as

# Generate three tables
def generate_relationship_tables(organ_table):
	BASE_PATH = f"../ccf-validation-tools/docs/{organ_table}/"
	table = pd.read_csv(f"{BASE_PATH}class_{organ_table}_log.tsv", sep='\t')
	simplified_table = table[["olabel", "o", "slabel", "s"]].drop_duplicates() # We are only interested in the ID and labels. We don't need duplicates.
	report_as, report_ct, report_ct_as = split_report(simplified_table)
    # List of DataFrames
	dataframes = [report_as, report_ct, report_ct_as]

    # Apply the method to each DataFrame
    # Use enumerate to get both index and DataFrame in the loop
	for idx, df in enumerate(dataframes):
		# Some reports might be empty, we don't need to do anything on them.
		if not df.empty:
			# Reset the index and update the DataFrame in the list
			dataframes[idx] = df.reset_index(drop=True)
            # Add the reporting column
			dataframes[idx]['reporting'] = dataframes[idx].apply(lambda row: f"**{row.name + 1} - {row['olabel']} &rarr; {row['slabel']}**", axis=1)

	report_as, report_ct, report_ct_as = dataframes
    
	return report_as, report_ct, report_ct_as

table_as, table_ct, table_ct_as = generate_relationship_tables(organ_table)

# Check if the folder exists for tables and reports
if not os.path.exists(f"docs/Tables.gitignore/{organ_table}"):
    # If it doesn't exist, create the folder
    os.makedirs(f"docs/Tables.gitignore/{organ_table}")
    os.makedirs(f"docs/Reports/{organ_table}")
    print(f"The folder '{organ_table}' has been created.")
else:
    print(f"The folder '{organ_table}' already exists.")

# It would be good to load last version to compare tables and if tables are the same, not write a new document.

date = datetime.today().strftime('%Y-%m-%d')

# Create a Pandas Excel writer using XlsxWriter as the engine
excel_file_path = f"docs/Tables.gitignore/{organ_table}/{organ_table}_{date}.xlsx"

# Create a Pandas Excel writer using XlsxWriter as the engine
with pd.ExcelWriter(excel_file_path) as writer:
# Write each dataframe to a different worksheet
    table_as.to_excel(writer, sheet_name=f"Table_AS_{date}", index=False)
    table_ct.to_excel(writer, sheet_name=f"Table_CT_{date}", index=False)
    table_ct_as.to_excel(writer, sheet_name=f"Table_AS-CT_{date}", index=False)

