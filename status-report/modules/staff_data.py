import pandas as pd
from pandas import DataFrame
from pandas.tseries.offsets import DateOffset

def cleanStaffData(filepath):
    # Read the CSV file
    df = pd.read_csv(filepath).fillna("Missing")
    
    # Show only "Active" users
    df = df[df['User Status'] == 'Active']
    
    # Show only these columns
    df = df[['Staff Name', 'Medical Evaluation Expiration', 'TB Test Completion', 
             'State Background Check Complete', 'FBI Check Complete', 
             'Child Abuse/Neglect Records Check Comp']]
    
    # Remove duplicate "Staff Name" rows (keeping the first occurrence)
    df = df.drop_duplicates(subset=['Staff Name'], keep='first')


    
    # Rename the TB Test Completion column to TB Test Expires
    df = df.rename(columns={'TB Test Completion': 'TB Test Expires'})
    df = df.rename(columns={'State Background Check Complete': 'State Background Check Expires'})
    df = df.rename(columns={'FBI Check Complete': 'FBI Check Expires'})
    df = df.rename(columns={'Child Abuse/Neglect Records Check Comp': 'Child Abuse Records Check Expires'})

    # Convert date columns to datetime and add 2 years
    add_two_years = ['TB Test Expires', 'State Background Check Expires', 'FBI Check Expires', 'Child Abuse Records Check Expires']
    for col in add_two_years:
        df[col] = pd.to_datetime(df[col], errors='coerce') + DateOffset(years=2)
    
    # Format dates for display (optional)
    for col in add_two_years:
        df[col] = df[col].dt.strftime('%m-%d-%Y').fillna("Missing")
    
    # Convert to HTML table
    htmlTbl = df.to_html(index=False)
    return htmlTbl