import pandas as pd
import io
import zipfile
from .utilities.AnalysisUtilities import AnalysisUtilities
from .utilities.Flip700utilities import Flip700Utilities
from .generate import Generate

class GenerateFlip700PhlLive:

    @staticmethod
    def generate_files(file_content):
        file_like_object = io.BytesIO(file_content)
        remove_columns_names = AnalysisUtilities.remove_rows_names_list()
        analysis_df, file_name, new_sheet_name = Flip700Utilities.prepare_analysis_df(file_like_object, remove_columns_names)
        analysis_df, flip700_indicators, flip700_cuttoff_z_scores = Generate.generate_flip700(analysis_df)
        analysis_df, phl_indicators, phl_cuttoff_z_score = Generate.generate_phl(analysis_df)
        analysis_df, live_indicators = Generate.generate_live(analysis_df)
        analysis_indicators = pd.concat([flip700_indicators, phl_indicators, live_indicators], axis=1)
        original_file_name = "FILE_NAME"  # Temporary placeholder for file name
        file_name = f"{original_file_name}"

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            GenerateFlip700PhlLive.generate_files_phl_bl1_flip700_vl1(file_like_object, zip_file, file_name)
        zip_buffer.seek(0)
        return zip_buffer, f"analysis_flip700_phl_live.zip"

    @staticmethod
    def generate_files_phl_bl1_flip700_vl1(file_like_object, zip_file, file_name):
        remove_columns_names = AnalysisUtilities.remove_rows_names_list()
        analysis_df, file_name, new_sheet_name = Flip700Utilities.prepare_analysis_df(file_like_object, remove_columns_names=remove_columns_names)
        analysis_df, phl_indicators, phl_cuttoff_z_score = Generate.generate_phl(analysis_df)
        analysis_df, flip700_indicators, flip700_cuttoff_z_scores = Generate.generate_flip700(analysis_df)
        analysis_df, live_indicators = Generate.generate_live(analysis_df)
        analysis_indicators = pd.concat([flip700_indicators, phl_indicators, live_indicators], axis=1)
        
        with io.BytesIO() as excel_buffer:
            Flip700Utilities.export_All_Cuttoff(phl_cuttoff_z_score, flip700_cuttoff_z_scores, excel_buffer, f"All_cuttoff_flip700_phl_{file_name}.xlsx")
            zip_file.writestr(f"All_cuttoff_flip700_phl_{file_name}.xlsx", excel_buffer.getvalue())
        with io.BytesIO() as excel_buffer:
            Flip700Utilities.export_All_Plates_flip700_pHL_Live(analysis_df, excel_buffer, f"All_P_Flip700_pHL_Live_{file_name}.xlsx")
            zip_file.writestr(f"All_P_Flip700_pHL_Live_{file_name}.xlsx", excel_buffer.getvalue())
        with io.BytesIO() as excel_buffer:
            Flip700Utilities.export_All_hits(analysis_df, excel_buffer, f"All_hits_{file_name}.xlsx")
            zip_file.writestr(f"All_hits_{file_name}.xlsx", excel_buffer.getvalue())
        with io.BytesIO() as excel_buffer:
            Flip700Utilities.write_analysis_sheet(analysis_df, excel_buffer, "Analysis", analysis_indicators)
            zip_file.writestr(f"analysis_{file_name}.xlsx", excel_buffer.getvalue())
        y_axes_list = ["total_count", "phl_count", "flip700_count", "live_percentage", "pHL_VL2_BL1", "flip700_vl2_bl1"]
        Generate.generate_graphs(analysis_df, y_axes_list, zip_file, f"QC_plots_{file_name}")