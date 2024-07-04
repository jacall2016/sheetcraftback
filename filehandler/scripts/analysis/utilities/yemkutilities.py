import pandas as pd
from scipy.stats import linregress
from datetime import datetime
from .AnalysisUtilities import AnalysisUtilities

class YemkUtilities:
    
    @staticmethod
    def get_new_column_names():
        new_column_names_list = [
            "pHL_VL2_BL1", "yemk_vl2_bl1", "relative_well_number", 
            "slope_corrected_phl_vl2_bl1", "slope_corrected_yemk_vl2_bl1", 
            "cutoff_PHL_VL2_BL1_below_cuttoff", "cutoff_yemk_vl2_bl1_below_cuttoff", 
            "phl_z_score", "yemk_z_score", "live_z_score", 
            "hits_phl_z_score", "hits_yemk_z_score", "hits_live_z_score"
        ]
        return new_column_names_list

    @staticmethod
    def prepare_analysis_df(file_like_object, remove_columns_names):
        sheet1="Samples"
        sheet2="High Controls"
        samples_df = pd.read_excel(file_like_object, sheet_name=sheet1)
        high_controls_df = pd.read_excel(file_like_object, sheet_name=sheet2)
        combined_df = pd.concat([samples_df, high_controls_df], ignore_index=True)
        combined_df = pd.read_excel(file_like_object)
        combined_df = combined_df.dropna(how='all')
        combined_df = combined_df[~combined_df[combined_df.columns[0]].str.lower().isin(remove_columns_names)]
        combined_df = combined_df.drop_duplicates()
        old_column_name_list = AnalysisUtilities.get_old_column_names(combined_df)
        renamed_column_names_list = YemkUtilities.get_renamed_column_names()
        new_column_names_list = YemkUtilities.get_new_column_names()
        analysis_df = AnalysisUtilities.rewrite_column_names(combined_df, old_column_name_list, renamed_column_names_list, new_column_names_list)
        analysis_df = AnalysisUtilities.calculate_relative_well_number(analysis_df)
        file_name = "analysis"
        new_sheet_name = "Analysis"
        return analysis_df, file_name, new_sheet_name 

    @staticmethod
    def get_renamed_column_names():
        renamed_column_names_list = [
            "well_number", "total_count", "phl_count", "yemk_count", 
            "live_percentage", "dead_percentage", "phl_vl2", "phl_bl1", 
            "yemk_vl2", "yemk_bl1"
        ]
        return renamed_column_names_list
    
    @staticmethod
    def calculate_yemk_vl2_bl1(analysis_df):
        analysis_df['yemk_vl2_bl1'] = analysis_df['yemk_vl2'] / analysis_df['yemk_bl1']
        return analysis_df
    
    @staticmethod
    def calculate_slope_yemk_vl2_bl1(analysis_df):
        slope, _, _, _, _ = linregress(analysis_df['relative_well_number'], analysis_df['yemk_vl2_bl1'])
        return slope
    
    @staticmethod
    def calculate_mean_yemk_vl2_yemk_bl1(analysis_df):
        mean_yemk_vl2_yemk_bl1 = analysis_df['slope_corrected_yemk_vl2_bl1'].mean()
        return mean_yemk_vl2_yemk_bl1
    
    @staticmethod
    def calculate_sd_yemk_vl2_yemk_bl1(analysis_df):
        sd_yemk_vl2_yemk_bl1 = analysis_df['slope_corrected_yemk_vl2_bl1'].std()
        return sd_yemk_vl2_yemk_bl1
    
    @staticmethod
    def calculate_cuttoff_yemk_vl2_yemk_bl1(mean_yemk_vl2_yemk_bl1, sd_yemk_vl2_yemk_bl1):
        cutoff = mean_yemk_vl2_yemk_bl1 + (1.5 * sd_yemk_vl2_yemk_bl1)
        return cutoff
    
    @staticmethod
    def calculate_slope_corrected_yemk_vl2_bl1(analysis_df, slope_yemk_vl2_yemk_bl1):
        analysis_df['slope_corrected_yemk_vl2_bl1'] = analysis_df['yemk_vl2_bl1'] - (analysis_df['relative_well_number'] * slope_yemk_vl2_yemk_bl1)
        return analysis_df
    
    @staticmethod
    def populate_cutoff_yemk_vl2_bl1_below_cuttoff(analysis_df, cuttoff_yemk_vl2_yemk_bl1):
        analysis_df['cutoff_yemk_vl2_bl1_below_cuttoff'] = analysis_df['slope_corrected_yemk_vl2_bl1']
        yemk_cuttoff = analysis_df.loc[analysis_df['slope_corrected_yemk_vl2_bl1'] > cuttoff_yemk_vl2_yemk_bl1, ['well_number', 'cutoff_yemk_vl2_bl1_below_cuttoff', 'yemk_z_score']].copy()
        analysis_df.loc[analysis_df['slope_corrected_yemk_vl2_bl1'] > cuttoff_yemk_vl2_yemk_bl1, 'cutoff_yemk_vl2_bl1_below_cuttoff'] = None
        return analysis_df, yemk_cuttoff
    
    @staticmethod
    def calculate_corrected_mean_yemk_vl2_yemk_bl1(analysis_df):
        corrected_mean_yemk_vl2_yemk_bl1 = analysis_df['cutoff_yemk_vl2_bl1_below_cuttoff'].mean()
        return corrected_mean_yemk_vl2_yemk_bl1
    
    @staticmethod
    def calculate_corrected_sd_yemk_vl2_yemk_bl1(analysis_df):
        corrected_sd_yemk_vl2_yemk_bl1 = analysis_df['cutoff_yemk_vl2_bl1_below_cuttoff'].std()
        return corrected_sd_yemk_vl2_yemk_bl1
    
    @staticmethod
    def populate_yemk_z_score(analysis_df, corrected_mean_yemk_vl2_yemk_bl1, corrected_sd_yemk_vl2_yemk_bl1):
        if not analysis_df['cutoff_yemk_vl2_bl1_below_cuttoff'].isna().all():
            analysis_df['yemk_z_score'] = (analysis_df['cutoff_yemk_vl2_bl1_below_cuttoff'] - corrected_mean_yemk_vl2_yemk_bl1)/corrected_sd_yemk_vl2_yemk_bl1
        return analysis_df
    
    @staticmethod
    def populate_yemk_cuttoff_z_scores(yemk_cuttoff, corrected_mean_yemk_vl2_yemk_bl1, corrected_sd_yemk_vl2_yemk_bl1):
        yemk_cuttoff['yemk_z_score'] = (yemk_cuttoff['cutoff_yemk_vl2_bl1_below_cuttoff'] - corrected_mean_yemk_vl2_yemk_bl1)/corrected_sd_yemk_vl2_yemk_bl1
        return yemk_cuttoff

    @staticmethod
    def populate_hits_yemk_z_score(analysis_df):
        analysis_df['yemk_z_score'] = pd.to_numeric(analysis_df['yemk_z_score'], errors='coerce')
        condition = (analysis_df['cutoff_yemk_vl2_bl1_below_cuttoff'].notna()) & (analysis_df['yemk_z_score'] < -5) & (analysis_df['yemk_count'] >= 1000)
        analysis_df.loc[condition, 'hits_yemk_z_score'] = analysis_df.loc[condition, 'yemk_z_score']
        return analysis_df
    
    @staticmethod
    def export_All_Cuttoff(phl_cuttoff_z_score, yemk_cuttoff_z_score, excel_buffer, sheet_name):
        export_df = pd.merge(phl_cuttoff_z_score, yemk_cuttoff_z_score, on='well_number')
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            export_df.to_excel(writer, sheet_name=sheet_name, index=False)
        return export_df

    @staticmethod
    def export_All_Plates_yemk_pHL_Live(analysis_df, excel_buffer, base_sheet_name):
        selected_columns = ['well_number', 'phl_z_score', 'yemk_z_score', 'live_z_score']
        export_df = analysis_df[selected_columns]
        formatted_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        sheet_name = f"{base_sheet_name}_{formatted_datetime}"
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            export_df.to_excel(writer, sheet_name=sheet_name, index=False)
        return export_df
    
    @staticmethod
    def export_All_hits(analysis_df, excel_buffer, sheet_name):
        selected_columns = ['well_number', 'hits_phl_z_score', 'hits_yemk_z_score', 'hits_live_z_score']
        export_df = analysis_df[analysis_df[selected_columns].map(lambda x: isinstance(x, (int, float))).any(axis=1)]
        export_df = export_df[selected_columns]
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            export_df.to_excel(writer, sheet_name=sheet_name, index=False)
        return export_df

    @staticmethod
    def write_analysis_sheet(analysis_df, excel_buffer, new_sheet_name, analysis_indicators):
        analysis_indicators = pd.melt(analysis_indicators, var_name='indicators', value_name='value')
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            analysis_df.to_excel(writer, sheet_name=new_sheet_name, index=False)
            analysis_indicators.to_excel(writer, "Analysis_indicators", index=False)
        return excel_buffer