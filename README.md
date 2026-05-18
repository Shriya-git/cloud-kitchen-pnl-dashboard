Live Project Link : https://cloud-kitchen-pnl-dashboard-8yxd8appmsv8ojgcxku7df5.streamlit.app/ 

Cloud Kitchen PNL Dashboard
Interactive Streamlit dashboard for cloud kitchen PNL analysis, variance tracking, and revenue insights built with Python, pandas, and Plotly.

Project Overview
This project was developed as a data analyst dashboard submission using Python, Streamlit, pandas, and Plotly. It combines data cleaning, KPI tracking, variance analysis, cohort-based filtering, and interactive business visualizations in one dashboard application. 

The dashboard is built on a cleaned kitchen PNL dataset and supports business users in monitoring store performance, revenue behavior, EBITDA trends, and variance distribution across revenue bands and months. 

Deliverables
app.py – Full Streamlit dashboard application. 
analysis.py – Dataset preparation and analysis script. 
cleaned_kitchen_pnl.csv – Cleaned dataset used by the dashboard. 
variance_avg_by_revenue.csv – Summary file for average variance by revenue band and month. 
variance_storecount_by_month.csv – Summary file for store count by variance bucket, revenue band, and month. 
requirements.txt – Package dependencies. 
Untitled-spreadsheet.xlsx – Source Excel input used for preprocessing. 
​

Dashboard Coverage
Kitchen Level PNL
Interactive filters for month, city, zone, status, store, revenue cohort, CM cohort, EBITDA category, and EBITDA cohort. 
Range filters for revenue, CM, and EBITDA. 
KPI cards for stores, net revenue, gross margin, EBITDA, and average variance percentage. 
Visual analysis for monthly revenue, EBITDA trend, top stores by revenue, and cohort performance. 
​

Variance Level PNL
Average variance percentage by revenue band and month. 
Store count by variance bucket, revenue band, and month. 
Interactive pivot tables and supporting charts for variance analysis. 
​

Insights
Additional insights tab focused on city and month performance. 
Optimized dashboard loading using st.cache_data. 

Data Preparation
The preprocessing logic in analysis.py reads the Excel source file, standardizes column names, converts numeric columns, and creates calculated business metrics such as CM, GM%, CM%, and Variance %. 
​

It also creates Revenue Band and Variance Bucket fields, then exports the cleaned dataset and variance summary CSV files used in the dashboard. 
​

Tech Stack
Python 3.12. 
pandas 2.2.3. 
NumPy 2.1.3. 
Plotly 5.24.1. 
Streamlit 1.41.1. 
openpyxl 3.1.5. 
​

Installation
Clone the repository and move into the project folder:

bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Install dependencies:

bash
pip install -r requirements.txt
Run Instructions
First, generate the cleaned dataset and summary files:

bash
python analysis.py
Then run the Streamlit dashboard:

bash
streamlit run app.py
These commands align with the current file structure because the dashboard reads cleaned_kitchen_pnl.csv directly from the project root rather than from an output/ folder. 

Project Structure
text
project-folder/
├── app.py
├── analysis.py
├── requirements.txt
├── README.md
├── README.txt
├── Untitled-spreadsheet.xlsx
├── cleaned_kitchen_pnl.csv
├── variance_avg_by_revenue.csv
└── variance_storecount_by_month.csv


Key Skills Demonstrated
Data cleaning and transformation using pandas. 
Business KPI and variance analysis. 
Interactive dashboard development in Streamlit. 
Data storytelling through charts, filters, and summary views. 
Performance optimization using cached data loading. 
