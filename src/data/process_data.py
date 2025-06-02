import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, data_dir: str = "Dataset"):
        self.data_dir = Path(data_dir)
        self.processed_data = {}

    def load_data(self):
        """Load all required datasets."""
        try:
            # Load IPL advertisers data
            self.processed_data['advertisers'] = pd.read_excel(
                self.data_dir / "fact_ipl_advertisers.xlsx"
            )
            
            # Load revenue demography data
            self.processed_data['revenue'] = pd.read_excel(
                self.data_dir / "fact_revenue_demography.xlsm"
            )
            
            # Load summary demography data
            self.processed_data['demography'] = pd.read_excel(
                self.data_dir / "fact_summary_demography.xlsx"
            )
            
            # Load central contracts data
            self.processed_data['contracts'] = pd.read_excel(
                self.data_dir / "fact_ipl_central_contracts.xlsx"
            )
            
            logger.info("Successfully loaded all datasets")
            return True
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return False

    def clean_advertisers_data(self):
        """Clean and process advertisers data."""
        df = self.processed_data['advertisers'].copy()
        
        # Add your data cleaning steps here
        # Example: Remove duplicates, handle missing values, etc.
        
        self.processed_data['advertisers_clean'] = df
        return df

    def calculate_health_risk_index(self):
        """Calculate health/social risk index for advertisers."""
        df = self.processed_data['advertisers_clean'].copy()
        
        # Define risk factors and their weights
        risk_factors = {
            'product_type': {
                'pan_masala': 0.8,
                'betting_app': 0.7,
                'alcohol': 0.6,
                'tobacco': 0.9,
                'other': 0.2
            },
            'ad_frequency': {
                'high': 0.8,
                'medium': 0.5,
                'low': 0.2
            }
        }
        
        # Calculate risk index
        df['health_risk_index'] = df.apply(
            lambda row: self._calculate_risk_score(row, risk_factors),
            axis=1
        )
        
        self.processed_data['advertisers_with_risk'] = df
        return df

    def _calculate_risk_score(self, row, risk_factors):
        """Helper function to calculate risk score for each advertiser."""
        product_risk = risk_factors['product_type'].get(row['product_type'], 0.2)
        frequency_risk = risk_factors['ad_frequency'].get(row['ad_frequency'], 0.5)
        
        return (product_risk * 0.7 + frequency_risk * 0.3) * 100

    def process_revenue_data(self):
        """Process revenue and contract data."""
        revenue_df = self.processed_data['revenue'].copy()
        contracts_df = self.processed_data['contracts'].copy()
        
        # Add your revenue processing logic here
        
        self.processed_data['revenue_processed'] = revenue_df
        self.processed_data['contracts_processed'] = contracts_df
        return revenue_df, contracts_df

    def save_processed_data(self, output_dir: str = "data/processed"):
        """Save processed data to files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for name, df in self.processed_data.items():
            if isinstance(df, pd.DataFrame):
                df.to_csv(output_path / f"{name}.csv", index=False)
        
        logger.info(f"Processed data saved to {output_dir}")

def main():
    processor = DataProcessor()
    
    if processor.load_data():
        processor.clean_advertisers_data()
        processor.calculate_health_risk_index()
        processor.process_revenue_data()
        processor.save_processed_data()
        logger.info("Data processing completed successfully")
    else:
        logger.error("Data processing failed")

if __name__ == "__main__":
    main() 