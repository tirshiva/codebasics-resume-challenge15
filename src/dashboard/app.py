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
    page_title="IPL Impact Analysis",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern look with better contrast
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    .stMarkdown {
        padding: 1rem 0;
        color: #2c3e50;
    }
    .question-box {
        background-color: #e9ecef;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #2c3e50;
        border-left: 5px solid #3498db;
    }
    .answer-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #3498db;
        color: #2c3e50;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-box {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #2c3e50;
    }
    .highlight {
        color: #2980b9;
        font-weight: bold;
    }
    h1, h2, h3, h4 {
        color: #2c3e50 !important;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #2980b9;
    }
    .stMetric [data-testid="stMetricLabel"] {
        color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)

def load_results():
    """Load analysis results."""
    results_path = Path("results/analysis_results.json")
    if results_path.exists():
        with open(results_path) as f:
            return json.load(f)
    return None

def create_revenue_charts(revenue_data):
    """Create basic revenue visualization charts."""
    # Bar chart for revenue by source
    fig_bar = go.Figure(data=[
        go.Bar(
            x=list(revenue_data['revenue_by_source'].keys()),
            y=list(revenue_data['revenue_by_source'].values()),
            text=[f'₹{v:,.0f} Cr' for v in revenue_data['revenue_by_source'].values()],
            textposition='auto',
            marker_color='#2980b9',
            textfont=dict(color='#2c3e50', size=12)
        )
    ])
    
    fig_bar.update_layout(
        title="Revenue by Source (2025)",
        xaxis_title="Revenue Source",
        yaxis_title="Revenue (Crores)",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50'),
        xaxis=dict(tickangle=-45, tickfont=dict(color='#2c3e50')),
        yaxis=dict(tickfont=dict(color='#2c3e50')),
        titlefont=dict(color='#2c3e50', size=16)
    )
    
    # Pie chart for revenue distribution
    fig_pie = go.Figure(data=[go.Pie(
        labels=list(revenue_data['revenue_percentage'].keys()),
        values=list(revenue_data['revenue_percentage'].values()),
        hole=.4,
        marker=dict(colors=px.colors.qualitative.Set3),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(color='#2c3e50', size=12)
    )])
    
    fig_pie.update_layout(
        title="Revenue Distribution by Source (2025)",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50'),
        titlefont=dict(color='#2c3e50', size=16)
    )
    
    return fig_bar, fig_pie

def create_health_risk_charts(df):
    """Create basic health risk visualization charts."""
    # Bar chart for top 10 risky brands
    fig_bar = go.Figure(data=[
        go.Bar(
            x=df.head(10)['brand_name'],
            y=df.head(10)['health_risk_index'],
            text=df.head(10)['health_risk_index'].round(1),
            textposition='auto',
            marker_color='#c0392b',
            textfont=dict(color='#2c3e50', size=12)
        )
    ])
    
    fig_bar.update_layout(
        title="Top 10 Advertisers by Health Risk Index",
        xaxis_title="Brand Name",
        yaxis_title="Health Risk Index",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50'),
        xaxis=dict(tickangle=-45, tickfont=dict(color='#2c3e50')),
        yaxis=dict(tickfont=dict(color='#2c3e50')),
        titlefont=dict(color='#2c3e50', size=16)
    )
    
    # Histogram for risk distribution
    fig_hist = go.Figure(data=[
        go.Histogram(
            x=df['health_risk_index'],
            nbinsx=10,
            marker_color='#27ae60',
            textfont=dict(color='#2c3e50', size=12)
        )
    ])
    
    fig_hist.update_layout(
        title="Distribution of Health Risk Scores",
        xaxis_title="Health Risk Index",
        yaxis_title="Number of Brands",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50'),
        xaxis=dict(tickfont=dict(color='#2c3e50')),
        yaxis=dict(tickfont=dict(color='#2c3e50')),
        titlefont=dict(color='#2c3e50', size=16)
    )
    
    return fig_bar, fig_hist

