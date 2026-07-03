import pandas as pd
from pathlib import Path
import logging

class DataLoader:
    def __init__(self, fullPath: str):
        self.fullPath = fullPath
        
    def load_data(self) -> pd.DataFrame:
        extension = Path(self.fullPath).suffix.lower()
        
        logging.info(f'Loading data from {self.fullPath} ...')

        if extension == '.csv':
            df = pd.read_csv(rf'{self.fullPath}')
        
        elif extension in ['.xlsx', '.xls']:
            df = pd.read_excel(rf'{self.fullPath}')

        else:
            raise ValueError(f'Unsupported file type: {extension}')
        
        logging.info(f'Successfully read the the file')
        return df
