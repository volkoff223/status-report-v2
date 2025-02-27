import numpy as np
import pandas as pd
from pandas import DataFrame

def cleanStaffData(filepath):


  df = pd.DataFrame(pd.read_csv(filepath))

  # Show only "Active" users
  df = df[df['User Status'] == 'Active']

  # Show only these columns
  df = df[['Staff Name', 'Medical Evaluation Expiration', 'TB Test Completion', 'State Background Check Complete', 'FBI Check Complete', 'Child Abuse/Neglect Records Check Comp', ]]

  # Remove duplicate "User Name" rows (keeping the first occurrence)
  df = df.drop_duplicates(subset=['Staff Name'], keep='first')
  htmlTbl = df.to_html(index=False)
  return htmlTbl
