import pandas as pd

def cleanBGData(filepath):

  df = pd.DataFrame(pd.read_csv(filepath))

  # Show only active staff
  df = df[df['User Status'] == 'Active']

  # Pivit table for better orginization of data
  df = df.pivot(index='Staff Name', columns='Background Check Type', values='Expiration Date')

  for col in df:
    df[col] = pd.to_datetime(df[col], errors='coerce')
    df[col] = df[col].dt.strftime('%m/%d/%Y').fillna('Missing')


  htmlTbl = df.to_html()
  htmlTbl = htmlTbl.replace('>Missing<', ' class="missing">Missing<')

  return htmlTbl