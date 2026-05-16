
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Cloud Kitchen PNL Dashboard", layout="wide")

@st.cache_data(ttl=3600, show_spinner=False)
def load_data():
    df = pd.read_csv('cleaned_kitchen_pnl.csv')
    num_cols = ['ORDER COUNT','CART SALES','DISCOUNT','NET REVENUE','IDEAL FOOD COST','GROSS MARGIN','EBITDA','VARIANCE','CM','GM%','CM%','Variance %']
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    month_order = ['Oct-2023','Nov-2023','Dec-2023','Jan-2024','Feb-2024','Mar-2024']
    df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)
    return df

def fmt_inr(x):
    if pd.isna(x):
        return '-'
    return f"₹{x:,.0f}"

def fmt_pct(x):
    if pd.isna(x):
        return '-'
    return f"{x:.2f}%"

def build_multiselect(label, series, key):
    vals = sorted([v for v in series.dropna().unique().tolist()])
    return st.multiselect(label, vals, key=key)

df = load_data()

st.title('Cloud Kitchen PNL Dashboard')
st.caption('Streamlit dashboard for Kitchen Level PNL and Variance Level PNL analysis.')

with st.sidebar:
    st.header('Global Filters')
    month_sel = build_multiselect('Month', df['Month'].astype(str), 'month_sel')
    city_sel = build_multiselect('City', df['CITY'], 'city_sel')
    zone_sel = build_multiselect('Zone', df['Zone'], 'zone_sel')
    status_sel = build_multiselect('Status', df['STATUS'], 'status_sel')
    store_sel = build_multiselect('Store', df['STORE'], 'store_sel')
    rev_cohort_sel = build_multiselect('Revenue Cohort', df['Revenue Cohort'], 'rev_cohort_sel')
    cm_cohort_sel = build_multiselect('CM Cohort', df['CM Cohort'], 'cm_cohort_sel')
    ebitda_cat_sel = build_multiselect('EBITDA Category', df['EBITDA Category'], 'ebitda_cat_sel')
    ebitda_cohort_sel = build_multiselect('EBITDA Cohort', df['EBITDA Cohort'], 'ebitda_cohort_sel')

    rev_min, rev_max = float(df['NET REVENUE'].min()), float(df['NET REVENUE'].max())
    cm_min, cm_max = float(df['CM'].min()), float(df['CM'].max())
    e_min, e_max = float(df['EBITDA'].min()), float(df['EBITDA'].max())
    variance_bucket_sel = st.multiselect('Variance Category', sorted(df['Variance Bucket'].dropna().unique()), default=sorted(df['Variance Bucket'].dropna().unique()))
    revenue_range = st.slider('Revenue Range', min_value=float(rev_min), max_value=float(rev_max), value=(float(rev_min), float(rev_max)))
    cm_range = st.slider('CM Range', min_value=float(cm_min), max_value=float(cm_max), value=(float(cm_min), float(cm_max)))
    ebitda_range = st.slider('EBITDA Range', min_value=float(e_min), max_value=float(e_max), value=(float(e_min), float(e_max)))

filtered = df.copy()
for col, vals in [
    ('Month', month_sel), ('CITY', city_sel), ('Zone', zone_sel), ('STATUS', status_sel), ('STORE', store_sel),
    ('Revenue Cohort', rev_cohort_sel), ('CM Cohort', cm_cohort_sel), ('EBITDA Category', ebitda_cat_sel), ('EBITDA Cohort', ebitda_cohort_sel)
]:
    if vals:
        filtered = filtered[filtered[col].astype(str).isin([str(v) for v in vals])]

filtered = filtered[
    filtered['Variance Bucket'].isin(variance_bucket_sel)
    & filtered['NET REVENUE'].between(revenue_range[0], revenue_range[1])
    & filtered['CM'].between(cm_range[0], cm_range[1])
    & filtered['EBITDA'].between(ebitda_range[0], ebitda_range[1])
]

if filtered.empty:
    st.warning('No data found for the selected filters.')
    st.stop()

k1,k2,k3,k4,k5 = st.columns(5)
k1.metric('Stores', filtered['STORE'].nunique())
k2.metric('Net Revenue', fmt_inr(filtered['NET REVENUE'].sum()))
k3.metric('Gross Margin', fmt_inr(filtered['GROSS MARGIN'].sum()))
k4.metric('EBITDA', fmt_inr(filtered['EBITDA'].sum()))
k5.metric('Average Variance %', fmt_pct(filtered['Variance %'].mean()))

tab1, tab2, tab3 = st.tabs(['Kitchen Level PNL', 'Variance Level PNL', 'Insights'])

