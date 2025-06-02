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
        
        # Rename columns for consistency
        df = df.rename(columns={
            'advertiser_brand': 'brand_name',
            'category': 'product_type',
            'brand_ambassadors': 'celebrity_name',
            'health_social_risk': 'social_risk_description'
        })
        
        # Add your data cleaning steps here
        # Example: Handle missing values, etc.
        
        self.processed_data['advertisers_clean'] = df
        return df

    def calculate_health_risk_index(self):
        """Calculate health/social risk index for advertisers."""
        df = self.processed_data['advertisers_clean'].copy()
        
        # Map qualitative risk descriptions to numerical scores
        risk_mapping = {
            'High': 90,
            'Medium': 50,
            'Low': 20,
            'Very High': 100,
            'Very Low': 10
        }
        
        df['health_risk_index'] = df['social_risk_description'].map(risk_mapping).fillna(0)
        
        self.processed_data['advertisers_with_risk'] = df
        return df

    def process_revenue_data(self):
        """Process revenue and contract data."""
        revenue_df = self.processed_data['revenue'].copy()
        contracts_df = self.processed_data['contracts'].copy()
        
        # Add your revenue processing logic here
        # Example: Ensure consistent column names, data types, etc.
        
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

def print_advertisers_columns():
    try:
        df = pd.read_excel("Dataset/fact_ipl_advertisers.xlsx")
        print("Advertisers data columns:")
        print(df.columns.tolist())
    except Exception as e:
        print(f"Error reading file: {e}")

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
    print_advertisers_columns() 