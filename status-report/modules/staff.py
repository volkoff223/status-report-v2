import pandas as pd
from pandas import DataFrame
from pandas.tseries.offsets import DateOffset

def cleanStaffData(filepath):
    # Read the CSV file
    df = pd.read_csv(filepath)
    
    # Show only "Active" users
    df = df[df['User Status'] == 'Active']
    
    # Show only these columns
    df = df[['Staff Name', 'Medical Evaluation Expiration', 'TB Test Completion']]
    
    # Remove duplicate "Staff Name" rows (keeping the first occurrence)
    df = df.drop_duplicates(subset=['Staff Name'], keep='first')

    
    # Format dates for display and replace NaN with "Missing"
    date_columns = df.columns.drop('Staff Name')
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        df[col] = df[col].dt.strftime('%m-%d-%Y').fillna("Missing")
    
    # Convert to HTML table
    htmlTbl = df.to_html(index=False)
    htmlTbl = htmlTbl.replace('>Missing<', ' class="missing">Missing<')
    return htmlTbl