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
    
    # Add documentation
    st.markdown("""
    ### Understanding IPL Revenue
    This section analyzes the revenue distribution of IPL for 2025 across different sources. The analysis includes:
    - Total revenue from all sources
    - Revenue distribution by source
    - Top revenue contributors
    - Average revenue per source
    """)
    
    results = load_results()
    if not results:
        st.error("No analysis results found. Please run the analysis first.")
        return
    
    revenue_data = results['central_contracts']
    
    # Create a clean layout with two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create a more visually appealing pie chart
        fig = go.Figure(data=[go.Pie(
            labels=list(revenue_data['revenue_percentage'].keys()),
            values=list(revenue_data['revenue_percentage'].values()),
            hole=.4,
            marker=dict(colors=px.colors.qualitative.Set3),
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig.update_layout(
            title="Revenue Distribution by Source (2025)",
            showlegend=False,
            height=500,
            margin=dict(t=50, b=0, l=0, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Add horizontal bar chart for better comparison
        fig2 = px.bar(
            x=list(revenue_data['revenue_by_source'].values()),
            y=list(revenue_data['revenue_by_source'].keys()),
            orientation='h',
            title="Revenue by Source (in Crores)",
            labels={'x': 'Revenue (₹ Crores)', 'y': 'Source'}
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.subheader("Key Metrics")
        st.metric(
            "Total Revenue (2025)",
            f"₹{revenue_data['total_revenue']:,.0f} Cr",
            help="Total revenue from all sources in Crores"
        )
        
        # Calculate and display average revenue
        avg_revenue = revenue_data['total_revenue'] / len(revenue_data['revenue_by_source'])
        st.metric(
            "Average Revenue per Source",
            f"₹{avg_revenue:,.0f} Cr",
            help="Average revenue contribution per source"
        )
        
        # Add top revenue sources
        st.subheader("Top Revenue Sources")
        top_sources = sorted(
            revenue_data['revenue_by_source'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        for source, amount in top_sources:
            st.metric(
                source,
                f"₹{amount:,.0f} Cr",
                f"{revenue_data['revenue_percentage'][source]:.1f}%"
            )
    
    # Add insights and recommendations
    st.markdown("""
    ### Key Insights
    1. **Media Rights Domination**: 
       - JioCinema and Star Sports together contribute over 92% of total revenue
       - This shows the critical importance of broadcasting rights in IPL's revenue model
    
    2. **Revenue Concentration**:
       - Top 3 sources account for 97% of total revenue
       - High dependency on a few major revenue streams
    
    3. **Growth Opportunities**:
       - Significant potential for growth in non-media revenue streams
       - Opportunity to diversify revenue sources
    
    ### Recommendations
    1. **Revenue Diversification**:
       - Develop more non-media revenue streams
       - Focus on increasing sponsorship and merchandise sales
    
    2. **Digital Expansion**:
       - Strengthen digital presence and monetization
       - Explore new digital revenue models
    
    3. **Strategic Partnerships**:
       - Build long-term partnerships with current sponsors
       - Explore new categories for sponsorship
    """)

def show_health_risk_analysis():
    """Show health risk analysis section."""
    st.header("Health and Social Risk Analysis")
    
    # Add documentation
    st.markdown("""
    ### Understanding Health Risk Analysis
    This section analyzes the health and social risks associated with IPL advertisers. The analysis includes:
    - Risk assessment of different product categories
    - Distribution of advertisers by product type
    - Detailed brand analysis with risk scores
    - Celebrity influence on brand perception
    
    **Risk Categories:**
    - Low Risk: Health Risk Index < 30
    - Medium Risk: Health Risk Index 30-70
    - High Risk: Health Risk Index > 70
    """)
    
    results = load_results()
    if not results:
        st.error("No analysis results found. Please run the analysis first.")
        return
    
    health_risk_data = results['health_risk']
    if not health_risk_data:
        st.warning("No health risk data available.")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(health_risk_data)
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Risk Analysis", "Product Categories", "Detailed View"])
    
    with tab1:
        # Create bar chart for top risky advertisers with enhanced visualization
        fig = px.bar(
            df.head(10),
            x='brand_name',
            y='health_risk_index',
            color='product_type',
            title="Top 10 Advertisers by Health Risk Index",
            labels={
                'brand_name': 'Brand Name',
                'health_risk_index': 'Health Risk Index',
                'product_type': 'Product Type'
            },
            text='health_risk_index',  # Add value labels
            color_discrete_sequence=px.colors.qualitative.Set3  # Use a more distinct color palette
        )
        
        # Enhance the layout
        fig.update_layout(
            xaxis_tickangle=-45,
            height=600,  # Increased height for better visibility
            margin=dict(t=50, b=100, l=50, r=50),
            showlegend=True,
            legend_title="Product Type",
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                title_font=dict(size=14),
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title_font=dict(size=14),
                tickfont=dict(size=12),
                gridcolor='lightgray'
            ),
            title=dict(
                font=dict(size=20),
                x=0.5,
                y=0.95
            )
        )
        
        # Add risk level annotations
        fig.add_shape(
            type="rect",
            xref="paper", yref="y",
            x0=0, y0=70,
            x1=1, y1=100,
            fillcolor="red",
            opacity=0.1,
            layer="below",
            line_width=0
        )
        
        fig.add_shape(
            type="rect",
            xref="paper", yref="y",
            x0=0, y0=30,
            x1=1, y1=70,
            fillcolor="yellow",
            opacity=0.1,
            layer="below",
            line_width=0
        )
        
        fig.add_shape(
            type="rect",
            xref="paper", yref="y",
            x0=0, y0=0,
            x1=1, y1=30,
            fillcolor="green",
            opacity=0.1,
            layer="below",
            line_width=0
        )
        
        # Add risk level labels
        fig.add_annotation(
            xref="paper", yref="y",
            x=0.02, y=85,
            text="High Risk",
            showarrow=False,
            font=dict(color="red", size=12)
        )
        
        fig.add_annotation(
            xref="paper", yref="y",
            x=0.02, y=50,
            text="Medium Risk",
            showarrow=False,
            font=dict(color="orange", size=12)
        )
        
        fig.add_annotation(
            xref="paper", yref="y",
            x=0.02, y=15,
            text="Low Risk",
            showarrow=False,
            font=dict(color="green", size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add explanation of the visualization
        st.markdown("""
        **Understanding the Health Risk Index:**
        - **High Risk (>70)**: Products with significant health concerns
        - **Medium Risk (30-70)**: Products with moderate health impact
        - **Low Risk (<30)**: Products with minimal health concerns
        
        The chart shows the top 10 advertisers ranked by their health risk index, with color coding indicating product type.
        """)
    
    with tab2:
        # Show product type distribution
        product_counts = df['product_type'].value_counts()
        fig = px.pie(
            values=product_counts.values,
            names=product_counts.index,
            title="Distribution of Advertisers by Product Type",
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        # Add horizontal bar chart for product types
        fig2 = px.bar(
            x=product_counts.values,
            y=product_counts.index,
            orientation='h',
            title="Number of Advertisers by Product Type",
            labels={'x': 'Number of Advertisers', 'y': 'Product Type'}
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        # Show detailed table with sorting and filtering
        st.dataframe(
            df[['brand_name', 'product_type', 'social_risk_description', 'celebrity_influence']],
            use_container_width=True,
            hide_index=True
        )
    
    # Show detailed metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Brands Analyzed",
            len(df)
        )
    
    with col2:
        high_risk_brands = len(df[df['health_risk_index'] > 70])
        st.metric(
            "High Risk Brands",
            high_risk_brands,
            f"{high_risk_brands/len(df)*100:.1f}% of total"
        )
    
    with col3:
        st.metric(
            "Unique Product Types",
            len(df['product_type'].unique())
        )
    
    # Add insights and recommendations
    st.markdown("""
    ### Key Insights
    1. **Product Category Distribution**:
       - High concentration of FMCG and Fantasy Gaming advertisers
       - Significant presence of Pan Masala/Mouth Freshener brands
    
    2. **Risk Patterns**:
       - Fantasy Gaming shows highest risk due to gambling concerns
       - Pan Masala brands pose health risks through surrogate advertising
       - FMCG products show moderate risk levels
    
    3. **Celebrity Influence**:
       - High celebrity involvement in risky product categories
       - Strong correlation between celebrity influence and brand visibility
    
    ### Recommendations
    1. **Policy Changes**:
       - Implement stricter guidelines for surrogate advertising
       - Review and update advertising policies for high-risk categories
    
    2. **Brand Selection**:
       - Prioritize low-risk brands for sponsorship
       - Implement risk assessment framework for new advertisers
    
    3. **Celebrity Guidelines**:
       - Develop clear guidelines for celebrity endorsements
       - Encourage responsible celebrity-brand associations
    """)

def show_population_impact():
    """Show population impact analysis."""
    st.header("Population Impact Analysis")
    
    # Add documentation
    st.markdown("""
    ### Understanding Population Impact
    This section analyzes the potential impact of IPL advertising on the population. The analysis includes:
    - Distribution of health risk scores across brands
    - Number of high-risk brands and their impact
    - Risk categories and their definitions
    - Overall risk assessment metrics
    """)
    
    results = load_results()
    if not results:
        st.error("No analysis results found. Please run the analysis first.")
        return
    
    impact_data = results['population_impact']
    health_risk_data = results['health_risk']
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Impact Overview", "Risk Distribution"])
    
    with tab1:
        # Create metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Brands Analyzed",
                len(health_risk_data)
            )
        
        with col2:
            high_risk_brands = len([brand for brand in health_risk_data if brand['health_risk_index'] > 70])
            st.metric(
                "High Risk Brands",
                high_risk_brands,
                f"{high_risk_brands/len(health_risk_data)*100:.1f}% of total"
            )
        
        with col3:
            # Convert average_risk_score to float if it's a string
            try:
                avg_risk = float(impact_data['average_risk_score'])
                risk_display = f"{avg_risk:.1f}"
            except (ValueError, TypeError):
                risk_display = "N/A"
            
            st.metric(
                "Average Risk Score",
                risk_display
            )
    
    with tab2:
        # Create risk distribution chart
        df = pd.DataFrame(health_risk_data)
        
        # Convert health_risk_index to numeric if it's not already
        df['health_risk_index'] = pd.to_numeric(df['health_risk_index'], errors='coerce')
        
        # Create histogram
        fig = px.histogram(
            df,
            x='health_risk_index',
            nbins=10,
            title="Distribution of Health Risk Scores",
            labels={'health_risk_index': 'Health Risk Index', 'count': 'Number of Brands'},
            color_discrete_sequence=['#2ecc71']
        )
        fig.update_layout(
            xaxis_title="Health Risk Index",
            yaxis_title="Number of Brands",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Add box plot for risk distribution
        fig2 = px.box(
            df,
            y='health_risk_index',
            title="Health Risk Score Distribution",
            labels={'health_risk_index': 'Health Risk Index'}
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Show risk categories
    st.subheader("Risk Categories")
    risk_categories = {
        "Low Risk": "Health Risk Index < 30",
        "Medium Risk": "Health Risk Index 30-70",
        "High Risk": "Health Risk Index > 70"
    }
    
    for category, description in risk_categories.items():
        st.info(f"**{category}**: {description}")
    
    # Add summary statistics
    st.subheader("Summary Statistics")
    if not df['health_risk_index'].empty:
        stats = df['health_risk_index'].describe()
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Minimum Risk", f"{stats['min']:.1f}")
        with col2:
            st.metric("Average Risk", f"{stats['mean']:.1f}")
        with col3:
            st.metric("Median Risk", f"{stats['50%']:.1f}")
        with col4:
            st.metric("Maximum Risk", f"{stats['max']:.1f}")
    
    # Add insights and recommendations
    st.markdown("""
    ### Key Insights
    1. **Risk Distribution**:
       - Wide range of risk scores across different brands
       - Significant number of brands in high-risk category
       - Clear correlation between product type and risk level
    
    2. **Impact Assessment**:
       - High-risk brands have significant market presence
       - Multiple brands targeting similar demographics
       - Cumulative effect of multiple high-risk advertisers
    
    3. **Market Dynamics**:
       - Strong presence of surrogate advertising
       - High concentration of risky products in certain categories
       - Need for better risk management
    
    ### Recommendations
    1. **Regulatory Framework**:
       - Implement stricter advertising guidelines
       - Regular monitoring of surrogate advertising
       - Clear categorization of high-risk products
    
    2. **Brand Management**:
       - Develop risk mitigation strategies
       - Regular risk assessment of advertisers
       - Balance between revenue and social responsibility
    
    3. **Consumer Protection**:
       - Enhanced disclosure requirements
       - Clear labeling of high-risk products
       - Public awareness campaigns
    """)

def show_celebrity_endorsements():
    """Show celebrity endorsement analysis."""
    st.header("Celebrity Endorsement Analysis")
    
    # Add documentation
    st.markdown("""
    ### Understanding Celebrity Endorsements
    This section analyzes the relationship between celebrities and brand endorsements. The analysis includes:
    - Top celebrities by number of brand endorsements
    - Brands with the most celebrity endorsements
    - Risk assessment of celebrity-endorsed brands
    - Impact of celebrity influence on brand perception
    """)
    
    results = load_results()
    if not results:
        st.error("No analysis results found. Please run the analysis first.")
        return
    
    health_risk_data = results['health_risk']
    if not health_risk_data:
        st.info("No celebrity endorsement data available.")
        return
    
    # Process celebrity data
    celebrity_data = []
    for brand in health_risk_data:
        if brand['celebrity_name'] and brand['celebrity_name'] != 'multiple':
            celebrities = [c.strip() for c in brand['celebrity_name'].split(',')]
            for celebrity in celebrities:
                celebrity_data.append({
                    'celebrity_name': celebrity,
                    'brand_name': brand['brand_name'],
                    'product_type': brand['product_type'],
                    'health_risk_index': brand['health_risk_index']
                })
    
    if not celebrity_data:
        st.info("No celebrity endorsement data available.")
        return
    
    df = pd.DataFrame(celebrity_data)
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Celebrity Analysis", "Brand Analysis", "Risk Analysis"])
    
    with tab1:
        # Count endorsements per celebrity
        celebrity_counts = df['celebrity_name'].value_counts().reset_index()
        celebrity_counts.columns = ['celebrity_name', 'brand_count']
        
        # Calculate average risk per celebrity
        avg_risk = df.groupby('celebrity_name')['health_risk_index'].mean().reset_index()
        celebrity_counts = celebrity_counts.merge(avg_risk, on='celebrity_name')
        
        # Create visualization
        fig = px.bar(
            celebrity_counts.head(10),
            x='celebrity_name',
            y='brand_count',
            color='health_risk_index',
            title="Top 10 Celebrities by Number of Brand Endorsements",
            labels={
                'celebrity_name': 'Celebrity',
                'brand_count': 'Number of Brands',
                'health_risk_index': 'Average Risk Score'
            }
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            height=500,
            margin=dict(t=50, b=100, l=50, r=50)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Show brand distribution
        brand_counts = df['brand_name'].value_counts().reset_index()
        brand_counts.columns = ['brand_name', 'celebrity_count']
        
        fig = px.bar(
            brand_counts.head(10),
            x='brand_name',
            y='celebrity_count',
            title="Top 10 Brands by Number of Celebrity Endorsements",
            labels={
                'brand_name': 'Brand',
                'celebrity_count': 'Number of Celebrities'
            }
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            height=500,
            margin=dict(t=50, b=100, l=50, r=50)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Enhanced scatter plot for celebrity endorsements vs risk score
        fig = px.scatter(
            celebrity_counts,
            x='brand_count',
            y='health_risk_index',
            hover_data=['celebrity_name'],
            title="Celebrity Endorsements vs Risk Score",
            labels={
                'brand_count': 'Number of Brand Endorsements',
                'health_risk_index': 'Average Risk Score'
            },
            color='health_risk_index',  # Color by risk score
            size='brand_count',  # Size by number of endorsements
            color_continuous_scale='RdYlGn_r',  # Red to green color scale
            size_max=20  # Maximum bubble size
        )
        
        # Enhance the layout
        fig.update_layout(
            height=600,
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                title_font=dict(size=14),
                tickfont=dict(size=12),
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title_font=dict(size=14),
                tickfont=dict(size=12),
                gridcolor='lightgray'
            ),
            title=dict(
                font=dict(size=20),
                x=0.5,
                y=0.95
            ),
            coloraxis_colorbar=dict(
                title="Risk Score",
                titleside="right"
            )
        )
        
        # Add risk level annotations
        fig.add_shape(
            type="rect",
            xref="paper", yref="y",
            x0=0, y0=70,
            x1=1, y1=100,
            fillcolor="red",
            opacity=0.1,
            layer="below",
            line_width=0
        )
        
        fig.add_shape(
            type="rect",
            xref="paper", yref="y",
            x0=0, y0=30,
            x1=1, y1=70,
            fillcolor="yellow",
            opacity=0.1,
            layer="below",
            line_width=0
        )
        
        fig.add_shape(
            type="rect",
            xref="paper", yref="y",
            x0=0, y0=0,
            x1=1, y1=30,
            fillcolor="green",
            opacity=0.1,
            layer="below",
            line_width=0
        )
        
        # Add risk level labels
        fig.add_annotation(
            xref="paper", yref="y",
            x=0.02, y=85,
            text="High Risk",
            showarrow=False,
            font=dict(color="red", size=12)
        )
        
        fig.add_annotation(
            xref="paper", yref="y",
            x=0.02, y=50,
            text="Medium Risk",
            showarrow=False,
            font=dict(color="orange", size=12)
        )
        
        fig.add_annotation(
            xref="paper", yref="y",
            x=0.02, y=15,
            text="Low Risk",
            showarrow=False,
            font=dict(color="green", size=12)
        )
        
        # Add trend line
        fig.add_traces(
            px.scatter(
                celebrity_counts,
                x='brand_count',
                y='health_risk_index',
                trendline="ols"
            ).data[1]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add explanation of the visualization
        st.markdown("""
        **Understanding the Celebrity Endorsement Analysis:**
        - **Bubble Size**: Represents the number of brand endorsements
        - **Color**: Indicates the average risk score (red = high risk, green = low risk)
        - **Trend Line**: Shows the relationship between number of endorsements and risk score
        
        The scatter plot helps identify patterns in celebrity endorsements and their association with brand risk levels.
        """)
    
    # Show detailed metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Celebrities",
            len(df['celebrity_name'].unique())
        )
    
    with col2:
        st.metric(
            "Total Brands",
            len(df['brand_name'].unique())
        )
    
    with col3:
        st.metric(
            "Average Risk Score",
            f"{df['health_risk_index'].mean():.1f}"
        )
    
    # Add insights and recommendations
    st.markdown("""
    ### Key Insights
    1. **Celebrity-Brand Relationships**:
       - High concentration of endorsements among top celebrities
       - Strong correlation between celebrity popularity and brand risk
       - Multiple endorsements per celebrity common
    
    2. **Risk Patterns**:
       - Celebrities often endorse multiple high-risk brands
       - Clear relationship between celebrity influence and brand risk
       - Need for better risk assessment in celebrity selection
    
    3. **Market Impact**:
       - Celebrity endorsements significantly impact brand visibility
       - High-risk brands leverage celebrity influence
       - Need for responsible celebrity-brand associations
    
    ### Recommendations
    1. **Celebrity Guidelines**:
       - Develop clear guidelines for celebrity endorsements
       - Implement risk assessment for celebrity-brand partnerships
       - Encourage responsible celebrity choices
    
    2. **Brand Strategy**:
       - Balance celebrity influence with brand risk
       - Focus on long-term brand health over short-term gains
       - Develop alternative marketing strategies
    
    3. **Industry Standards**:
       - Create industry-wide guidelines for celebrity endorsements
       - Regular monitoring of celebrity-brand associations
       - Public awareness about responsible endorsements
    """)

def main():
    st.title("IPL Economic and Social Impact Analysis")
    
    # Create sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Revenue Analysis", "Health Risk Analysis", 
         "Population Impact", "Celebrity Endorsements"]
    )
    
    # Show selected page
    if page == "Revenue Analysis":
        show_revenue_analysis()
    elif page == "Health Risk Analysis":
        show_health_risk_analysis()
    elif page == "Population Impact":
        show_population_impact()
    elif page == "Celebrity Endorsements":
        show_celebrity_endorsements()

if __name__ == "__main__":
    main() 