def create_population_impact_charts(df):
    """Create basic population impact visualization charts."""
    # Box plot for risk scores
    fig_box = go.Figure(data=[
        go.Box(
            y=df['health_risk_index'],
            name="Health Risk Index",
            marker_color='#8e44ad',
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            textfont=dict(color='#2c3e50', size=12)
        )
    ])
    
    fig_box.update_layout(
        title="Health Risk Score Distribution",
        yaxis_title="Health Risk Index",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50'),
        xaxis=dict(tickfont=dict(color='#2c3e50')),
        yaxis=dict(tickfont=dict(color='#2c3e50')),
        titlefont=dict(color='#2c3e50', size=16)
    )
    
    # Scatter plot for risk vs product type
    fig_scatter = go.Figure(data=[
        go.Scatter(
            x=df['product_type'],
            y=df['health_risk_index'],
            mode='markers',
            marker=dict(
                size=10,
                color=df['health_risk_index'],
                colorscale='RdYlGn_r',
                showscale=True,
                colorbar=dict(
                    title="Risk Score",
                    titleside="right",
                    titlefont=dict(color='#2c3e50'),
                    tickfont=dict(color='#2c3e50')
                )
            ),
            text=df['brand_name'],
            textposition="top center",
            textfont=dict(color='#2c3e50', size=10)
        )
    ])
    
    fig_scatter.update_layout(
        title="Health Risk by Product Type",
        xaxis_title="Product Type",
        yaxis_title="Health Risk Index",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50'),
        xaxis=dict(tickangle=-45, tickfont=dict(color='#2c3e50')),
        yaxis=dict(tickfont=dict(color='#2c3e50')),
        titlefont=dict(color='#2c3e50', size=16)
    )
    
    return fig_box, fig_scatter

def create_celebrity_charts(df_celebrity):
    """Create basic celebrity endorsement visualization charts."""
    # Bar chart for celebrity endorsements
    fig_bar = go.Figure(data=[
        go.Bar(
            x=df_celebrity['celebrity_name'],
            y=df_celebrity['brand_count'],
            text=df_celebrity['brand_count'],
            textposition='auto',
            marker_color='#d35400',
            textfont=dict(color='#2c3e50', size=12)
        )
    ])
    
    fig_bar.update_layout(
        title="Number of Brand Endorsements by Celebrity",
        xaxis_title="Celebrity Name",
        yaxis_title="Number of Endorsements",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50'),
        xaxis=dict(tickangle=-45, tickfont=dict(color='#2c3e50')),
        yaxis=dict(tickfont=dict(color='#2c3e50')),
        titlefont=dict(color='#2c3e50', size=16)
    )
    
    # Scatter plot for risk vs endorsements
    fig_scatter = go.Figure(data=[
        go.Scatter(
            x=df_celebrity['brand_count'],
            y=df_celebrity['health_risk_index'],
            mode='markers+text',
            marker=dict(
                size=10,
                color=df_celebrity['health_risk_index'],
                colorscale='RdYlGn_r',
                showscale=True,
                colorbar=dict(
                    title="Risk Score",
                    titleside="right",
                    titlefont=dict(color='#2c3e50'),
                    tickfont=dict(color='#2c3e50')
                )
            ),
            text=df_celebrity['celebrity_name'],
            textposition="top center",
            textfont=dict(color='#2c3e50', size=10)
        )
    ])
    
    fig_scatter.update_layout(
        title="Celebrity Endorsements vs Risk Score",
        xaxis_title="Number of Endorsements",
        yaxis_title="Average Risk Score",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50'),
        xaxis=dict(tickfont=dict(color='#2c3e50')),
        yaxis=dict(tickfont=dict(color='#2c3e50')),
        titlefont=dict(color='#2c3e50', size=16)
    )
    
    return fig_bar, fig_scatter

