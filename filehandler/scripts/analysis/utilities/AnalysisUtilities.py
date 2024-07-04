import pandas as pd
import os

class AnalysisUtilities:
    
    @staticmethod
    def getfile_name(uploaded_file_path):
        """Extract the base name (file name with extension) from the full path and remove the extension."""
        file_name_with_extension = os.path.basename(uploaded_file_path)
        file_name_without_extension = os.path.splitext(file_name_with_extension)[0]
        return file_name_without_extension

    @staticmethod
    def getsheet1_name(sheet1):
        return sheet1

    @staticmethod
    def getsheet2_name(sheet2):
        return sheet2
    
    @staticmethod
    def get_new_sheet_name(final_sheet):
        return final_sheet

    @staticmethod
    def remove_rows_names_list():
        return ['mean', 'sd']

    @staticmethod
    def get_old_column_names(combined_df):
        old_column_name_list = combined_df.columns.tolist()
        return old_column_name_list

    @staticmethod
    def rewrite_column_names(combined_df, old_column_name_list, renamed_column_names_list, new_column_names_list):
        """Rename existing columns and add new empty columns."""
        analysis_df = combined_df.copy()  # Create a copy to avoid modifying the original DataFrame

        # Rename existing columns
        for old_name, new_name in zip(old_column_name_list, renamed_column_names_list):
            analysis_df.rename(columns={old_name: new_name}, inplace=True)

        # Add new empty columns
        for new_name in new_column_names_list:
            if new_name not in analysis_df.columns:
                analysis_df[new_name] = None

        return analysis_df
    
    @staticmethod
    def calculate_relative_well_number(analysis_df):
        mapping_dict = {'A': 0, 'B': 24, 'C': 48, 'D': 72, 'E': 96, 'F': 120, 'G': 144, 'H': 168,
                        'I': 192, 'J': 216, 'K': 240, 'L': 264, 'M': 288, 'N': 312, 'O': 336, 'P': 360}

        analysis_df['relative_well_number'] = (
            pd.to_numeric(analysis_df['well_number'].str.extract('(\d+)').squeeze(), errors='coerce') +
            analysis_df['well_number'].str.extract('([A-P])').replace(mapping_dict).fillna(0).squeeze()
        )

        return analysis_df
