import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
st.set_page_config(
    page_title="My Streamlit App",
    page_icon=":bar_chart:",
    layout="wide",
)

df = pd.read_csv("Global Population Trends(2016-2022).csv")
#data = df.loc[df["Year"]==2020]
#I will work with the first 100 rows of the data because the number of countries
# is too big and they are not classified into regions or something that I can group them by.
df_small = df.loc[:100, :]
# Replace '-' with NaN in the DataFrame
df_small = df_small.replace('-', np.nan)
df_small.dropna()
st.sidebar.header("Please Filter Here:")
year = st.sidebar.multiselect(
    "Select the year:",
    options=df_small["Year"].unique(),
    default=df_small["Year"].unique()
)
country = st.sidebar.multiselect(
    "Select the country:",
    options=df_small["Country"].unique(),
    default=df_small["Country"].unique()
)
st.title(":bar_chart: Population Density BarChart")
st.markdown("##")

df_small['Population Density'] = pd.to_numeric(df_small['Population Density'], errors='coerce')
df_small['Life Expectancy'] = pd.to_numeric(df_small['Life Expectancy'], errors='coerce')
df_small['Growth Rate'] = pd.to_numeric(df_small['Growth Rate'], errors='coerce')
df_small['Birth Rate'] = pd.to_numeric(df_small['Birth Rate'], errors='coerce')
df_selection = df_small.query("Year == @year & Country == @country")

if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()
Average_Birth_Rate = int(round(df_selection['Birth Rate'].mean(),1))
Average_Life_Expectancy = int(round(df_selection["Life Expectancy"].mean(),1))
Average_Growth_Rate = int(round(df_selection["Growth Rate"].mean(),1))
left_column,middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Average Life Expectancy:")
    st.subheader(f"{Average_Life_Expectancy} ")
with middle_column:
    st.subheader("Average Birth Rate: ")
    st.subheader(f"{Average_Birth_Rate} ")
with right_column:
    st.subheader("Average Growth Rate:")
    st.subheader(f"{Average_Growth_Rate} ") 
st.markdown("""---""")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df_selection)
#Adding a slider for the year range
#I will exclude 2021 because there is no data on population density in 2021 for the majority of countries
year_to_filter = st.slider(
    "Select a Year",2017,2020, 2017) #min = 2017, max = 2020, default = 2017
filtered_data = df_small.loc[df_small["Year"]==year_to_filter]
fig1 = px.bar(
    filtered_data,
    x="Country", 
    y=filtered_data['Population Density'], 
    color_discrete_sequence=["#0083B8"], 
    template="plotly_white",
    title="Population Density per Country:")
st.plotly_chart(fig1)

# Load the external data source with iso_alpha codes
iso_data = px.data.gapminder().query("year==2007")
df = df.rename(columns={'Country': 'country'})#to be able to merge the two datasets
# Merge the two DataFrames on the 'country' column to add 'iso_alpha' to my original DataFrame
df2 = pd.merge(df, iso_data[['country', 'iso_alpha']], on='country', how='left')
filter_year = st.slider(
    "Select a Year ",2017,2021, 2021)
filtered_data2 = df2.loc[df2["Year"]==filter_year]
fig2 = px.choropleth(filtered_data2, locations="iso_alpha",
                    color="Growth Rate",
                    hover_name="country",
                    color_continuous_scale=px.colors.sequential.Plasma)
st.plotly_chart(fig2)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)