def main():
    # Title and Introduction
    st.markdown("""
    <h1 style='color: #2c3e50;'>IPL Impact Analysis: Key Questions & Answers</h1>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style='color: #2c3e50;'>
    This analysis explores the economic and social impact of the Indian Premier League (IPL),
    addressing key questions about revenue generation, health risks, and social implications.
    </p>
    """, unsafe_allow_html=True)
    
    # Load results
    results = load_results()
    if not results:
        st.error("No analysis results found. Please run the analysis first.")
        return
    
    # Primary Questions Section
    st.markdown("""
    <h2 style='color: #2c3e50;'>Primary Questions</h2>
    """, unsafe_allow_html=True)
    
    # Question 1: Revenue Generation
    st.markdown("""
    <div class="question-box">
        <h3 style='color: #2c3e50;'>1. How much revenue does IPL generate and what are its main sources?</h3>
    </div>
    """, unsafe_allow_html=True)
    
    revenue_data = results['central_contracts']
    
    # Create three columns for revenue metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric(
            "Total Revenue (2025)",
            f"₹{revenue_data['total_revenue']:,.0f} Cr",
            help="Total revenue from all sources in Crores"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        avg_revenue = revenue_data['total_revenue'] / len(revenue_data['revenue_by_source'])
        st.metric(
            "Average Revenue per Source",
            f"₹{avg_revenue:,.0f} Cr",
            help="Average revenue contribution per source"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        top_source = max(revenue_data['revenue_by_source'].items(), key=lambda x: x[1])
        st.metric(
            "Top Revenue Source",
            top_source[0],
            f"₹{top_source[1]:,.0f} Cr"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Create and display revenue charts
    fig_bar, fig_pie = create_revenue_charts(revenue_data)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("""
    <div class="answer-box">
        <h4 style='color: #2c3e50;'>Answer:</h4>
        <p style='color: #2c3e50;'>IPL generates substantial revenue primarily through media rights, with JioCinema and Star Sports 
        contributing over 92% of total revenue. The analysis shows:</p>
        <ul style='color: #2c3e50;'>
            <li>Total revenue of <span class="highlight">₹{total_revenue:,.0f} Crores</span> for 2025</li>
            <li>Average revenue of <span class="highlight">₹{avg_revenue:,.0f} Crores</span> per source</li>
            <li>Media rights dominate with <span class="highlight">{media_percentage:.1f}%</span> of total revenue</li>
            <li>Digital platforms (JioCinema) contribute <span class="highlight">{digital_percentage:.1f}%</span> of revenue</li>
        </ul>
    </div>
    """.format(
        total_revenue=revenue_data['total_revenue'],
        avg_revenue=avg_revenue,
        media_percentage=revenue_data['revenue_percentage'].get('JioCinema (Viacom18)', 0) + 
                        revenue_data['revenue_percentage'].get('Star Sports', 0),
        digital_percentage=revenue_data['revenue_percentage'].get('JioCinema (Viacom18)', 0)
    ), unsafe_allow_html=True)
    
    # Question 2: Health Risks
    st.markdown("""
    <div class="question-box">
        <h3 style='color: #2c3e50;'>2. What are the health risks associated with IPL advertising?</h3>
    </div>
    """, unsafe_allow_html=True)
    
    health_risk_data = results['health_risk']
    df = pd.DataFrame(health_risk_data)
    
    # Create and display health risk charts
    fig_bar, fig_hist = create_health_risk_charts(df)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_hist, use_container_width=True)
    
    st.markdown("""
    <div class="answer-box">
        <h4 style='color: #2c3e50;'>Answer:</h4>
        <p style='color: #2c3e50;'>The analysis reveals significant health risks in IPL advertising:</p>
        <ul style='color: #2c3e50;'>
            <li><span class="highlight">Fantasy Gaming and Pan Masala</span> brands show highest risk levels</li>
            <li><span class="highlight">{high_risk_count}</span> brands fall into the high-risk category</li>
            <li>Average risk score of <span class="highlight">{avg_risk:.1f}</span> across all advertisers</li>
            <li>Key risk categories:
                <ul>
                    <li>Gambling and betting promotion</li>
                    <li>Surrogate advertising for restricted products</li>
                    <li>High sugar content in FMCG products</li>
                </ul>
            </li>
        </ul>
    </div>
    """.format(
        high_risk_count=len(df[df['health_risk_index'] > 70]),
        avg_risk=df['health_risk_index'].mean()
    ), unsafe_allow_html=True)
    
    # Question 3: Population Impact
    st.markdown("""
    <div class="question-box">
        <h3 style='color: #2c3e50;'>3. How does IPL advertising affect the population?</h3>
    </div>
    """, unsafe_allow_html=True)
    
    impact_data = results['population_impact']
    
    # Create and display population impact charts
    fig_box, fig_scatter = create_population_impact_charts(df)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_box, use_container_width=True)
    with col2:
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("""
    <div class="answer-box">
        <h4 style='color: #2c3e50;'>Answer:</h4>
        <p style='color: #2c3e50;'>The population impact analysis shows:</p>
        <ul style='color: #2c3e50;'>
            <li>Wide range of risk scores across different brands</li>
            <li>Significant number of high-risk brands targeting similar demographics</li>
            <li>Clear correlation between product type and risk level</li>
            <li>Key demographic impacts:
                <ul>
                    <li>Youth exposure to gambling and betting</li>
                    <li>Children's exposure to high-sugar products</li>
                    <li>General population exposure to surrogate advertising</li>
                </ul>
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Question 4: Celebrity Impact
    st.markdown("""
    <div class="question-box">
        <h3 style='color: #2c3e50;'>4. How do celebrity endorsements affect brand perception?</h3>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    if celebrity_data:
        df_celebrity = pd.DataFrame(celebrity_data)
        celebrity_counts = df_celebrity['celebrity_name'].value_counts().reset_index()
        celebrity_counts.columns = ['celebrity_name', 'brand_count']
        
        # Calculate average risk per celebrity
        avg_risk = df_celebrity.groupby('celebrity_name')['health_risk_index'].mean().reset_index()
        celebrity_counts = celebrity_counts.merge(avg_risk, on='celebrity_name')
        
        # Create and display celebrity charts
        fig_bar, fig_scatter = create_celebrity_charts(celebrity_counts)
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("""
    <div class="answer-box">
        <h4 style='color: #2c3e50;'>Answer:</h4>
        <p style='color: #2c3e50;'>The celebrity endorsement analysis reveals:</p>
        <ul style='color: #2c3e50;'>
            <li>Strong correlation between celebrity influence and brand risk</li>
            <li>High concentration of endorsements among top celebrities</li>
            <li>Multiple endorsements per celebrity common in high-risk categories</li>
            <li>Key findings:
                <ul>
                    <li>Top celebrities endorsing high-risk products</li>
                    <li>Multiple brand associations per celebrity</li>
                    <li>Impact on brand perception and consumer trust</li>
                </ul>
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommendations Section
    st.markdown("""
    <h2 style='color: #2c3e50;'>Recommendations</h2>
    """, unsafe_allow_html=True)
    
    # Create four columns for recommendations
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-box">
            <h4 style='color: #2c3e50;'>Revenue Diversification</h4>
            <ul style='color: #2c3e50;'>
                <li>Develop non-media revenue streams</li>
                <li>Focus on sponsorship growth</li>
                <li>Explore digital monetization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-box">
            <h4 style='color: #2c3e50;'>Health Risk Management</h4>
            <ul style='color: #2c3e50;'>
                <li>Implement stricter guidelines</li>
                <li>Monitor surrogate advertising</li>
                <li>Categorize high-risk products</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-box">
            <h4 style='color: #2c3e50;'>Celebrity Guidelines</h4>
            <ul style='color: #2c3e50;'>
                <li>Develop endorsement policies</li>
                <li>Assess brand-celebrity fit</li>
                <li>Promote responsible choices</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-box">
            <h4 style='color: #2c3e50;'>Consumer Protection</h4>
            <ul style='color: #2c3e50;'>
                <li>Enhance disclosures</li>
                <li>Improve labeling</li>
                <li>Increase awareness</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 