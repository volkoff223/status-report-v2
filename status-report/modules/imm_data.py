import pandas as pd
from pandas import DataFrame

def cleanImmData(filepath):

  df = DataFrame
  df = pd.DataFrame(pd.read_csv(filepath))


  # Show only "Active" users
  df = df[df['Child Status'] == 'Active']

  # Show only these columns
  df = df[['Child Full Name', 'Alert']]

  # Show students with an alert
  df = df[df['Alert'] == 'Overdue']

  # Remove duplicate "Staff Name" rows (keeping the first occurrence)
  df = df.drop_duplicates(subset=['Child Full Name'], keep='first')

  htmlTbl = df.to_html(index=False)
  return htmlTbl