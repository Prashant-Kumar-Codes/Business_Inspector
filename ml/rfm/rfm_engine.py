import pandas as pd
import logging

class RFMEngine:
    def __init__(self, segment_map: dict, segment_fea: list, summary_fea: list):
        self.segment_map = segment_map
        self.segment_fea = segment_fea
        self.summary_fea = summary_fea
        
    def calcuate_rfm(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate Recency, Frequency and Monetory values and add these feature to dataframe"""
        
        #recency
        self.recency = (df['InvoiceDate'].max() - df.groupby('Customer ID').agg({'InvoiceDate': 'max'})).rename(columns={'InvoiceDate': 'Recency'})
        self.recency['Recency'] = self.recency['Recency'].apply(lambda x: x.days)
        
        #frequency
        self.freq = df.groupby('Customer ID').agg({'InvoiceDate': 'nunique'}).rename(columns={'InvoiceDate': 'Frequency'})
        
        # monetary
        self.monetary = df.groupby('Customer ID').agg({'TotalPrice':'sum'}).rename(columns={'TotalPrice':'Monetary'})
        
        return pd.concat([self.recency, self.freq, self.monetary], axis=1)
        
    def rfm_score(self, rfm: pd.DataFrame) -> pd.DataFrame:
        'Calcuate RFM score and return RFM value and RFM Score DataFrame'
        rfm['RecencyScore'] = pd.qcut(rfm['Recency'], q=5, labels=[5,4,3,2,1])
        
        rfm['FrequencyScore'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=5, labels=[1,2,3,4,5])
        
        rfm['MonetaryScore'] = pd.qcut(rfm['Monetary'], q=5, labels=[1,2,3,4,5])
        
        return rfm
    
    def assign_segments(self, rfm: pd.DataFrame) -> pd.DataFrame:
        'Assign the segment names as per the RM score and return full fledged RFM dataframe for each Customer ID'
        
        rfm['Segment'] = rfm['RecencyScore'].astype(str)+rfm['FrequencyScore'].astype(str)

        rfm['Segment'] = rfm['Segment'].replace(self.segment_map, regex=True)

        rfm['CustomerID'] = rfm.index.astype(int)
        rfm.reset_index(drop=True, inplace=True)
        rfm = rfm[self.segment_fea]
        
        return rfm

    def rfm_summary(self, rfm: pd.DataFrame) -> pd.DataFrame:
        rfmSummary = rfm[['Segment', 'Recency', 'Frequency', 'Monetary']].groupby('Segment').agg(['mean', 'median', 'std'])

        rfmSummary.columns = rfmSummary.columns.map('_'.join).str.strip('|')
        rfmSummary['Segment'] = rfmSummary.index
        rfmSummary['Segment_count'] = rfm['Segment'].value_counts()
        rfmSummary = rfmSummary.reset_index(drop=True)
        rfmSummary = rfmSummary[self.summary_fea]
        
        return rfmSummary