import pandas as pd

def cleanProviderData(filepath):
    # Read the CSV into a DataFrame
    df = pd.read_csv(filepath)

    # Show only these columns
    df = df[['Inspection Type', 'Date Inspection Expires']]

    # Convert 'Date Inspection Expires' to proper datetime format and format as MM/DD/YYYY
    df['Date Inspection Expires'] = pd.to_datetime(df['Date Inspection Expires'], errors='coerce').dt.strftime('%m/%d/%Y')

    # Convert DataFrame to HTML table
    htmlTbl = df.to_html(index=False)
    return htmlTbl
