import pandas as pd

def merge_rows(df):
    """
    This function merges rows where the 'Number', 'Time Start', and 'Time End' columns match,
    and concatenates the 'Action' values. After merging, it removes the duplicate rows.
    """
    # List to store indices of rows that have been merged
    processed_rows = []

    # Iterate over each row in the DataFrame
    for i in range(len(df)):
        current_row = df.iloc[i]
        
        # Skip this row if it has already been merged
        if i in processed_rows:
            continue
        
        # Compare with subsequent rows
        for j in range(i+1, len(df)):
            compare_row = df.iloc[j]
            
            # Check if the 'Number', 'Time Start', and 'Time End' columns match
            if (current_row['Number'] == compare_row['Number']) and \
               (current_row['Time Start'] == compare_row['Time Start']) and \
               (current_row['Time End'] == compare_row['Time End']):
                
                # Merge the 'Action' values by concatenating them with a space
                df.at[i, 'Action'] = f"{current_row['Action']} {compare_row['Action']}"
                
                # Mark the subsequent row for deletion (after merging)
                processed_rows.append(j)
                
    # Drop the rows that were merged
    df_cleaned = df.drop(index=processed_rows)
    return df_cleaned

def process_excel_file(input_file, output_file):
    """
    Processes all sheets in an Excel file, applies the merge_rows function to each,
    and saves the results in separate sheets in a new Excel file.
    """
    # Load all sheets from the input Excel file
    sheets = pd.read_excel(input_file, sheet_name=None)

    # Create a writer object for the output Excel file
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        # Process each sheet
        for sheet_name, sheet_df in sheets.items():
            # Apply the merge function to each sheet
            merged_df = merge_rows(sheet_df)
            # Write the merged DataFrame to the output Excel file, with the same sheet name
            merged_df.to_excel(writer, sheet_name=sheet_name, index=False)

# Example usage:
input_file = 'timelineResults.xlsx'  # Replace with your input file path
output_file = 'merged_timeline_results.xlsx'  # Replace with your desired output file path
process_excel_file(input_file, output_file)

print(f"File saved to {output_file}")
