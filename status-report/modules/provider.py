import pandas as pd
from pandas import DataFrame

def cleanProviderData(filepath):

  df = DataFrame
  df = pd.DataFrame(pd.read_csv(filepath))

  # Show only these columns
  df = df[['Inspection Type', 'Date Inspection Expires']]

  # Convert all dates to proper format
  df['Date Inspection Expires'] = pd.to_datetime(df['Date Inspection Expires'])

  htmlTbl = df.to_html(index=False)
  return htmlTbl