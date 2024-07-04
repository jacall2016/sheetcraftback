import os
import pandas as pd
import io
from .utilities import AnalysisUtilities
from .utilities.Flip700utilities import Flip700Utilities
from .utilities.ph1utilities import PhlUtilities
from .utilities.liveutilities import LiveUtilities
from .utilities.yemkutilities import YemkUtilities

import matplotlib.pyplot as plt

class Generate:

    @staticmethod
    def generate_flip700(analysis_df):
        analysis_df = Flip700Utilities.calculate_Flip700_vl2_bl1(analysis_df)
        slope_Flip700_vl2_Flip700_bl1 = Flip700Utilities.calculate_slope_Flip700_vl2_bl1(analysis_df)
        analysis_df = Flip700Utilities.calculate_slope_corrected_flip700_vl2_bl1(analysis_df, slope_Flip700_vl2_Flip700_bl1)
        mean_Flip700_vl2_Flip700_bl1 = Flip700Utilities.calculate_mean_flip700_vl2_flip700_bl1(analysis_df)
        sd_Flip700_vl2_Flip700_bl1 = Flip700Utilities.calculate_sd_flip700_vl2_flip700_bl1(analysis_df)
        cuttoff_Flip700_vl2_Flip700_bl1 = Flip700Utilities.calculate_cuttoff_flip700_vl2_flip700_bl1(mean_Flip700_vl2_Flip700_bl1, sd_Flip700_vl2_Flip700_bl1)
        analysis_df, flip700_cuttoff = Flip700Utilities.populate_cutoff_flip700_vl2_bl1_below_cuttoff(analysis_df, cuttoff_Flip700_vl2_Flip700_bl1)
        corrected_mean_Flip700_vl2_Flip700_bl1 = Flip700Utilities.calculate_corrected_mean_flip700_vl2_flip700_bl1(analysis_df)
        corrected_sd_Flip700_vl2_Flip700_bl1 = Flip700Utilities.calculate_corrected_sd_flip700_vl2_flip700_bl1(analysis_df)
        analysis_df = Flip700Utilities.populate_flip700_z_score(analysis_df, corrected_mean_Flip700_vl2_Flip700_bl1, corrected_sd_Flip700_vl2_Flip700_bl1)
        flip700_cuttoff_z_scores = Flip700Utilities.populate_flip700_cuttoff_z_scores(flip700_cuttoff, corrected_mean_Flip700_vl2_Flip700_bl1, corrected_sd_Flip700_vl2_Flip700_bl1)
        analysis_df = Flip700Utilities.populate_hits_flip700_z_score(analysis_df)

        flip700_indicators = pd.DataFrame({
            'slope_Flip700': [slope_Flip700_vl2_Flip700_bl1],
            'mean_Flip700': [mean_Flip700_vl2_Flip700_bl1], #corrected_mean_Flip700_vl2_flip700_bl1
            'corrected_mean_Flip700': [corrected_mean_Flip700_vl2_Flip700_bl1],
            'sd_Flip700': [sd_Flip700_vl2_Flip700_bl1], #sd_Flip700_vl2_flip700_bl1
            'corrected_sd_Flip700': [corrected_sd_Flip700_vl2_Flip700_bl1], #corrected_sd_Flip700_vl2_flip700_bl1
            'cuttoff_Flip700': [cuttoff_Flip700_vl2_Flip700_bl1], #cuttoff_Flip700_vl2_flip700_bl1
        })

        return analysis_df, flip700_indicators, flip700_cuttoff_z_scores

    @staticmethod
    def generate_yemk(analysis_df):
        analysis_df = YemkUtilities.calculate_yemk_vl2_bl1(analysis_df)
        slope_yemk_vl2_yemk_bl1 = YemkUtilities.calculate_slope_yemk_vl2_bl1(analysis_df)
        analysis_df = YemkUtilities.calculate_slope_corrected_yemk_vl2_bl1(analysis_df, slope_yemk_vl2_yemk_bl1)
        mean_yemk_vl2_yemk_bl1 = YemkUtilities.calculate_mean_yemk_vl2_yemk_bl1(analysis_df)
        sd_yemk_vl2_yemk_bl1 = YemkUtilities.calculate_sd_yemk_vl2_yemk_bl1(analysis_df)
        cuttoff_yemk_vl2_yemk_bl1 = YemkUtilities.calculate_cuttoff_yemk_vl2_yemk_bl1(mean_yemk_vl2_yemk_bl1, sd_yemk_vl2_yemk_bl1)
        analysis_df, yemk_cuttoff = YemkUtilities.populate_cutoff_yemk_vl2_bl1_below_cuttoff(analysis_df, cuttoff_yemk_vl2_yemk_bl1)
        corrected_mean_yemk_vl2_yemk_bl1 = YemkUtilities.calculate_corrected_mean_yemk_vl2_yemk_bl1(analysis_df)
        corrected_sd_yemk_vl2_yemk_bl1 = YemkUtilities.calculate_corrected_sd_yemk_vl2_yemk_bl1(analysis_df)
        analysis_df = YemkUtilities.populate_yemk_z_score(analysis_df, corrected_mean_yemk_vl2_yemk_bl1, corrected_sd_yemk_vl2_yemk_bl1)
        yemk_cuttoff_z_scores = YemkUtilities.populate_yemk_cuttoff_z_scores(yemk_cuttoff, corrected_mean_yemk_vl2_yemk_bl1, corrected_sd_yemk_vl2_yemk_bl1)
        analysis_df = YemkUtilities.populate_hits_yemk_z_score(analysis_df)

        yemk_indicators = pd.DataFrame({
            'slope_yemk': [slope_yemk_vl2_yemk_bl1],
            'mean_yemk': [mean_yemk_vl2_yemk_bl1],
            'corrected_mean_yemk': [corrected_mean_yemk_vl2_yemk_bl1],
            'sd_yemk': [sd_yemk_vl2_yemk_bl1],
            'corrected_sd_yemk': [corrected_sd_yemk_vl2_yemk_bl1],
            'cuttoff_yemk': [cuttoff_yemk_vl2_yemk_bl1],
        })

        return analysis_df, yemk_indicators, yemk_cuttoff_z_scores

    @staticmethod
    def generate_phl(analysis_df):
        analysis_df = PhlUtilities.calculate_pHL_VL2_BL1(analysis_df)
        slope_phl_vl2_phl_bl1 = PhlUtilities.calculate_slope_phl_vl2_phl_bl1(analysis_df)
        analysis_df = PhlUtilities.calculate_slope_corrected_phl_vl2_bl1(analysis_df, slope_phl_vl2_phl_bl1)
        mean_phl_vl2_phl_bl1 = PhlUtilities.calculate_mean_phl_vl2_phl_bl1(analysis_df)
        sd_phl_vl2_phl_bl1 = PhlUtilities.calculate_sd_phl_vl2_phl_bl1(analysis_df)
        cuttoff_phl_vl2_phl_bl1 = PhlUtilities.calculate_cuttoff_phl_vl2_phl_bl1(mean_phl_vl2_phl_bl1, sd_phl_vl2_phl_bl1)
        analysis_df, phl_cuttoff = PhlUtilities.populate_cutoff_PHL_VL2_BL1_below_cuttoff(analysis_df, cuttoff_phl_vl2_phl_bl1)
        corrected_mean_phl_vl2_phl_bl1 = PhlUtilities.calculate_corrected_mean_phl_vl2_phl_bl1(analysis_df)
        corrected_sd_phl_vl2_phl_bl1 = PhlUtilities.calculate_corrected_sd_phl_vl2_phl_bl1(analysis_df)
        analysis_df = PhlUtilities.populate_phl_z_score(analysis_df, corrected_mean_phl_vl2_phl_bl1, corrected_sd_phl_vl2_phl_bl1)
        phl_cuttoff_z_score = PhlUtilities.populate_phl_cuttoff_z_scores(phl_cuttoff, corrected_mean_phl_vl2_phl_bl1, corrected_sd_phl_vl2_phl_bl1)
        analysis_df = PhlUtilities.populate_hits_phl_z_score(analysis_df)

        phl_indicators = pd.DataFrame({
            'slope_ph': [slope_phl_vl2_phl_bl1],
            'mean_ph': [mean_phl_vl2_phl_bl1],
            'corrected_mean_ph': [corrected_mean_phl_vl2_phl_bl1],
            'sd_ph': [sd_phl_vl2_phl_bl1],
            'corrected_sd_ph': [corrected_sd_phl_vl2_phl_bl1],
            'cuttoff_ph': [cuttoff_phl_vl2_phl_bl1],
        })

        return analysis_df, phl_indicators, phl_cuttoff_z_score

    @staticmethod
    def generate_live(analysis_df):
        live_mean = LiveUtilities.calculate_live_mean(analysis_df)
        live_sd = LiveUtilities.calculate_live_sd(analysis_df)
        analysis_df = LiveUtilities.populate_live_z_score(analysis_df, live_mean, live_sd)
        analysis_df = LiveUtilities.populate_hits_live_z_score(analysis_df)
        live_indicators = pd.DataFrame({
            'live_mean': [live_mean],
            'live_sd': [live_sd]
        })
        return analysis_df, live_indicators

    @staticmethod
    def generate_graphs(analysis_df, y_axes_list, zip_file, output_folder):
        os.makedirs(output_folder, exist_ok=True)
        for y_axis in y_axes_list:
            fig, ax = plt.subplots()
            ax.scatter(analysis_df['relative_well_number'], analysis_df[y_axis])
            ax.set_xlabel('Relative Well Number')
            ax.set_ylabel(y_axis.replace('_', ' ').title())
            ax.set_title(f'Relative Well Number vs {y_axis}')
            max_value = analysis_df[y_axis].max()
            buffer_factor = 1.1
            ax.set_ylim(0, max_value * buffer_factor)

            with io.BytesIO() as img_buffer:
                plt.savefig(img_buffer, format='png')
                plt.close(fig)
                zip_file.writestr(f"{output_folder}/{y_axis}_scatterplot.png", img_buffer.getvalue())

    @staticmethod
    def write_analysis_sheet(analysis_df, zip_file, file_path, new_sheet_name, analysis_indicators):
        analysis_indicators = pd.melt(analysis_indicators, var_name='indicators', value_name='value')
        original_file_name = os.path.basename(file_path)
        new_file_name = f"analysis_{original_file_name}"

        original_df = pd.read_excel(file_path, sheet_name=None)
        if new_sheet_name in original_df:
            del original_df[new_sheet_name]

        with pd.ExcelWriter(zip_file, engine='openpyxl') as writer:
            for sheet_name, sheet_df in original_df.items():
                sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
            analysis_df.to_excel(writer, sheet_name=new_sheet_name, index=False)
            analysis_indicators.to_excel(writer, "Analysis_indicators", index=False)
