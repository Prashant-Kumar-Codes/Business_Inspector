from ml.rfm.data_loader import DataLoader
from ml.rfm.preprocess import DataPreprocess
from ml.rfm.rfm_engine import RFMEngine
from ml.rfm.visualizer import Visualizer
from ml.rfm.config import COLUMNS, SEGMENT_MAP, assign_segment_features, rfm_summary_features, COLORS



import logging
import warnings

# configure basic logging and warnings
warnings.simplefilter(category=FutureWarning, action='ignore')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(full_file_path):
    # laod the data
    loader = DataLoader(full_file_path)
    raw_df = loader.load_data()
    
    
    # preprocessing of data
    preprocessor = DataPreprocess()
    stdCol_df = preprocessor.standardCols(raw_df, COLUMNS)
    clean_df = preprocessor.cleanData(stdCol_df)
    
    
    # RFM Analysis
    rfm_engine = RFMEngine(SEGMENT_MAP, assign_segment_features, rfm_summary_features)
    
        # rfm dataframe with rfm values for each customer ids
    rfm_value_df = rfm_engine.calcuate_rfm(clean_df)
    
        # rfm dataframe with rfm value and scroe for each customer ids
    rfm_score_df = rfm_engine.rfm_score(rfm_value_df)
    
        # rfm dataframe with rfm score and segement
    rfm_segment_df = rfm_engine.assign_segments(rfm_score_df)

        # rfm summary dataframe
    rfm_summary_df = rfm_engine.rfm_summary(rfm_segment_df)
    
    print("\n--- RFM Summary ---")
    print(rfm_summary_df.head())
    
    # visualizer
    visualize = Visualizer(COLORS)
    pie_plot = visualize.summary_pie_chart(rfm_summary_df)
    bar_plot = visualize.summary_bar_chart(rfm_summary_df)
    
    logging.info(f'Successfully generated the RFM of the dataset')
    
    return [rfm_segment_df, rfm_summary_df, pie_plot, bar_plot]