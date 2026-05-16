import pandas as pd
import numpy as np

# Load source file
raw = pd.read_excel('Untitled-spreadsheet.xlsx', sheet_name='Sheet1', header=1)
raw.columns = [str(c).strip() for c in raw.columns]

df = raw.rename(columns={
    'MONTH':'Month',
    'ZONE MAPPING':'Zone',
    'KITCHEN EBITDA':'EBITDA',
    'REVENUE COHORT':'Revenue Cohort',
    'CM COHORT':'CM Cohort',
    'EBITDA CATEGORY':'EBITDA Category',
    'EBITDA COHORT':'EBITDA Cohort'
})

num_cols = ['ORDER COUNT','CART SALES','DISCOUNT','NET REVENUE','IDEAL FOOD COST','GROSS MARGIN','EBITDA','VARIANCE']
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

df['CM'] = df['GROSS MARGIN'] - df['DISCOUNT']
df['GM%'] = df['GROSS MARGIN'] / df['NET REVENUE'] * 100
df['CM%'] = df['CM'] / df['NET REVENUE'] * 100
df['Variance %'] = df['VARIANCE'] / df['NET REVENUE'] * 100

bins = [0,1500000,2500000,3500000,4500000,float('inf')]
labels = ['Below INR 15 lacs','INR 15 to 25 lacs','INR 25 to 35 lacs','INR 35 to 45 lacs','Above INR 45 lacs']
df['Revenue Band'] = pd.cut(df['NET REVENUE'], bins=bins, labels=labels, right=False, include_lowest=True)

def var_bucket(x):
    if x < 2:
        return 'Var < 2%'
    elif x < 3:
        return 'Var 2% to 3%'
    elif x < 5:
        return 'Var 3% to 5%'
    return 'Var > 5%'

df['Variance Bucket'] = df['Variance %'].apply(var_bucket)
df.to_csv('cleaned_kitchen_pnl.csv', index=False)

variance_avg = df.groupby(['Revenue Band','Month'], observed=True)['Variance %'].mean().reset_index()
variance_count = df.groupby(['Variance Bucket','Revenue Band','Month'], observed=True)['STORE'].nunique().reset_index(name='Store Count')

variance_avg.to_csv('variance_avg_by_revenue.csv', index=False)
variance_count.to_csv('variance_storecount_by_month.csv', index=False)
