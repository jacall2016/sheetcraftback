import os
import io
import pandas as pd

def extract_plate_number(file_name):
    if "analysis_" in file_name:
        start_index = file_name.find("L")
        end_index = file_name.find("P", start_index) + 2
        if start_index != -1 and end_index != -1:
            plate_number = file_name[start_index:end_index]
            return plate_number
    return "ERROR_GETTING_FILE_NAME"

def IsHighControl(well_number):
    if len(well_number) < 3:
        return False
    if well_number[1] not in ['1', '2'] or well_number[2] != '.':
        return False
    return True

def process_excel_files(files):
    all_dfs = []
    
    for file in files:
        xls = pd.ExcelFile(file)
        if 'Analysis' in xls.sheet_names:
            df = pd.read_excel(xls, 'Analysis')
            df['high_controls'] = None
            df['plate_number'] = extract_plate_number(file.name)
            all_dfs.append(df)
    
    combined_df = pd.concat(all_dfs, ignore_index=True)

    required_columns = ['plate_number', 'well_number', 
                        'yemk_z_score', 'hits_yemk_z_score', 
                        'high_controls', 
                        'phl_z_score', 'hits_phl_z_score', 
                        'flip700_z_score', 'hits_flip700_z_score',
                        'live_z_score', 'hits_live_z_score']
    existing_columns = [col for col in required_columns if col in combined_df.columns]
    combined_df = combined_df[existing_columns]
    
    return combined_df

def separate_dataframes(combined_df):
    def create_df(columns):
        return combined_df[[col for col in columns if col in combined_df.columns]]

    yemk_df = create_df(['plate_number', 'well_number', 'yemk_z_score', 'hits_yemk_z_score', 'high_controls'])
    phl_df = create_df(['plate_number', 'well_number', 'phl_z_score', 'hits_phl_z_score', 'high_controls'])
    flip700_df = create_df(['plate_number', 'well_number', 'flip700_z_score', 'hits_flip700_z_score', 'high_controls'])
    live_df = create_df(['plate_number', 'well_number', 'live_z_score', 'hits_live_z_score', 'high_controls'])
    
    return yemk_df, phl_df, flip700_df, live_df

def populate_high_controls(df):
    z_score_columns = [col for col in df.columns if 'z_score' in col and 'hits' not in col]
    if not z_score_columns:
        return df
    z_score_column = z_score_columns[0]
    for index, row in df.iterrows():
        if IsHighControl(row['well_number']):
            df.at[index, 'high_controls'] = row[z_score_column]
    return df

def concatenate_analysis(files):
    all_dfs = []

    for file in files:
        xls = pd.ExcelFile(file)
        if 'Analysis' in xls.sheet_names:
            df = pd.read_excel(xls, 'Analysis')
            df['high_controls'] = None
            df['plate_number'] = extract_plate_number(file.name)
            all_dfs.append(df)

    combined_df = pd.concat(all_dfs, ignore_index=True)

    # Check and retain only the columns that exist
    required_columns = ['plate_number', 'well_number', 
                        'yemk_z_score', 'hits_yemk_z_score', 
                        'high_controls', 
                        'phl_z_score', 'hits_phl_z_score', 
                        'flip700_z_score', 'hits_flip700_z_score',
                        'live_z_score', 'hits_live_z_score']
    existing_columns = [col for col in required_columns if col in combined_df.columns]
    combined_df = combined_df[existing_columns]

    yemk_df, phl_df, flip700_df, live_df = separate_dataframes(combined_df)

    yemk_df = populate_high_controls(yemk_df)
    phl_df = populate_high_controls(phl_df)
    flip700_df = populate_high_controls(flip700_df)
    live_df = populate_high_controls(live_df)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        if not yemk_df.empty:
            yemk_df.to_excel(writer, index=False, sheet_name='yemk')
        if not phl_df.empty:
            phl_df.to_excel(writer, index=False, sheet_name='phl')
        if not flip700_df.empty:
            flip700_df.to_excel(writer, index=False, sheet_name='flip700')
        if not live_df.empty:
            live_df.to_excel(writer, index=False, sheet_name='live')
    output.seek(0)

    processed_data = {
        'yemk': {'columns': yemk_df.columns.tolist(), 'rows': yemk_df.values.tolist()},
        'phl': {'columns': phl_df.columns.tolist(), 'rows': phl_df.values.tolist()},
        'flip700': {'columns': flip700_df.columns.tolist(), 'rows': flip700_df.values.tolist()},
        'live': {'columns': live_df.columns.tolist(), 'rows': live_df.values.tolist()}
    }

    return processed_data, output, 'concatenated_analysis.xlsx'