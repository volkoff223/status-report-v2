import pandas as pd
from datetime import datetime

def cleanEnrolData(filepath):
    df = pd.DataFrame(pd.read_csv(filepath))

    # Show only "Active" users
    df = df[df['Child Status'] == 'Active']

    # Convert 'Medical Evaluation Expiration' to datetime format
    df['Medical Evaluation Expiration'] = pd.to_datetime(df['Medical Evaluation Expiration'], errors='coerce')

    # Get today's date
    today = datetime.today()

    # Filter for rows where 'Medical Evaluation Expiration' is before today OR 'Child Notes' is not empty
    df = df[(df['Medical Evaluation Expiration'] < today) | (df['Child Notes'].notna())]

    # Replace NaN values in 'Child Notes' with 'None'
    df['Child Notes'] = df['Child Notes'].fillna('None')

    # Show only the necessary columns
    df = df[['Child Full Name', 'Medical Evaluation Expiration', 'Child Notes']]

    # Sort rows alphabetically by 'Child Full Name'
    df = df.sort_values(by='Child Full Name')

    # Convert to HTML table format
    htmlTbl = df.to_html(index=False)
    
    return htmlTbl
