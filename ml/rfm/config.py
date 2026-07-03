# config file to store all the hardcoded variables and constants

# Segment Mapping
SEGMENT_MAP = {
    r'[1-2][1-2]': 'Hibernating',
    r'[1-2][3-4]': 'At Risk',
    r'[1-2]5': "Can't Loose",
    r'3[1-2]': 'About to Sleep',
    r'33': 'Need Attention',
    r'[3-4][4-5]': 'Loyal Customers',
    r'41': 'Promising',
    r'51': 'New Customers',
    r'[4-5][2-3]': 'Potential Loyalists',
    r'5[4-5]': 'Champions'
}

# feature names for ordering the outputs
assign_segment_features = ['CustomerID','Recency','Frequency', 'Monetary','RecencyScore','FrequencyScore','MonetaryScore','Segment']

rfm_summary_features = ['Segment', 'Recency_mean', 'Recency_median', 'Recency_std','Frequency_mean','Frequency_median', 'Frequency_std', 'Monetary_mean', 'Monetary_median', 'Monetary_std', 'Segment_count']

# Visualization Colors
COLORS = [
    "darkred", "navy", "darkgreen", "goldenrod", "deeppink", 
    "darkorange", "firebrick", "indigo", "teal", "darkmagenta", 
    "saddlebrown", "gray", "darkblue"
]
