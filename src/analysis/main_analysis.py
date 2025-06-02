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
        
        # Calculate total revenue and percentage contribution
        total_revenue = contracts_df['revenue'].sum()
        revenue_by_source = contracts_df.groupby('source')['revenue'].sum()
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
        for _, row in top_5_risky.iterrows():
            current_value = row['current_revenue']
            future_value = row['projected_revenue_2030']
            cagr = ((future_value / current_value) ** (1/years) - 1) * 100
            
            cagr_results[row['brand_name']] = round(cagr, 2)
        
        self.results['cagr'] = cagr_results
        return cagr_results

    def estimate_population_impact(self) -> Dict:
        """Estimate population impact of high-risk brands."""
        demography_df = self.data['demography']
        advertisers_df = self.data['advertisers_with_risk']
        
        # Calculate impact metrics
        high_risk_brands = advertisers_df[advertisers_df['health_risk_index'] > 70]
        total_users = demography_df['total_viewers'].sum()
        
        impact_metrics = {
            'total_affected_population': total_users * 0.15,  # Assuming 15% impact
            'high_risk_brands_count': len(high_risk_brands),
            'average_risk_score': high_risk_brands['health_risk_index'].mean()
        }
        
        self.results['population_impact'] = impact_metrics
        return impact_metrics

    def analyze_celebrity_endorsements(self) -> pd.DataFrame:
        """Analyze celebrity endorsements for high-risk brands."""
        advertisers_df = self.data['advertisers_with_risk']
        
        # Get top 5 celebrities promoting high-risk brands
        high_risk_brands = advertisers_df[advertisers_df['health_risk_index'] > 70]
        celebrity_endorsements = high_risk_brands.groupby('celebrity_name').agg({
            'brand_name': 'count',
            'health_risk_index': 'mean'
        }).nlargest(5, 'brand_name')
        
        self.results['celebrity_endorsements'] = celebrity_endorsements
        return celebrity_endorsements

    def calculate_advertising_ethics_index(self) -> float:
        """Calculate Advertising Ethics Index (AEI)."""
        advertisers_df = self.data['advertisers_with_risk']
        
        # Calculate AEI components
        risk_score = 100 - advertisers_df['health_risk_index'].mean()
        diversity_score = len(advertisers_df['product_type'].unique()) * 10
        compliance_score = advertisers_df['compliance_score'].mean()
        
        # Calculate final AEI
        aei = (risk_score * 0.4 + diversity_score * 0.3 + compliance_score * 0.3)
        
        self.results['aei'] = round(aei, 2)
        return aei

    def save_results(self, output_dir: str = "results"):
        """Save analysis results to files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save results as JSON
        with open(output_path / "analysis_results.json", "w") as f:
            json.dump(self.results, f, indent=4)
        
        # Save detailed results as CSV files
        for name, result in self.results.items():
            if isinstance(result, pd.DataFrame):
                result.to_csv(output_path / f"{name}.csv", index=True)
        
        logger.info(f"Analysis results saved to {output_dir}")

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