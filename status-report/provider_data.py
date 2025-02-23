import numpy as np
import pandas as pd
from pandas import DataFrame

def cleanProviderData(filepath):


  df = pd.DataFrame(pd.read_csv(filepath))

  # Show only these columns
  df = df[['Inspection Type', 'Date Inspection Expires']]

  htmlTbl = df.to_html(index=False)
  return htmlTbl