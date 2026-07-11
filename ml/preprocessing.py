import pandas as pd
import logging
from ml.config import STANDARD_COLUMNS


STANDARD_COLUMNS = {
    "InvoiceNo": ["InvoiceNo", "Invoice No", "Invoice Number", "Bill No", "Bill Number", "Order ID", "Order Number"],
    #"StockCode": ["StockCode", "Stock Code", "Product Code", "Item Code", "SKU", "Code"],
    # "Description": ["Description", "Product", "Product Name", "Item", "Item Name", "Name"],
    "Quantity": ["Quantity", "Qty", "Units", "Count"],
    "InvoiceDate": ["InvoiceDate", "Invoice Date", "Date", "Purchase Date", "Order Date", "Transaction Date"],
    "UnitPrice": ["UnitPrice", "Unit Price", "Price", "Rate", "Cost", "Selling Price"],
    "CustomerID": ["CustomerID", "Customer ID", "Customer", "Client ID", "User ID"],
    "Country": ["Country", "Nation"]
}

class DataPreprocess:
    def standardCols(self, cols: list, stdCols: dict) -> list:
        for col in cols: 
            if col in STANDARD_COLUMNS.values:
                cols
                
        
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