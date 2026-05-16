
Data Analyst Case Study Submission : 

Deliverables
    app.py -  Full Streamlit dashboard submission
    analysis.py -  Dataset preparation / analysis script
    cleaned_kitchen_pnl.csv -  Cleaned input dataset
    variance_avg_by_revenue.csv -  Sub- dashboard 1 summary
    variance_storecount_by_month.csv -  Sub- dashboard 2 summary
    requirements.txt -  Python and package versions

Python Version
    Python 3.12

Packages
    See requirements.txt

Run Instructions
    pip install -r requirements.txt
    streamlit run output/app.py

Dashboard Coverage : 
    1. Kitchen Level PNL dashboard with filters for store, month, cohorts, EBITDA category,
        and range filters. 
    2. Variance Level PNL with:
        1. Average variance % by revenue category
        2. Store count by variance bucket, revenue band, and month
    3. Extra insights tab for city and month performance.
    4. Performance optimization via st.cache_data.

Note :
    Performance optimization used: st.cache_data for dataset loading and pre-aggregation-friendly 
    transformations to support real-time refresh scenarios.

