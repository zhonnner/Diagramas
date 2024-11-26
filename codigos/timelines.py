import pandas as pd

def process_sheet(sheet_df):
    """Process a single sheet, filtering and extracting pairs with corresponding actions."""
    # Filter rows where '3lineas' column is not "N/A", "none", or 0
    filtered_df = sheet_df[
        (sheet_df['3lineas'] != 'N/A') & 
        (sheet_df['3lineas'] != 'none') & 
        (sheet_df['3lineas'] != 0) & 
        (~sheet_df['3lineas'].isnull())
    ]

    # Initialize a list to store processed rows
    processed_rows = []

    # Iterate over the filtered dataframe
    for index, row in filtered_df.iterrows():
        pairs = str(row['3lineas']).split()  # Split pairs by spaces
        actions = str(row['action']).split()  # Split actions by spaces
        time_start = row['time_start']
        time_end = row['time_end']
        
        # Iterate through pairs and actions and map them
        for i, pair in enumerate(pairs):
            numbers = pair.split(',')  # Split the pair into individual numbers
            for number in numbers:
                # Append a new row with number, time_start, time_end, and corresponding action
                processed_rows.append([number, time_start, time_end, actions[i] if i < len(actions) else ""])

    # Create a DataFrame from the processed rows
    processed_df = pd.DataFrame(processed_rows, columns=['Number', 'Time Start', 'Time End', 'Action'])
    return processed_df

def process_excel_file(input_file, output_file):
    """Process each sheet of an Excel file and save the results in separate sheets in a new Excel file."""
    # Load all sheets from the input Excel file
    sheets = pd.read_excel(input_file, sheet_name=None)

    # Create a writer object for the output Excel file
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        # Process each sheet
        for sheet_name, sheet_df in sheets.items():
            # Process the sheet
            processed_df = process_sheet(sheet_df)
            # Write the processed DataFrame to the output Excel file, with a sheet for each original sheet
            processed_df.to_excel(writer, sheet_name=sheet_name, index=False)

# Example usage:
input_file = 'dataframes5.xlsx'  # Replace with the path to your input file
output_file = 'timelineResults.xlsx'  # Replace with the desired output file path
process_excel_file(input_file, output_file)