with tab1:
    st.subheader('Kitchen Snapshot')
    kitchen_tbl = filtered[['Month','CITY','STORE','STATUS','Zone','NET REVENUE','GROSS MARGIN','GM%','CM','CM%','EBITDA','Variance %','Revenue Cohort','CM Cohort','EBITDA Category','EBITDA Cohort']].copy()
    kitchen_tbl = kitchen_tbl.sort_values(['Month','CITY','STORE'])
    st.dataframe(kitchen_tbl, use_container_width=True, height=420)

    c1, c2 = st.columns(2)
    with c1:
        rev_month = filtered.groupby('Month', observed=True, as_index=False)['NET REVENUE'].sum()
        fig1 = px.bar(rev_month, x='Month', y='NET REVENUE', title='Net Revenue by Month', text_auto='.2s', color='NET REVENUE', color_continuous_scale='Teal')
        fig1.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        ebitda_month = filtered.groupby('Month', observed=True, as_index=False)['EBITDA'].sum()
        fig2 = px.line(ebitda_month, x='Month', y='EBITDA', title='EBITDA Trend by Month', markers=True)
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        top_store = filtered.groupby('STORE', as_index=False)['NET REVENUE'].sum().sort_values('NET REVENUE', ascending=False).head(10)
        fig3 = px.bar(top_store, x='NET REVENUE', y='STORE', orientation='h', title='Top 10 Stores by Net Revenue', text_auto='.2s')
        fig3.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig3, use_container_width=True)
    with c4:
        cohort_perf = filtered.groupby('Revenue Cohort', as_index=False).agg({'NET REVENUE':'sum','EBITDA':'sum'})
        fig4 = px.scatter(cohort_perf, x='NET REVENUE', y='EBITDA', size='NET REVENUE', color='Revenue Cohort', title='Revenue Cohort vs EBITDA')
        st.plotly_chart(fig4, use_container_width=True)

with tab2:
    st.subheader('Variance Level PNL')
    st.markdown('### Sub-dashboard 1: Average Variance % by Revenue Category')
    var_avg = filtered.groupby(['Revenue Band','Month'], observed=True)['Variance %'].mean().reset_index()
    pivot_avg = var_avg.pivot(index='Revenue Band', columns='Month', values='Variance %').reset_index()
    st.dataframe(pivot_avg, use_container_width=True)
    fig5 = px.line(var_avg, x='Month', y='Variance %', color='Revenue Band', markers=True, title='Average Variance % across Revenue Bands')
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown('### Sub-dashboard 2: Store Count by Variance Bucket, Revenue Band and Month')
    var_count = filtered.groupby(['Variance Bucket','Revenue Band','Month'], observed=True)['STORE'].nunique().reset_index(name='Store Count')
    sel_bucket = st.selectbox('Select Variance Bucket for Store Count View', sorted(filtered['Variance Bucket'].dropna().unique()))
    var_count_f = var_count[var_count['Variance Bucket'] == sel_bucket]
    pivot_count = var_count_f.pivot(index='Revenue Band', columns='Month', values='Store Count').fillna(0).reset_index()
    st.dataframe(pivot_count, use_container_width=True)
    fig6 = px.bar(var_count_f, x='Month', y='Store Count', color='Revenue Band', barmode='group', title=f'Store Count for {sel_bucket}')
    st.plotly_chart(fig6, use_container_width=True)

with tab3:
    st.subheader('Additional Insights')
    i1, i2 = st.columns(2)
    with i1:
        city_perf = filtered.groupby('CITY', as_index=False).agg({'NET REVENUE':'sum','EBITDA':'sum','STORE':'nunique'})
        city_perf = city_perf.rename(columns={'STORE':'Store Count'})
        st.dataframe(city_perf.sort_values('NET REVENUE', ascending=False), use_container_width=True)
    with i2:
        best_month = filtered.groupby('Month', observed=True).agg({'NET REVENUE':'sum','EBITDA':'sum','Variance %':'mean'}).reset_index()
        fig7 = make_subplots(specs=[[{"secondary_y": True}]])
        fig7.add_trace(go.Bar(x=best_month['Month'], y=best_month['NET REVENUE'], name='Net Revenue'), secondary_y=False)
        fig7.add_trace(go.Scatter(x=best_month['Month'], y=best_month['Variance %'], name='Variance %', mode='lines+markers'), secondary_y=True)
        fig7.update_layout(title='Revenue and Variance % by Month')
        fig7.update_yaxes(title_text='Net Revenue', secondary_y=False)
        fig7.update_yaxes(title_text='Variance %', secondary_y=True)
        st.plotly_chart(fig7, use_container_width=True)

    st.markdown('#### Observations')
    top_city = filtered.groupby('CITY')['NET REVENUE'].sum().sort_values(ascending=False).index[0]
    top_month = filtered.groupby('Month', observed=True)['NET REVENUE'].sum().sort_values(ascending=False).index[0]
    low_var_band = filtered.groupby('Revenue Band', observed=True)['Variance %'].mean().sort_values().index[0]
    st.write(f'- Highest net revenue in current filter selection comes from **{top_city}**.')
    st.write(f'- Best month by net revenue is **{top_month}**.')
    st.write(f'- Lowest average variance % appears in **{low_var_band}** revenue band.')
