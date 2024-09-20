import pandas as pd
from statistics import mode

# Function to process the log file and generate the Excel file
def process_log_to_df(log_file_path) -> pd.DataFrame:
    # Read the log file
    with open(log_file_path, 'r') as file:
        log_content = file.readlines()

    # Define the column headers based on the Excel file
    columns = [
        'Testing Mode', 'Gin Code', 'Gin Bale Number', 'Mic', 'Rd', 'b+', 
        'Color Grade', 'Area', 'Cnt', 'T.L', 'Len', 'Unf', 
        'Str', 'SFI', 'ELG', 'Retest', 'Retest Code', 'Line Number'
    ]

    # Prepare a list to store the processed rows
    processed_data = []

    # Parse the log file's lines
    for line in log_content:
        # Split the line by '@' to get individual fields
        values = line.strip().split('@')

        # Ensure that there are enough values in the line to avoid index errors
        if len(values) >= 21:
            # Apply your original transformations for each field
            row = [
                values[0],  # Testing Mode
                values[1],  # Gin Code
                values[2],  # Gin Bale Number
                f"{int(values[4])/100:.2f}",  # Mic (e.g., 448 -> 4.48)
                f"{int(values[5])/10:.1f}",   # Rd (e.g., 753 -> 75.3)
                f"{int(values[6])/10:.1f}",   # b+ (e.g., 130 -> 13.0)
                f"{values[7][0]}{values[7][1]}-{values[7][2]}",  # Color Grade (e.g., 133 -> 13-3)
                f"{int(values[8])/100:.1f}",  # Area (e.g., 030 -> 0.3)
                int(values[9]),  # Count (e.g., 020 -> 20)
                int(values[10]), # Leaf
                f"{int(values[11])/1000:.3f}",  # Length (e.g., 0972 -> 0.972)
                f"{int(values[12])/10:.1f}",    # Uniformity (e.g., 767 -> 76.7)
                f"{int(values[13])/10:.1f}",    # Strength (e.g., 236 -> 23.6)
                f"{int(values[15])/10:.1f}",    # SFI (e.g., 070 -> 7.0)
                f"{int(values[16])/10:.1f}",    # Elongation (e.g., 070 -> 7.0)
                values[17],  # Retest (N)
                values[18],  # Retest Code (N)
                int(values[21]),  # Line Number (e.g., 000021 -> 21)
            ]
            processed_data.append(row)

    # Convert the processed data into a DataFrame
    log_df = pd.DataFrame(processed_data, columns=columns)

    # Convert numeric columns for mean calculation
    numeric_columns = ['Mic', 'Rd', 'b+', 'Area', 'Cnt', 'T.L', 'Len', 'Unf', 'Str', 'SFI', 'ELG']
    log_df[numeric_columns] = log_df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Group by 'Gin Bale Number' and calculate the mean of other numeric columns
    grouped_df = log_df.groupby('Gin Bale Number').agg({
        'Testing Mode': 'first',
        'Gin Code': 'first',
        'Mic': 'mean',
        'Rd': 'mean',
        'b+': 'mean',
        'Color Grade': lambda x: mode(x),  # Take the mode for Color Grade
        'Area': 'mean',
        'Cnt': 'mean',
        'T.L': 'mean',
        'Len': 'mean',
        'Unf': 'mean',
        'Str': 'mean',
        'SFI': 'mean',
        'ELG': 'mean',
        'Retest': 'first',       # Keep the first Retest
        'Retest Code': 'first',  # Keep the first Retest Code
        'Line Number': 'first'   # Keep the first Line Number
    }).reset_index()
    # Calculate the SCI column using the provided formula
    grouped_df['SCI'] = (-414.67 +
                     2.9 * grouped_df['Str'] -
                     9.32 * grouped_df['Mic'] +
                     49.17 * grouped_df['Len'] +
                     4.74 * grouped_df['Unf'] +
                     0.65 * grouped_df['Rd'] +
                     0.36 * grouped_df['b+'])

    # Insert the new column 'SCI' before 'Mic'
    mic_index = grouped_df.columns.get_loc('Mic')
    grouped_df.insert(mic_index, 'SCI', grouped_df.pop('SCI'))
    # Round values after grouping
    grouped_df['SCI']= grouped_df['SCI'].round(0).astype(int)
    grouped_df['Mic'] = grouped_df['Mic'].round(2)
    grouped_df['Rd'] = grouped_df['Rd'].round(1)
    grouped_df['b+'] = grouped_df['b+'].round(1)
    grouped_df['Area'] = grouped_df['Area'].round(2)
    grouped_df['Cnt'] = grouped_df['Cnt'].round(0).astype(int)
    grouped_df['T.L'] = grouped_df['T.L'].round(0).astype(int)
    grouped_df['Len'] = grouped_df['Len'].round(2)
    grouped_df['Unf'] = grouped_df['Unf'].round(1)
    grouped_df['Str'] = grouped_df['Str'].round(1)
    grouped_df['SFI'] = grouped_df['SFI'].round(1)
    grouped_df['ELG'] = grouped_df['ELG'].round(1)

    return grouped_df
