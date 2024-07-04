import pandas as pd
from scipy.stats import linregress

class PhlUtilities:
    
    @staticmethod
    def calculate_pHL_VL2_BL1(analysis_df):
        analysis_df['pHL_VL2_BL1'] = analysis_df['phl_vl2'] / analysis_df['phl_bl1']
        return analysis_df
    
    @staticmethod
    def calculate_slope_phl_vl2_phl_bl1(analysis_df):
        slope, _, _, _, _ = linregress(analysis_df['relative_well_number'], analysis_df['pHL_VL2_BL1'])
        return slope
    
    @staticmethod
    def calculate_mean_phl_vl2_phl_bl1(analysis_df):
        mean_phl_vl2_phl_bl1 = analysis_df['slope_corrected_phl_vl2_bl1'].mean()
        return mean_phl_vl2_phl_bl1
    
    @staticmethod
    def calculate_sd_phl_vl2_phl_bl1(analysis_df):
        sd_phl_vl2_phl_bl1 = analysis_df['slope_corrected_phl_vl2_bl1'].std()
        return sd_phl_vl2_phl_bl1
    
    @staticmethod
    def calculate_cuttoff_phl_vl2_phl_bl1(mean_phl_vl2_phl_bl1, sd_phl_vl2_phl_bl1):
        cutoff = mean_phl_vl2_phl_bl1 + (1.5 * sd_phl_vl2_phl_bl1)
        return cutoff
    
    @staticmethod
    def calculate_slope_corrected_phl_vl2_bl1(analysis_df, slope_phl_vl2_phl_bl1):
        analysis_df['slope_corrected_phl_vl2_bl1'] = analysis_df['pHL_VL2_BL1'] - (analysis_df['relative_well_number'] * slope_phl_vl2_phl_bl1)
        return analysis_df
    
    @staticmethod
    def populate_cutoff_PHL_VL2_BL1_below_cuttoff(analysis_df, cuttoff_phl_vl2_phl_bl1):
        analysis_df['cutoff_PHL_VL2_BL1_below_cuttoff'] = analysis_df['slope_corrected_phl_vl2_bl1']
        phl_cuttoff = analysis_df.loc[analysis_df['slope_corrected_phl_vl2_bl1'] > cuttoff_phl_vl2_phl_bl1, ['well_number', 'cutoff_PHL_VL2_BL1_below_cuttoff', 'phl_z_score']].copy()
        analysis_df.loc[analysis_df['slope_corrected_phl_vl2_bl1'] > cuttoff_phl_vl2_phl_bl1, 'cutoff_PHL_VL2_BL1_below_cuttoff'] = None
        return analysis_df, phl_cuttoff
    
    @staticmethod
    def calculate_corrected_mean_phl_vl2_phl_bl1(analysis_df):
        corrected_mean_phl_vl2_phl_bl1 = analysis_df['cutoff_PHL_VL2_BL1_below_cuttoff'].mean()
        return corrected_mean_phl_vl2_phl_bl1
    
    @staticmethod
    def calculate_corrected_sd_phl_vl2_phl_bl1(analysis_df):
        corrected_sd_phl_vl2_phl_bl1 = analysis_df['cutoff_PHL_VL2_BL1_below_cuttoff'].std()
        return corrected_sd_phl_vl2_phl_bl1
    
    @staticmethod
    def populate_phl_z_score(analysis_df, corrected_mean_phl_vl2_phl_bl1, corrected_sd_phl_vl2_phl_bl1):
        if not analysis_df['cutoff_PHL_VL2_BL1_below_cuttoff'].isna().all():
            analysis_df['phl_z_score'] = (analysis_df['cutoff_PHL_VL2_BL1_below_cuttoff'] - corrected_mean_phl_vl2_phl_bl1)/corrected_sd_phl_vl2_phl_bl1
        return analysis_df
    
    @staticmethod
    def populate_phl_cuttoff_z_scores(phl_cuttoff, corrected_mean_phl_vl2_phl_bl1, corrected_sd_phl_vl2_phl_bl1):
        phl_cuttoff['phl_z_score'] = (phl_cuttoff['cutoff_PHL_VL2_BL1_below_cuttoff'] - corrected_mean_phl_vl2_phl_bl1)/corrected_sd_phl_vl2_phl_bl1
        return phl_cuttoff
    
    @staticmethod
    def populate_hits_phl_z_score(analysis_df):
        analysis_df['phl_z_score'] = pd.to_numeric(analysis_df['phl_z_score'], errors='coerce')
        condition = (analysis_df['cutoff_PHL_VL2_BL1_below_cuttoff'].notna()) & (analysis_df['phl_z_score'] < -5) & (analysis_df['phl_count'] >= 1000)
        analysis_df.loc[condition, 'hits_phl_z_score'] = analysis_df.loc[condition, 'phl_z_score']
        return analysis_df
