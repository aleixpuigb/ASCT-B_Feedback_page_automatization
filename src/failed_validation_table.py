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

table = answers["organ"]

# Split the table from the repository into three tables (AS-AS, CT-CT, AS-CT)
def split_report(report):
  report_as = report[report['s'].str.contains('UBERON') & report['o'].str.contains('UBERON')]
  report_ct = report[report['s'].str.contains('CL') & report['o'].str.contains('CL')]
  report_ct_as = report[report['s'].str.contains('CL') & report['o'].str.contains('UBERON')]

  return report_as, report_ct, report_ct_as

