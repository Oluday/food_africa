import streamlit as st
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import plotly.express as px



# page config
st.set_page_config(layout='wide', initial_sidebar_state='expanded')





with st.form("My form"):
    first = st.text_input("First name")
    last = st.text_input("Last name")
    if st.form_submit_button("Submit"):
        st.write(first+" "+last)

css="""
<style>
    [data-testid="stForm"] {
        background: LightBlue;
    }
</style>
"""
st.write(css, unsafe_allow_html=True)
#with open('style.css') as f:
#    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



st.markdown(
    """
<style>
.css-nzvw1x {
    background-color: #061E42 !important;
    background-image: none !important;
}
.css-1aw8i8e {
    background-image: none !important;
    color: #FFFFFF !important
}
.css-ecnl2d {
    background-color: #496C9F !important;
    color: #496C9F !important
}
.css-15zws4i {
    background-color: #496C9F !important;
    color: #FFFFFF !important
}
</style>
""",
    unsafe_allow_html=True
)

# Title
#st.set_page_config(page_title="African food prices", layout='centered', page_icon='📊')
#(page_title="Africa food prices", layout='wide',initial_sidebar_state='expanded', page_icon='📊')

st.markdown("##")
@st.cache_data
def load_data():
    df = pd.read_csv("africa_food_prices.csv")
  
    # dropping columns
    df.drop(columns=['Unnamed: 0','mp_commoditysource','currency_id','country_id',
                 'market_id','state_id','produce_id','pt_id','quantity'],  inplace= True)

    # fiiling none columns state
    df['state'].fillna('unknown', inplace=True)
    #df['year'] = df.year.replace(',', '.')
    
    #renaming two columns
    df.rename({'um_unit_id': 'exchanged_qty'}, axis=1, inplace=True)
    df['exchanged_qty'] = df.exchanged_qty.astype('float')

    #cleaning produce column and renaming it
    df['core_produce'] = df['produce'].str.extract(r'([^\(]+)')
    df['core_produce'] = df['core_produce'].str.split('-').str[0]
    df['core_produce'] = df['core_produce'].str.strip()
    return df


df = load_data()
#st.subheader("Data  Preview")
#st.dataframe(df.tail())
st.sidebar.title("filters")
produces = df['core_produce'].unique()
years = df['year'] = df.year.replace(',', '')
years = df['year'].unique()
countries = df['country'].unique()
no_exchanged =df['exchanged_qty'].sum()
sumPrice =df['price'].sum().round(2)
naija = df[df['country'] == 'Nigeria']


#lengths
no_produces = len(produces)
no_years = len(years)
no_countries = len(countries)

# create a multislect for produces
selected_produces = st.sidebar.multiselect("select products", produces,[produces[0]])
selected_years = st.sidebar.multiselect("Select year", years,[years[0]])
selected_countries = st.sidebar.multiselect("select country", countries,[countries[0]])



# display in columns
st.markdown('###')
col1, col2, col3 = st.columns(3)
col1.metric("No of produce", f'{no_produces:,}')
col2.metric("Total Price", f'{sumPrice:,}')
col3.metric("Quantity exchanged", f'{no_exchanged:,}')



# returning filtered table
new_table = df.query("core_produce == @selected_produces & year == @selected_years & country == @selected_countries")
no_new_table = new_table['produce'].nunique()

#catching error
st.subheader("Filtered tables")
if not selected_produces:
    st.error("select an article")
elif not selected_years:
    st.error("select year")
elif not selected_countries: 
    st.error("select country")
elif new_table.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.
else:
    st.dataframe(new_table.sample(3))

# calculations
total_produce_selected = len(selected_produces)
total_selected_country = len(selected_countries)
no_years_selected = len(selected_years)

# display in columns
col1,col2,col3 = st.columns(3)
if total_produce_selected:
    col1.metric("Produce selected",f'{total_produce_selected:,}')
else:
    col1.metric("No of produce to pick from", f'{no_produces:,}')
