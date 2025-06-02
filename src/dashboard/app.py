import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path
import sys
import os

# Add src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.analysis.main_analysis import IPLAnalyzer

# Set page config
st.set_page_config(
    page_title="IPL Economic and Social Impact Analysis",
    page_icon="🏏",
    layout="wide"
)

# Initialize analyzer
analyzer = IPLAnalyzer()

def load_results():
    """Load analysis results."""
    results_path = Path("results/analysis_results.json")
    if results_path.exists():
        with open(results_path) as f:
            return json.load(f)
    return None

def create_balanced_scorecard():
    """Create balanced scorecard for IPL advertisers."""
    st.header("Balanced Scorecard for IPL Advertisers")
    
    # Load data
    advertisers_df = pd.read_csv("results/advertisers_with_risk.csv")
    
    # Create metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Average Health Risk Index",
            f"{advertisers_df['health_risk_index'].mean():.1f}"
        )
    
    with col2:
        st.metric(
            "Total Advertisers",
            len(advertisers_df)
        )
    
    with col3:
        st.metric(
            "High Risk Advertisers",
            len(advertisers_df[advertisers_df['health_risk_index'] > 70])
        )
    
    with col4:
        st.metric(
            "Advertising Ethics Index",
            f"{analyzer.calculate_advertising_ethics_index():.1f}"
        )
    
    # Create visualization
    fig = px.scatter(
        advertisers_df,
        x='revenue_contribution',
        y='health_risk_index',
        color='product_type',
        size='ad_frequency',
        hover_data=['brand_name'],
        title="Advertiser Risk vs Revenue Contribution"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_revenue_analysis():
    """Show revenue analysis section."""
    st.header("IPL Revenue Analysis")
    
    results = load_results()
    if not results:
        st.error("No analysis results found. Please run the analysis first.")
        return
    
    revenue_data = results['central_contracts']
    
    # Create pie chart for revenue distribution
    fig = go.Figure(data=[go.Pie(
        labels=list(revenue_data['revenue_percentage'].keys()),
        values=list(revenue_data['revenue_percentage'].values()),
        hole=.3
    )])
    
    fig.update_layout(title="Revenue Distribution by Source")
    st.plotly_chart(fig, use_container_width=True)
    
    # Show detailed metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Total Revenue",
            f"₹{revenue_data['total_revenue']:,.2f}"
        )
    
    with col2:
        st.metric(
            "Average Revenue per Source",
            f"₹{revenue_data['total_revenue']/len(revenue_data['revenue_by_source']):,.2f}"
        )

def show_health_risk_analysis():
    """Show health risk analysis section."""
    st.header("Health and Social Risk Analysis")
    
    # Load data
    health_risk_df = pd.read_csv("results/health_risk.csv")
    
    # Create bar chart for top risky advertisers
    fig = px.bar(
        health_risk_df.head(10),
        x='brand_name',
        y='health_risk_index',
        color='product_type',
        title="Top 10 Advertisers by Health Risk Index"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Show detailed metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Average Risk Index",
            f"{health_risk_df['health_risk_index'].mean():.1f}"
        )
    
    with col2:
        st.metric(
            "Highest Risk Score",
            f"{health_risk_df['health_risk_index'].max():.1f}"
        )

def show_population_impact():
    """Show population impact analysis."""
    st.header("Population Impact Analysis")
    
    results = load_results()
    if not results:
        st.error("No analysis results found. Please run the analysis first.")
        return
    
    impact_data = results['population_impact']
    
    # Create metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Affected Population",
            f"{impact_data['total_affected_population']:,.0f}"
        )
    
    with col2:
        st.metric(
            "High Risk Brands",
            impact_data['high_risk_brands_count']
        )
    
    with col3:
        st.metric(
            "Average Risk Score",
            f"{impact_data['average_risk_score']:.1f}"
        )

def show_celebrity_endorsements():
    """Show celebrity endorsement analysis."""
    st.header("Celebrity Endorsement Analysis")
    
    # Load data
    celebrity_df = pd.read_csv("results/celebrity_endorsements.csv")
    
    # Create visualization
    fig = px.bar(
        celebrity_df,
        x=celebrity_df.index,
        y='brand_name',
        color='health_risk_index',
        title="Top 5 Celebrities by High-Risk Brand Endorsements"
    )
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.title("IPL Economic and Social Impact Analysis")
    
    # Create sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Balanced Scorecard", "Revenue Analysis", "Health Risk Analysis", 
         "Population Impact", "Celebrity Endorsements"]
    )
    
    # Show selected page
    if page == "Balanced Scorecard":
        create_balanced_scorecard()
    elif page == "Revenue Analysis":
        show_revenue_analysis()
    elif page == "Health Risk Analysis":
        show_health_risk_analysis()
    elif page == "Population Impact":
        show_population_impact()
    elif page == "Celebrity Endorsements":
        show_celebrity_endorsements()

if __name__ == "__main__":
    main() 