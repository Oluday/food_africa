
import streamlit as st
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import plotly.express as px


#import matplotlib.pyplot as plt

## load data

# page config
st.set_page_config(page_title="Bakery sales", layout='centered', page_icon='📊')

# Title
st.title (" 📊  Bakery sales - Web App")
@st.cache_data

def load_data():
    df = pd.read_csv("bakerysales.csv")
    # data cleaning
    df.drop(columns = 'Unnamed: 0', inplace=True)
    df['date'] = pd.to_datetime(df.date)
    df['ticket_number'] = df.ticket_number.astype('object')
    df['unit_price'] = df.unit_price.str.replace(',', '.').str.replace(' €', '')
    df['unit_price'] = df.unit_price.astype('float')
    # calculate sales
    sales = df.Quantity * df.unit_price

    # add a new column to the dataframe
    df['sales'] = sales
    # return cleaned dataframe
    return df


df = load_data()
#st.title("bakery sales App")
st.sidebar.title("filters")

# display the dataset

st.subheader("Data  Preview")
st.dataframe(df.head())

# create a filter for articles and ticket numbers
articles = df['article'].unique()

# get top10 ticketNos
ticketNos10 = df['ticket_number'].value_counts().head(10).reset_index()['ticket_number']
#st.write(df['ticket_number'].unique())

# create a multislect for articles
selected_articles = st.sidebar.multiselect("Products", articles,[articles[0],articles[10]])
top_10_ticketsNos = st.sidebar.selectbox("Top 10 Tickets", ticketNos10[:10])

#selected_ticketNos = st.
filtered_articles = df[df["article"].isin(selected_articles)]
no_filtered_articles = filtered_articles['article'].nunique()
total_filtered_sales = np.round(filtered_articles['sales'].sum(),2)
total_filtered_qty = np.round(filtered_articles['Quantity'].sum(),2)
st.subheader("Filtered sales_by_products")
if not selected_articles:
    st.error("select an article")
else:
    st.dataframe(filtered_articles.sample(3))

# calculations
total_sales = np.round(df['sales'].sum())
total_qty = np.round(df['Quantity'].sum())
no_articles = len(articles)

# display in columns
col1,col2,col3 = st.columns(3)
col1.metric("Total Sales",f'{total_sales:,}')
col2.metric("Total Quantity",f'{total_qty:,}')
col3.metric("No of articles",no_articles)
# quantity
if no_articles:
    col2.metric("Quantity", f'{total_qty:,}')
else:
    col2.metric("Quantity", f'{total_filtered_qty:,}')
if not selected_articles:
    col3.metric("No of products", no_articles)
else:
    col3.metric("No. of Products", no_filtered_articles)

#charts
st.header("Plotting")
# data
article_grp = df.groupby('article')['sales'].sum()
article_grp = article_grp.sort_values(ascending=False)[:-3]
table = article_grp.reset_index()

filtered_table = table[table['article'].isin(selected_articles)]

 #bar chart

article_sales = filtered_table.groupby('article')['sales'].mean().sort_values(ascending=False)
avg_sales_fig = px.bar(
    article_sales  ,
    x=article_sales.index,
    y="sales",
    title="<b>Average sales per article</b>",
    color_discrete_sequence=["#0083B8"] * len(article_sales  ),
    template="plotly_white"
)
avg_sales_fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(avg_sales_fig)






# pie chart
#percentages
st.subheader("Pie Chart")
grouped_sales = filtered_table.groupby('article')['sales'].sum().reset_index()
grouped_sales = grouped_sales.sort_values(by = 'sales', ascending = False)
mrkt_fig = px.pie(
    grouped_sales,
    names="article",
    values="sales",
    hover_data=['sales'],
    title="<b>Market Type</b>",
    template="plotly_white"
)
mrkt_fig.update_layout(
    plot_bgcolor="rgba(7,0,4,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(mrkt_fig)







st.subheader("Trend analysis")
daily_sales = df.groupby('date')['sales'].sum()
daily_sales  = px.line(
    daily_sales,
    x=daily_sales.index,
    y="sales",
    title="<b>Average price per country</b>",
    color_discrete_sequence=["#0083B8"] * len(daily_sales ),
    template="plotly_white",
)
daily_sales .update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(daily_sales )








sales_by_product = (
    filtered_table.groupby(by=["article"]).sum()[["sales"]].sort_values("sales")
    
)
sales_fig = px.bar(
    sales_by_product,
    x=sales_by_product.index,
    y="sales",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product),
    template="plotly_white"
)
sales_fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(sales_fig)