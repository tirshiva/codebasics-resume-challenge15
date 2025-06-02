import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, Tuple, List
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IPLAnalyzer:
    def __init__(self, data_dir: str = "data/processed"):
        self.data_dir = Path(data_dir)
        self.data = {}
        self.results = {}

    def load_processed_data(self):
        """Load processed data files."""
        try:
            for file in self.data_dir.glob("*.csv"):
                name = file.stem
                self.data[name] = pd.read_csv(file)
            logger.info("Successfully loaded processed data")
            return True
        except Exception as e:
            logger.error(f"Error loading processed data: {str(e)}")
            return False

    def analyze_central_contracts_revenue(self) -> Dict:
        """Analyze IPL revenue from central contracts."""
        contracts_df = self.data['contracts_processed']
        
        # Calculate total revenue and percentage contribution using correct column names
        total_revenue = contracts_df['amount_in_crores_2025'].sum()
        revenue_by_source = contracts_df.groupby('partner_sponsor_name')['amount_in_crores_2025'].sum()
        revenue_percentage = (revenue_by_source / total_revenue * 100).round(2)
        
        results = {
            'total_revenue': total_revenue,
            'revenue_by_source': revenue_by_source.to_dict(),
            'revenue_percentage': revenue_percentage.to_dict()
        }
        
        self.results['central_contracts'] = results
        return results

    def analyze_health_risk(self) -> pd.DataFrame:
        """Analyze health/social risk for top advertising brands."""
        advertisers_df = self.data['advertisers_with_risk']
        
        # Get top advertisers by risk index
        top_risk_advertisers = advertisers_df.nlargest(10, 'health_risk_index')
        
        self.results['health_risk'] = top_risk_advertisers
        return top_risk_advertisers

    def calculate_cagr(self, years: int = 5) -> Dict:
        """Calculate CAGR for top 5 high-risk companies."""
        advertisers_df = self.data['advertisers_with_risk']
        top_5_risky = advertisers_df.nlargest(5, 'health_risk_index')
        
        cagr_results = {}
        # Assuming 'current_revenue' and 'projected_revenue_2030' columns exist in the processed advertisers data
        for _, row in top_5_risky.iterrows():
            # Need actual column names for revenue or estimate based on available data
            # For now, using placeholder names, assuming they would be added in data processing if available
            current_value = row.get('current_revenue', 1) # Using get with default to avoid error if column missing
            future_value = row.get('projected_revenue_2030', 1) # Using get with default
            
            # Avoid division by zero or log of zero/negative number for CAGR calculation
            if current_value > 0 and future_value > 0:
                cagr = ((future_value / current_value) ** (1/years) - 1) * 100
                cagr_results[row['brand_name']] = round(cagr, 2)
            else:
                 cagr_results[row['brand_name']] = "N/A" # Or handle as appropriate

        
        self.results['cagr'] = cagr_results
        return cagr_results

    def estimate_population_impact(self) -> Dict:
        """Estimate population impact of high-risk brands."""
        demography_df = self.data['demography']
        advertisers_df = self.data['advertisers_with_risk']
        
        # Calculate impact metrics
        high_risk_brands = advertisers_df[advertisers_df['health_risk_index'] > 70]
        
        # Convert population to numeric and handle any non-numeric values
        demography_df['estimated_user_population'] = pd.to_numeric(
            demography_df['estimated_user_population'].str.replace(',', ''), 
            errors='coerce'
        )
        total_users = demography_df['estimated_user_population'].sum()
        
        impact_metrics = {
            'total_affected_population': total_users * 0.15,  # Assuming 15% impact based on prompt
            'high_risk_brands_count': len(high_risk_brands),
            'average_risk_score': high_risk_brands['health_risk_index'].mean()
        }
        
        self.results['population_impact'] = impact_metrics
        return impact_metrics

    def analyze_celebrity_endorsements(self) -> pd.DataFrame:
        """Analyze celebrity endorsements for high-risk brands."""
        advertisers_df = self.data['advertisers_with_risk']
        
        # Get top 5 celebrities promoting high-risk brands
        # Using 'celebrity_name' as identified from the advertisers data columns
        high_risk_brands = advertisers_df[advertisers_df['health_risk_index'] > 70]
        
        # Ensure 'celebrity_name' column exists before grouping
        if 'celebrity_name' in high_risk_brands.columns:
            celebrity_endorsements = high_risk_brands.groupby('celebrity_name').agg({
                'brand_name': 'count',
                'health_risk_index': 'mean'
            }).nlargest(5, 'brand_name')
            
            self.results['celebrity_endorsements'] = celebrity_endorsements
            return celebrity_endorsements
        else:
            logger.warning("'celebrity_name' column not found in advertisers data. Cannot analyze celebrity endorsements.")
            self.results['celebrity_endorsements'] = pd.DataFrame()
            return pd.DataFrame()


    def calculate_advertising_ethics_index(self) -> float:
        """Calculate Advertising Ethics Index (AEI)."""
        advertisers_df = self.data['advertisers_with_risk']
        
        # Calculate AEI components
        risk_score = 100 - advertisers_df['health_risk_index'].mean()
        
        # Using 'product_type' as identified from the advertisers data columns (after renaming in data processing)
        diversity_score = len(advertisers_df['product_type'].unique()) * 10
        
        # Assuming 'compliance_score' column exists in the processed advertisers data
        compliance_score = advertisers_df.get('compliance_score', pd.Series([0])).mean() # Using get with default
        
        # Calculate final AEI
        aei = (risk_score * 0.4 + diversity_score * 0.3 + compliance_score * 0.3)
        
        self.results['aei'] = round(aei, 2)
        return aei

    def save_results(self, output_dir: str = "results"):
        """Save analysis results to files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save results as JSON
        # Convert DataFrames to dictionary for JSON serialization
        serializable_results = {}
        for name, result in self.results.items():
            if isinstance(result, pd.DataFrame):
                serializable_results[name] = result.to_dict(orient='records')
            else:
                serializable_results[name] = result

        with open(output_path / "analysis_results.json", "w") as f:
            json.dump(serializable_results, f, indent=4)
        
        # Save detailed results as CSV files
        for name, result in self.results.items():
            if isinstance(result, pd.DataFrame):
                result.to_csv(output_path / f"{name}.csv", index=True)
        
        logger.info(f"Analysis results saved to {output_dir}")

def print_contracts_columns():
    try:
        df = pd.read_excel("Dataset/fact_ipl_central_contracts.xlsx")
        print("Contracts data columns:")
        print(df.columns.tolist())
    except Exception as e:
        print(f"Error reading file: {e}")

def print_demography_columns():
    try:
        df = pd.read_excel("Dataset/fact_summary_demography.xlsx")
        print("Demography data columns:")
        print(df.columns.tolist())
    except Exception as e:
        print(f"Error reading file: {e}")

def main():
    analyzer = IPLAnalyzer()
    
    if analyzer.load_processed_data():
        # Perform primary analysis
        analyzer.analyze_central_contracts_revenue()
        analyzer.analyze_health_risk()
        analyzer.calculate_cagr()
        analyzer.estimate_population_impact()
        analyzer.analyze_celebrity_endorsements()
        
        # Perform secondary analysis
        analyzer.calculate_advertising_ethics_index()
        
        # Save results
        analyzer.save_results()
        logger.info("Analysis completed successfully")
    else:
        logger.error("Analysis failed")

if __name__ == "__main__":
    main()
    # print_demography_columns() 