if total_selected_country:
    col3.metric("Countries selected",f'{total_selected_country:,}')
else:
    col3.metric("Countries to pick from", f'{no_countries:,}')
if no_years_selected:
    col2.metric("Years selected",f'{no_years_selected:,}')
else:
    col2.metric("Years to pic from", f'{no_years:,}')







average_price_year = df.groupby('year')['price'].mean().sort_values(ascending=False)
avg_price_yr = px.scatter(
    average_price_year ,
    x=average_price_year.index,
    y="price",
    title="<b>Average price per year</b>",
    color_discrete_sequence=["green"] * len(average_price_year   ),
    template="plotly_white"
)
avg_price_yr.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(avg_price_yr)








average_price_produce = df.groupby('core_produce')['price'].mean().sort_values(ascending=False)
avg_price_fig = px.bar(
    average_price_produce  ,
    x=average_price_produce.index,
    y="price",
    title="<b>Average price per produce</b>",
    color_discrete_sequence=["#0083B8"] * len(average_price_produce  ),
    template="plotly_white"
)
avg_price_fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(avg_price_fig)







average_price_year = df.groupby('year')['price'].std().sort_values(ascending=False)
avg_price_yr = px.histogram(
    average_price_year ,
    x=average_price_year.index,
    y="price",
    title="<b>Average price per year</b>",
    color_discrete_sequence=["green"] * len(average_price_year   ),
    template="plotly_white"
)
avg_price_yr.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(avg_price_yr)





#average_price_year = df.groupby('year')['price'].mean().sort_values(ascending=False)
average_price_coun =df.groupby('country')['price'].mean().sort_values(ascending=False)
#st.dataframe(average_price_coun)
avg_price_cou = px.line(
    average_price_coun,
    x=average_price_coun.index,
    y="price",
    title="<b>Average price per country</b>",
    color_discrete_sequence=["#0083B8"] * len(average_price_coun ),
    template="plotly_white",
)
avg_price_cou.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(avg_price_cou)




grouped_marketype = df.groupby('market_type')['exchanged_qty'].sum().reset_index()
grouped_marketype = grouped_marketype.sort_values(by = 'exchanged_qty', ascending = False)
mrkt_fig = px.pie(
    grouped_marketype,
    names="market_type",
    values="exchanged_qty",
    hover_data=['exchanged_qty'],
    title="<b>Market Type</b>",
    template="plotly_white"
)
mrkt_fig.update_layout(
    plot_bgcolor="rgba(7,0,4,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(mrkt_fig)












state_price_volatility = new_table.groupby('state')['price'].std().sort_values(ascending=False)
state_vol_fig = px.bar(
    state_price_volatility ,
    x=state_price_volatility.index,
    y="price",
    title="<b>state price volatility</b>",
    color_discrete_sequence=["#0083B8"] * len(state_price_volatility ),
    template="plotly_white"
)
state_vol_fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(state_vol_fig)






price_by_product = (
    new_table.groupby(by=["country"]).sum()[["price"]].sort_values("price")
    
)
sales_fig = px.bar(
    price_by_product,
    x=price_by_product.index,
    y="price",
    title="<b>Sum price by produce</b>",
    color_discrete_sequence=["#0083B8"] * len(price_by_product),
    template="plotly_white"
)
sales_fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
#st.plotly_chart(sales_fig)





country_price_volatility = new_table.groupby('country')['price'].std().sort_values(ascending=False)
price_vol_fig = px.bar(
    country_price_volatility ,
    x=country_price_volatility.index,
    y="price",
    title="<b>Country price volatility</b>",
    color_discrete_sequence=["white"] * len(country_price_volatility ),
    template="plotly_white"
)
price_vol_fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
#st.plotly_chart(price_vol_fig)



left_column, right_column = st.columns(2)
left_column.plotly_chart(sales_fig, use_container_width=True)
right_column.plotly_chart(price_vol_fig, use_container_width=True)






# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
