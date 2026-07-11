import pandas as pd
import logging

class DataPreprocess:
    def standardCols(self, cols: list) -> pd.DataFrame:
        return df[cols]
    
    def cleanData(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info(f'Cleaning the Data...')
        
        # drop all NaN
        df = df.dropna()
        
        # convert to pandas datetime
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        
        # remove the cancelled orders (Invoice containing 'C')
        df = df[~df['Invoice'].str.contains('C', na=False)]
        
        # adding total price feature
        df['TotalPrice'] = df['Quantity'] * df['Price']

        logging.info(f'Cleaning successful remainig rows: {df.shape[0]}')
        
        return df