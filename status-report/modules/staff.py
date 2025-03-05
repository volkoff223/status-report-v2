import pandas as pd
from pandas import DataFrame
from pandas.tseries.offsets import DateOffset

def cleanStaffData(filepath):
    # Read the CSV file
    df = pd.read_csv(filepath)
    
    # Show only "Active" users
    df = df[df['User Status'] == 'Active']

    # Remove the row where 'Staff Name' is 'Staff, HRSSA'
    df = df[df['Staff Name'] != 'Staff, HRSSA']
    
    # Extract relevant columns
    df = df[['Staff Name', 'Medical Evaluation Expiration', 'TB Test Completion',
             'Course Name', 'Training Expiration Date']]
    
    # Pivot the data to create separate columns for each training type
    training_types = ['Child Abuse & Neglect', 'CPR', 'Pre Service Training', 'Pre Service 3 Hour Update']
    
    # Create an empty dataframe to store training dates
    training_df = pd.DataFrame()
    
    for training in training_types:
        temp_df = df[df['Course Name'].str.contains(training, na=False, case=False)]
        temp_df = temp_df[['Staff Name', 'Training Expiration Date']].rename(columns={'Training Expiration Date': training})
        training_df = pd.merge(training_df, temp_df, on='Staff Name', how='outer') if not training_df.empty else temp_df
    
    # Merge back with the main dataframe
    df = df.drop(columns=['Course Name', 'Training Expiration Date']).drop_duplicates()
    df = pd.merge(df, training_df, on='Staff Name', how='left')
    
    # Ensure 'Pre Service Training' correctly displays 'Completed' if it has a value
    df['Pre Service Training'] = df['Pre Service Training'].apply(lambda x: 'Completed' if pd.notna(x) and str(x).strip() != '' else 'Missing')
    
    # Rename 'TB Test Completion' to 'TB Test Expiration' and add 2 years to each date
    df = df.rename(columns={'TB Test Completion': 'TB Test Expiration'})
    df['TB Test Expiration'] = pd.to_datetime(df['TB Test Expiration'], errors='coerce')
    df['TB Test Expiration'] = df['TB Test Expiration'] + DateOffset(years=2)
    
    # Format all date columns in short US date style (MM/DD/YYYY) and ensure only date is displayed
    date_columns = ['TB Test Expiration', 'Child Abuse & Neglect', 'CPR', 'Pre Service 3 Hour Update']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce').dt.date  # Convert to date only
        df[col] = df[col].apply(lambda x: x.strftime('%m/%d/%Y') if pd.notna(x) else "Missing")
    
    # Replace empty strings or NaN with "Missing" for all columns except 'Staff Name'
    df.loc[:, df.columns != 'Staff Name'] = df.loc[:, df.columns != 'Staff Name'].replace(['', 'NaN', None, pd.NA], 'Missing')
    
    # Sort rows alphabetically by 'Staff Name'
    df = df.sort_values(by='Staff Name')

    # Convert to HTML table
    htmlTbl = df.to_html(index=False)
    htmlTbl = htmlTbl.replace('>Missing<', ' class="missing">Missing<')
    return htmlTbl
