# IPL Economic and Social Impact Analysis

This project analyzes the economic and social impact of the Indian Premier League (IPL), focusing on advertising practices, revenue generation, and their implications on public health and society.

## Setup and Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Data Sources

The project uses the following datasets:
- fact_ipl_advertisers.xlsx
- fact_revenue_demography.xlsx
- fact_summary_demography.xlsx
- fact_ipl_central_contracts.xlsx

## Analysis Components

### Primary Analysis
1. IPL Revenue Analysis from Central Contracts (2025)
2. Health/Social Risk Index for Top Advertising Brands
3. CAGR Projection Analysis (2025-2030)
4. Population Impact Assessment
5. Celebrity Endorsement Analysis

### Secondary Analysis
1. Public Health Implications
2. Economic Ecosystem Analysis

## Dashboard Features

The Streamlit dashboard includes:
1. Balanced Scorecard for IPL Advertisers
2. Advertising Ethics Index (AEI)
3. Economic Benefits Framework
4. Responsible Advertising Policy
5. Player Endorsement Strategy Recommendations

## Running the Project

1. Data Processing:
```bash
python src/data/process_data.py
```

2. Run Analysis:
```bash
python src/analysis/main_analysis.py
```

3. Launch Dashboard:
```bash
streamlit run src/dashboard/app.py
```

## Contributing

Please read the project guidelines before contributing.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 