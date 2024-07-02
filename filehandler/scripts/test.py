# test.py
import pandas as pd
import io

def process_file(file):
    # Read the uploaded file into a dictionary of DataFrames
    xls = pd.ExcelFile(file)
    sheet_to_df_map = {}
    
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(file, sheet_name=sheet_name)
        df = df.fillna('')  # Replace NaN values with empty strings
        sheet_to_df_map[sheet_name] = df
    
    # Write the DataFrames to a new Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, df in sheet_to_df_map.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    output.seek(0)
    
    # Prepare the data for the template
    processed_data = {
        sheet_name: {
            'columns': df.columns.tolist(),
            'rows': df.values.tolist()
        }
        for sheet_name, df in sheet_to_df_map.items()
    }
    
    return processed_data, output, 'processed_file.xlsx'
