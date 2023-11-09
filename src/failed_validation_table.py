from datetime import datetime
import pandas as pd




def split_report(report):
  report_as = report[report['s'].str.contains('UBERON') & report['o'].str.contains('UBERON')]
  report_ct = report[report['s'].str.contains('CL') & report['o'].str.contains('CL')]
  report_ct_as = report[report['s'].str.contains('CL') & report['o'].str.contains('UBERON')]

  return report_as, report_ct, report_ct_as