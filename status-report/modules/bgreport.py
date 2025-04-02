import pandas as pd

def cleanBGData(filepath):

  df = pd.DataFrame(pd.read_csv(filepath))

  # Show only active staff
  df = df[df['User Status'] == 'Active']

  # Pivit table for better orginization of data
  df = df.pivot(index='Staff Name', columns='Background Check Type', values='Expiration Date')

  print(df.columns.tolist())


  # Show only these columns
  df = df[['5-yr Child Abuse & Neglect', '5-yr FBI Background Check', '5-yr State Background Check']]

  for col in df:
    df[col] = pd.to_datetime(df[col], errors='coerce')
    df[col] = df[col].dt.strftime('%m/%d/%Y').fillna('Missing')


  htmlTbl = df.to_html()
  htmlTbl = htmlTbl.replace('>Missing<', ' class="missing">Missing<')

  return htmlTbl