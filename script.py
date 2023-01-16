#import libs
import numpy as np
import pandas as pd
import plotly_express as px
import streamlit as st 

#read file 
df = pd.read_excel('data.xls', sheet_name='Sheet1')

df["month"] = pd.DatetimeIndex(df['Дата']).month
df["year"] = pd.DatetimeIndex(df['Дата']).year


#streamlit configuration
st.set_page_config(
    page_title = "Sales",
    page_icon=":bar_chart:",
    layout = "wide")


#________SIDEBAR________ (Країна + рік)
st.sidebar.header("Please Filter Here:")
country = st.sidebar.multiselect(
    "Select the Country:",
    options=df['Страна'].unique(),
    default=df['Страна'].unique()
)

year = st.sidebar.multiselect(
    "Select the Year:",
    options=df['year'].unique(),
    default=df['year'].unique()
)

df_selection = df.query(
    "Страна == @country & year == @year"
)


#________MAINPAGE________
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")


# TOP KPI's
total_sales = int(df_selection["Продажи, дол"].sum())
average_sale_by_transaction = round(df_selection["Продажи, дол"].mean(), 2)

left_column,  right_column = st.columns(2)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# SALES BY MONTH [BAR CHART]
sales_by_month= df_selection.groupby(by=["month"]).sum()[["Продажи, дол"]]
fig_monthly_sales = px.bar(
    sales_by_month,
    x=sales_by_month.index,
    y=["Продажи, дол"],
    title="<b>Sales by monthes</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_month),
    template="plotly_white",
)
fig_monthly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_monthly_sales)

#________HIDE STREAMLIT STYLE________
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)