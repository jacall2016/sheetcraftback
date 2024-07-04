import os
import pandas as pd
import numpy as np
import io
import re

def generate_well_numbers():
    rows = list('ABCDEFGHIJKLMNOP')
    columns = list(range(1, 25))
    return [f"{row}{col}" for row in rows for col in columns]

def extract_file_info(file):
    if not hasattr(file, 'name'):
        file.name = 'uploaded_flip700_file.xlsx'
    base_name = file.name  # Use the file name directly from the file object
    base_name = base_name.split(' ', 1)[-1]
    plate_name = base_name.split('_')[0]
    library = plate_name[:3]
    library_copy_number = base_name.split('_')[1][:4]
    return plate_name, library, library_copy_number

def process_excel_file(file):
    plate_name, library, library_copy_number = extract_file_info(file)
    df = pd.read_excel(file, sheet_name='Analysis')
    df['Library'] = library
    df['Library_Copy_number'] = library_copy_number
    df['Plate_Name'] = plate_name
    df['Molecule_Name'] = ""
    df['SMILES'] = ""
    df['Compound_number'] = ""
    df['High_Controls_z_score'] = np.nan
    df.rename(columns={'well_number': 'Plate_Well'}, inplace=True)
    df['Plate_Well'] = df['Plate_Well'].apply(lambda x: x.split('.')[0])
    df.loc[df['Plate_Well'].str.contains(r'23$|24$|^(?:A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P)(1|2)$'), 'High_Controls_z_score'] = df['flip700_z_score']
    df = df[[
        'Library', 'Library_Copy_number', 'Plate_Name', 'Plate_Well', 'Molecule_Name', 'SMILES', 
        'Compound_number', 'flip700_z_score', 'hits_flip700_z_score', 'High_Controls_z_score'
    ]]
    df.rename(columns={
        'flip700_z_score': 'All_Compounds_Flip700_z_score',
        'hits_flip700_z_score': 'Hits_Flip700_z_score'
    }, inplace=True)
    return df

def sort_compiled_data(df):
    def extract_row_column(well):
        match = re.match(r'([A-Z])(\d+)', well)
        if match:
            return match.group(1), int(match.group(2))
        return well, 0
    df['Row'], df['Column'] = zip(*df['Plate_Well'].map(extract_row_column))
    row_order = {row: idx for idx, row in enumerate('ABCDEFGHIJKLMNOP')}
    df['Row_Order'] = df['Row'].map(row_order)
    df_sorted = df.sort_values(by=['Plate_Name', 'Row_Order', 'Column']).reset_index(drop=True)
    df_sorted.drop(columns=['Row', 'Column', 'Row_Order'], inplace=True)
    return df_sorted

def add_missing_wells(df):
    compiled_data = []
    expected_wells = generate_well_numbers()
    for plate_name, group in df.groupby('Plate_Name'):
        current_wells = set(group['Plate_Well'])
        missing_wells = set(expected_wells) - current_wells
        for missing_well in missing_wells:
            new_row = {
                'Library': group['Library'].iloc[0],
                'Library_Copy_number': group['Library_Copy_number'].iloc[0],
                'Plate_Name': plate_name,
                'Plate_Well': missing_well,
                'Molecule_Name': "",
                'SMILES': "",
                'Compound_number': "",
                'All_Compounds_Flip700_z_score': np.nan,
                'Hits_Flip700_z_score': np.nan,
                'High_Controls_z_score': np.nan
            }
            compiled_data.append(new_row)
    df_with_missing = pd.concat([df, pd.DataFrame(compiled_data)], ignore_index=True)
    return df_with_missing

def compile_flip700(files):
    all_data = pd.DataFrame(columns=[
        'Library', 'Library_Copy_number', 'Plate_Name', 'Plate_Well', 'Molecule_Name', 'SMILES', 
        'Compound_number', 'All_Compounds_Flip700_z_score', 'Hits_Flip700_z_score', 'High_Controls_z_score'
    ])
    for file in files:
        file_data = process_excel_file(file)
        all_data = pd.concat([all_data, file_data], ignore_index=True)
    all_data_sorted = sort_compiled_data(all_data)
    all_data_with_missing = add_missing_wells(all_data_sorted)
    final_sorted_data = sort_compiled_data(all_data_with_missing)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        final_sorted_data.to_excel(writer, sheet_name='Compiled_Data', index=False)
    output.seek(0)
    processed_data = {
        'Compiled_Data': {
            'columns': final_sorted_data.columns.tolist(),
            'rows': final_sorted_data.values.tolist()
        }
    }
    return processed_data, output, 'Compiled_Flip700.xlsx'
