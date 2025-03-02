import pandas as pd


def cleanBalanceData(filepath):
    # Read the CSV file
    df = pd.read_csv(filepath)
    
    # Show only these columns
    df = df[['Child Name', 'Bill to Name', 'Current Balance']]
    
    # Remove duplicate "Staff Name" rows (keeping the first occurrence)
    df = df.drop_duplicates(subset=['Child Name'], keep='first').fillna('')

    # Remove rows where Child Name is an empty string
    df = df[df['Child Name'] != '']

    # Display only negitive balances
    df = df[df['Current Balance'] < 0]

    # Convert to HTML table
    htmlTbl = df.to_html(index=False)
    return htmlTbl