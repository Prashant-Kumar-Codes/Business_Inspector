import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from zipfile import ZipFile

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter(action='ignore', category=FutureWarning)

colors = [
    "darkred",
    "navy",
    "darkgreen",
    "goldenrod",
    "deeppink",
    "darkorange",
    "indigo",
    "teal",
    "darkmagenta",
    "saddlebrown",
    'gray',
    'darkblue',
    "firebrick"
]


class RFM:
    def read_file(self, file_path):
        if 'csv' in file_path:
            self.df = f.read_csv()
        elif 'xlsx' in file_path:
            self.df = f.read_excel()
        else:
            return None
        return df
    
    def preprocess(self):
        self.df = self.df[~df['Invoice'].str.contains('C', na=False)]
        
    def recency():
        self.recency = (self.df['InvoiceDate'].max() - self.df.groupby('Customer ID').agg({'InvoiceDate': 'max'})).rename(columns={'InvoiceDate': 'Recency'})
        self.recency['Recency'] = self.recency['Recency'].apply(lambda x: x.days)
    
    def frequency():
        self.freq = self.df.groupby('Customer ID').agg({'InvoiceDate': 'nunique'}).rename(columns={'InvoiceDate': 'Frequency'})
        
    def 