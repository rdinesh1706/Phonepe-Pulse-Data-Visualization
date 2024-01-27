import json
import streamlit as st
import pandas as pd
import mysql.connector
import requests
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk
import plotly.io as pio
from geopy.geocoders import Nominatim
import geocoder


# connecting mysql using mysql connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rdx@17",
    database="phonepe"
)
cursor = mydb.cursor(buffered=True)
# from the mysql database we are fetching the value from the each table and converting into dataframe so we can access the
# the dataframe whenever we want


# aggregation_transaction_table
cursor.execute(" select * from aggregation_transaction")
mydb.commit()
table_1 = cursor.fetchall()

aggregation_transaction_table = pd.DataFrame(table_1, columns=(
    "States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))


# aggregation_user_table
cursor.execute("select * from aggregation_user")
mydb.commit()
table_2 = cursor.fetchall()
aggregation_user_table = pd.DataFrame(table_2, columns=(
    "States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

# aggregation_insurance_table
cursor.execute("select * from aggregation_insurance")
mydb.commit()
table_3 = cursor.fetchall()

aggregation_insurance_table = pd.DataFrame(table_3, columns=(
    "States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

# map_transaction_table
cursor.execute("select * from map_transaction")
mydb.commit()
table_4 = cursor.fetchall()

map_transaction_table = pd.DataFrame(table_4, columns=(
    "States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))

# map_user_table
cursor.execute("select * from map_user")
mydb.commit()
table_5 = cursor.fetchall()

map_user_table = pd.DataFrame(table_5, columns=(
    "States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))

# map_insurance_table
cursor.execute("select * from map_insurance")
mydb.commit()
table_6 = cursor.fetchall()

map_insurance_table = pd.DataFrame(table_6, columns=(
    "States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))

# top_transaction_table
cursor.execute("select * from top_transaction")
mydb.commit()
table_7 = cursor.fetchall()

top_transaction_table = pd.DataFrame(table_7, columns=(
    "States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

# top_users_table
cursor.execute("select * from top_users")
mydb.commit()
table_8 = cursor.fetchall()

top_users_table = pd.DataFrame(table_8, columns=(
    "States", "Years", "Quarter", "Pincodes", "RegisteredUser"))

# top_insurance_table
cursor.execute("select * from top_insurance")
mydb.commit()
table_9 = cursor.fetchall()

top_insurance_table = pd.DataFrame(table_9, columns=(
    "States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))


# streamlit part

# this function is used to fetch the data from the dataframe and map them in the streamlit app
# this is used for india map plot

def aggregation_analytics(df, year):
    map1 = df[df["Years"] == year]

    map1.reset_index(drop=True, inplace=True)

    map2 = map1.groupby("States")[
        ["Transaction_count", "Transaction_amount"]].sum()
    map2.reset_index(inplace=True)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)

    fig_india_1 = px.choropleth(map1, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale="Sunsetdark",
                                range_color=(map2["Transaction_amount"].min(
                                ), map2["Transaction_amount"].max()),
                                hover_name="States", title="Transaction AMOUNT",
                                fitbounds="locations", width=800, height=800)
    fig_india_1.update_geos(visible=False)
    # fig_india_1.show()

    st.plotly_chart(fig_india_1)

# this function is used to fetch the data from the dataframe and map them in the streamlit app
# this is used for bar plot using transaction amount


def bar_graph(df, year):
    hi_tr1 = df[df["Years"] == year]
    hi_tr1 = hi_tr1[[
        "States", "Transaction_amount"]]
    hi_tr2 = hi_tr1.groupby("States")["Transaction_amount"].sum(
    ).sort_values(ascending=True)
    hi_tr3 = pd.DataFrame(hi_tr2).reset_index()

    fig_hi_tr = px.bar(hi_tr3, x="Transaction_amount", y="States", title="Transaction Amount",
                       color="Transaction_amount")
    st.plotly_chart(fig_hi_tr)

# this function is used to fetch the data from the dataframe and map them in the streamlit app
# this is used for bar plot using transaction count


def agg_bar_graph(df, year):
    hi_tr1 = df[df["Years"] == year]
    hi_tr1 = hi_tr1[[
        "States", "Transaction_count"]]
    hi_tr2 = hi_tr1.groupby("States")["Transaction_count"].sum(
    ).sort_values(ascending=True)
    hi_tr3 = pd.DataFrame(hi_tr2).reset_index()

    fig_hi_tr = px.bar(hi_tr3, x="Transaction_count", y="States", title="Transaction Count",
                       color="Transaction_count")
    st.plotly_chart(fig_hi_tr)

# this function is used to fetch the data from the dataframe and map them in the streamlit app
# this is used for bar plot using transaction amount for every quarter data


def quarter(df, year, no):
    hi_tr1 = df[df["Quarter"] == no]
    hi_tr1 = hi_tr1[hi_tr1["Years"] == year]
    hi_tr1 = hi_tr1[[
        "States", "Transaction_amount"]]
    hi_tr2 = hi_tr1.groupby("States")["Transaction_amount"].sum(
    ).sort_values(ascending=True)
    hi_tr3 = pd.DataFrame(hi_tr2).reset_index()

    fig_hi_tr = px.bar(hi_tr3, x="Transaction_amount", y="States", orientation="h", title="Transaction Amount",
                       color="Transaction_amount", width=800, height=800)

    st.plotly_chart(fig_hi_tr)
    st.write("note: if there is a empty graph means its value not avaliable")

# this function is used to fetch the data from the dataframe and map them in the streamlit app
# this is used for bar plot using transaction count for every quarter data


def user_quarter(df, year, no):
    hi_tr1 = df[df["Quarter"] == no]
    hi_tr1 = hi_tr1[hi_tr1["Years"] == year]
    hi_tr1 = hi_tr1[[
        "States", "Transaction_count"]]
    hi_tr2 = hi_tr1.groupby("States")["Transaction_count"].sum(
    ).sort_values(ascending=True)
    hi_tr3 = pd.DataFrame(hi_tr2).reset_index()

    fig_hi_tr = px.bar(hi_tr3, x="Transaction_count", y="States", orientation="h", title="Transaction Count",
                       color="Transaction_count", width=800, height=800)
    st.plotly_chart(fig_hi_tr)
    st.write("note: if there is a empty graph means its value not avaliable")

# this function is used to fetch the data from the dataframe and map them in the streamlit app
# this is used for bar plot using RegisteredUser for every quarter data


def user_reg_quarter(df, year, no):
    hi_tr1 = df[df["Quarter"] == no]
    hi_tr1 = hi_tr1[hi_tr1["Years"] == year]
    hi_tr1 = hi_tr1[[
        "States", "RegisteredUser"]]
    hi_tr2 = hi_tr1.groupby("States")["RegisteredUser"].sum(
    ).sort_values(ascending=True)
    hi_tr3 = pd.DataFrame(hi_tr2).reset_index()

    fig_hi_tr = px.bar(hi_tr3, x="RegisteredUser", y="States", orientation="h", title="Registered User in India",
                       color="RegisteredUser", width=800, height=800)
    st.plotly_chart(fig_hi_tr)
    st.write("note: if there is a empty graph means its value not avaliable")

# this function is used to fetch the data from the dataframe and map them in the streamlit app
# this is used for india map plot using transaction count for every quarter data


def cchoropleth(df, year):
    map3 = df[df["Years"] == year]
    # aiyq = map3
    # aiyqg = map4
    map3.reset_index(drop=True, inplace=True)

    map4 = map3.groupby("States")[
        ["Transaction_count", "Transaction_amount"]].sum()
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    map4.reset_index(inplace=True)
    fig_india_2 = px.choropleth(map4, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="Sunsetdark",
                                range_color=(map4["Transaction_count"].min(
                                ), map4["Transaction_count"].max()),
                                hover_name="States", title="Transaction Count",
                                fitbounds="locations", width=800, height=800)
    fig_india_2.update_geos(visible=False)

    st.plotly_chart(fig_india_2)

# this function is used to fetch the data from the dataframe and map them in the streamlit app
# this is used for india map plot using transaction count for every quarter data


def cchoropleth_am(df, year):
    map3 = df[df["Years"] == year]
    # aiyq = map3
    # aiyqg = map4
    map3.reset_index(drop=True, inplace=True)

    map4 = map3.groupby("States")[
        ["Transaction_count", "Transaction_amount"]].sum()
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    map4.reset_index(inplace=True)
    fig_india_2 = px.choropleth(map4, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale="Sunsetdark",
                                range_color=(map4["Transaction_amount"].min(
                                ), map4["Transaction_amount"].max()),
                                hover_name="States", title="Transaction_amount",
                                fitbounds="locations", width=800, height=800)
    fig_india_2.update_geos(visible=False)

    st.plotly_chart(fig_india_2)

############################
# this function is used to fetch the data from the dataframe and map them in the streamlit app
# this is used for india map plot


def map_user_choropleth(df, year):
    map3 = df[df["Years"] == year]
    map3.reset_index(drop=True, inplace=True)

    map4 = map3.groupby("States")[
        ["RegisteredUser"]].sum()
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    map4.reset_index(inplace=True)
    fig_india_2 = px.choropleth(map4, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="RegisteredUser", color_continuous_scale="Sunsetdark",
                                range_color=(map4["RegisteredUser"].min(
                                ), map4["RegisteredUser"].max()),
                                hover_name="States", title="Registered User ",
                                fitbounds="locations", width=800, height=800)
    fig_india_2.update_geos(visible=False)

    st.plotly_chart(fig_india_2)

# this function is used to fetch the data from the dataframe and map them in the streamlit app
# this is used for india map plot using transaction count for every quarter data


def agg_cchoropleth(df, year):
    map3 = df[df["Years"] == year]
    map3.reset_index(drop=True, inplace=True)

    map4 = map3.groupby("States")[
        ["Transaction_count"]].sum()
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    map4.reset_index(inplace=True)
    fig_india_2 = px.choropleth(map4, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="Sunsetdark",
                                range_color=(map4["Transaction_count"].min(
                                ), map4["Transaction_count"].max()),
                                hover_name="States", title="Transaction Count",
                                fitbounds="locations", width=800, height=800)
    fig_india_2.update_geos(visible=False)

    st.plotly_chart(fig_india_2)


def show_agg():
    # tab1 = st.tabs(
    #     ["Aggregated Analysis"])
    # with tab1:
    method = st.radio("**Select the Aggregated Analysis Method**",
                      ["Transaction Analysis", "User Analysis", "Insurance Analysis"])
    method2 = st.radio("**Select the year**",
                       ["2018", "2019", "2020", "2021", "2022", "2023"])

    if method == "Insurance Analysis" and method2 == "2018":
        st.write("There is no data")
        # year = 2018
        # df = aggregation_insurance_table
        # aggregation_analytics(df, year)
        # tab1, tab2, tab3, tab4 = st.tabs(
        #     ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        # with tab1:
        #     no = 1
        #     quarter(df, year, no)
        # with tab2:
        #     no = 2
        #     quarter(df, year, no)
        # with tab3:
        #     no = 3
        #     quarter(df, year, no)
        # with tab4:
        #     no = 4
        #     quarter(df, year, no)
    elif method == "Transaction Analysis" and method2 == "2018":
        year = 2018
        df = aggregation_transaction_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method == "User Analysis" and method2 == "2018":
        year = 2018
        df = aggregation_user_table
        agg_cchoropleth(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            user_quarter(df, year, no)
        with tab2:
            no = 2
            user_quarter(df, year, no)
        with tab3:
            no = 3
            user_quarter(df, year, no)
        with tab4:
            no = 4
            user_quarter(df, year, no)

    elif method == "Insurance Analysis" and method2 == "2019":
        st.write("There is no data")
        # year = 2019
        # df = aggregation_insurance_table
        # aggregation_analytics(df, year)
        # tab1, tab2, tab3, tab4 = st.tabs(
        #     ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        # with tab1:
        #     no = 1
        #     quarter(df, year, no)
        # with tab2:
        #     no = 2
        #     quarter(df, year, no)
        # with tab3:
        #     no = 3
        #     quarter(df, year, no)
        # with tab4:
        #     no = 4
        #     quarter(df, year, no)
    elif method == "Transaction Analysis" and method2 == "2019":
        year = 2019
        df = aggregation_transaction_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method == "User Analysis" and method2 == "2019":
        year = 2019
        df = aggregation_user_table
        agg_cchoropleth(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            user_quarter(df, year, no)
        with tab2:
            no = 2
            user_quarter(df, year, no)
        with tab3:
            no = 3
            user_quarter(df, year, no)
        with tab4:
            no = 4
            user_quarter(df, year, no)

    elif method == "Insurance Analysis" and method2 == "2020":
        # st.write("There is no 2023 data")
        year = 2020
        df = aggregation_insurance_table
        cchoropleth(df, year)
        aggregation_analytics(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method == "Transaction Analysis" and method2 == "2020":
        year = 2020
        df = aggregation_transaction_table
        cchoropleth(df, year)

        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method == "User Analysis" and method2 == "2020":
        year = 2020
        df = aggregation_user_table
        agg_cchoropleth(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            user_quarter(df, year, no)
        with tab2:
            no = 2
            user_quarter(df, year, no)
        with tab3:
            no = 3
            user_quarter(df, year, no)
        with tab4:
            no = 4
            user_quarter(df, year, no)

    elif method == "Insurance Analysis" and method2 == "2021":
        year = 2021
        df = aggregation_insurance_table
        cchoropleth(df, year)
        aggregation_analytics(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method == "Insurance Analysis" and method2 == "2022":
        year = 2022
        df = aggregation_insurance_table
        cchoropleth(df, year)
        aggregation_analytics(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method == "Insurance Analysis" and method2 == "2023":
        year = 2023
        df = aggregation_insurance_table
        cchoropleth(df, year)
        aggregation_analytics(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)

    elif method == "Transaction Analysis" and method2 == "2021":
        year = 2021
        df = aggregation_transaction_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method == "Transaction Analysis" and method2 == "2022":
        year = 2022
        df = aggregation_transaction_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method == "Transaction Analysis" and method2 == "2023":
        year = 2023
        df = aggregation_transaction_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)

    elif method == "User Analysis" and method2 == "2021":
        year = 2021
        df = aggregation_user_table
        agg_cchoropleth(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            user_quarter(df, year, no)
        with tab2:
            no = 2
            user_quarter(df, year, no)
        with tab3:
            no = 3
            user_quarter(df, year, no)
        with tab4:
            no = 4
            user_quarter(df, year, no)
    elif method == "User Analysis" and method2 == "2022":
        year = 2022
        df = aggregation_user_table
        agg_cchoropleth(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            user_quarter(df, year, no)
        with tab2:
            no = 2
            user_quarter(df, year, no)
        with tab3:
            no = 3
            user_quarter(df, year, no)
        with tab4:
            no = 4
            user_quarter(df, year, no)
    elif method == "User Analysis" and method2 == "2023":
        st.write("There is no 2023 data")
        #     year = 2023
        #     df = aggregation_user_table
        #     agg_cchoropleth(df, year)
        #     tab1, tab2, tab3, tab4 = st.tabs(
        #         ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        #     with tab1:
        #         no = 1
        #         user_quarter(df, year, no)
        #     with tab2:
        #         no = 2
        #         user_quarter(df, year, no)
        #     with tab3:
        #         no = 3
        #         user_quarter(df, year, no)
        #     with tab4:
        #         no = 4
        #         user_quarter(df, year, no)
    # with tab2:

        # method3 = st.radio("**Select the Map Analysis ahdhihasd Method**",
        #                    ["Transaction Analysis", "User Analysis", "Insurance Analysis"])

    # with tab3:
        # method5 = st.radio("**Select the Top Analysis Method**",
        #                    ["Transaction Analysis", "User Analysis", "Insurance Analysis"])
        # method6 = st.radio("**Select the year..**",
        #                    ["2021", "2022", "2023"])
        # if method == "Insurance Analysis" and method2 == "2021":
        #     year = 2021
        #     df = top_insurance_table
        #     aggregation_analytics(df, year)
        #     tab1, tab2, tab3, tab4 = st.tabs(
        #         ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        #     with tab1:
        #         no = 1
        #         quarter(df, year, no)
        #     with tab2:
        #         no = 2
        #         quarter(df, year, no)
        #     with tab3:
        #         no = 3
        #         quarter(df, year, no)
        #     with tab4:
        #         no = 4
        #         quarter(df, year, no)
        # elif method == "Insurance Analysis" and method2 == "2022":
        #     year = 2022
        #     df = top_insurance_table
        #     aggregation_analytics(df, year)
        #     tab1, tab2, tab3, tab4 = st.tabs(
        #         ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        #     with tab1:
        #         no = 1
        #         quarter(df, year, no)
        #     with tab2:
        #         no = 2
        #         quarter(df, year, no)
        #     with tab3:
        #         no = 3
        #         quarter(df, year, no)
        #     with tab4:
        #         no = 4
        #         quarter(df, year, no)
        # elif method == "Insurance Analysis" and method2 == "2023":
        #     year = 2023
        #     df = top_insurance_table
        #     aggregation_analytics(df, year)
        #     tab1, tab2, tab3, tab4 = st.tabs(
        #         ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        #     with tab1:
        #         no = 1
        #         quarter(df, year, no)
        #     with tab2:
        #         no = 2
        #         quarter(df, year, no)
        #     with tab3:
        #         no = 3
        #         quarter(df, year, no)
        #     with tab4:
        #         no = 4
        #         quarter(df, year, no)
#########################################


# 4th button in sidebar of streamlit
def map_thirdd():
    aa = pd.read_csv("file2.csv")
    chart_data = pd.DataFrame(
        aa,
        columns=['latitude', 'longitude', 'States', 'Transaction_amount'])
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=20.5937,
            longitude=78.9629,
            zoom=4,
            pitch=500,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=chart_data,
                get_position='[longitude, latitude]',
                radius=20000,
                elevation_scale=1000,
                elevation_range=[0, 1000],
                pickable=True,
                hover_name="States",
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=chart_data,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=2000,
            ),
        ],

    ))
#########################################


# 2nd button in sidebar of streamlit
def mapLL():
    method3 = st.radio("**Select the Map Analysis Method**",
                       ["Transaction Analysis", "User Analysis", "Insurance Analysis"])
    method4 = st.radio("**Select the year.**",
                       ["2018", "2019", "2020", "2021", "2022", "2023"])

    if method3 == "Insurance Analysis" and method4 == "2018":
        year = 2018
        st.write("There is no 2018 data")
        # df = map_insurance_table
        # cchoropleth(df, year)
        # tab1, tab2, tab3, tab4 = st.tabs(
        #     ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        # with tab1:
        #     no = 1
        #     quarter(df, year, no)
        # with tab2:
        #     no = 2
        #     quarter(df, year, no)
        # with tab3:
        #     no = 3
        #     quarter(df, year, no)
        # with tab4:
        #     no = 4
        #     quarter(df, year, no)
    elif method3 == "Insurance Analysis" and method4 == "2019":
        st.write("There is no 2019 data")
        # year = 2019
        # df = map_insurance_table
        # cchoropleth(df, year)
        # tab1, tab2, tab3, tab4 = st.tabs(
        #     ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        # with tab1:
        #     no = 1
        #     quarter(df, year, no)
        # with tab2:
        #     no = 2
        #     quarter(df, year, no)
        # with tab3:
        #     no = 3
        #     quarter(df, year, no)
        # with tab4:
        #     no = 4
        #     quarter(df, year, no)
    elif method3 == "Insurance Analysis" and method4 == "2020":
        year = 2020
        df = map_insurance_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method3 == "Insurance Analysis" and method4 == "2021":
        year = 2021
        df = map_insurance_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method3 == "Insurance Analysis" and method4 == "2022":
        year = 2022
        df = map_insurance_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method3 == "Insurance Analysis" and method4 == "2023":
        year = 2023
        df = map_insurance_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)

    elif method3 == "Transaction Analysis" and method4 == "2018":
        year = 2018
        df = map_transaction_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method3 == "Transaction Analysis" and method4 == "2019":
        year = 2019
        df = map_transaction_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method3 == "Transaction Analysis" and method4 == "2020":
        year = 2020
        df = map_transaction_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method3 == "Transaction Analysis" and method4 == "2021":
        year = 2021
        df = map_transaction_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method3 == "Transaction Analysis" and method4 == "2022":
        year = 2022
        df = map_transaction_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method3 == "Transaction Analysis" and method4 == "2023":
        year = 2023
        df = map_transaction_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)

    elif method3 == "User Analysis" and method4 == "2018":
        year = 2018
        df = map_user_table
        map_user_choropleth(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            user_reg_quarter(df, year, no)
        with tab2:
            no = 2
            user_reg_quarter(df, year, no)
        with tab3:
            no = 3
            user_reg_quarter(df, year, no)
        with tab4:
            no = 4
            user_reg_quarter(df, year, no)
    elif method3 == "User Analysis" and method4 == "2019":
        year = 2019
        df = map_user_table
        map_user_choropleth(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            user_reg_quarter(df, year, no)
        with tab2:
            no = 2
            user_reg_quarter(df, year, no)
        with tab3:
            no = 3
            user_reg_quarter(df, year, no)
        with tab4:
            no = 4
            user_reg_quarter(df, year, no)
    elif method3 == "User Analysis" and method4 == "2020":
        year = 2020
        df = map_user_table
        map_user_choropleth(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            user_reg_quarter(df, year, no)
        with tab2:
            no = 2
            user_reg_quarter(df, year, no)
        with tab3:
            no = 3
            user_reg_quarter(df, year, no)
        with tab4:
            no = 4
            user_reg_quarter(df, year, no)
    elif method3 == "User Analysis" and method4 == "2021":
        year = 2021
        df = map_user_table
        map_user_choropleth(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            user_reg_quarter(df, year, no)
        with tab2:
            no = 2
            user_reg_quarter(df, year, no)
        with tab3:
            no = 3
            user_reg_quarter(df, year, no)
        with tab4:
            no = 4
            user_reg_quarter(df, year, no)
    elif method3 == "User Analysis" and method4 == "2022":
        year = 2022
        df = map_user_table
        map_user_choropleth(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            user_reg_quarter(df, year, no)
        with tab2:
            no = 2
            user_reg_quarter(df, year, no)
        with tab3:
            no = 3
            user_reg_quarter(df, year, no)
        with tab4:
            no = 4
            user_reg_quarter(df, year, no)
    elif method3 == "User Analysis" and method4 == "2023":
        year = 2023
        df = map_user_table
        map_user_choropleth(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            user_reg_quarter(df, year, no)
        with tab2:
            no = 2
            user_reg_quarter(df, year, no)
        with tab3:
            no = 3
            user_reg_quarter(df, year, no)
        with tab4:
            no = 4
            user_reg_quarter(df, year, no)
#########################################


# 3rd button in sidebar of streamlit
def Top():
    method5 = st.radio("**Select the Top Analysis Method**",
                       ["Transaction Analysis", "User Analysis", "Insurance Analysis"])
    method6 = st.radio("**Select the year..**",
                       ["2018", "2019", "2020", "2021", "2022", "2023"])

    if method5 == "Insurance Analysis" and method6 == "2018":
        st.write("There is no 2018 data")
        # year = 2018
        # df = top_insurance_table
        # cchoropleth(df, year)
        # tab1, tab2, tab3, tab4 = st.tabs(
        #     ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        # with tab1:
        #     no = 1
        #     quarter(df, year, no)
        # with tab2:
        #     no = 2
        #     quarter(df, year, no)
        # with tab3:
        #     no = 3
        #     quarter(df, year, no)
        # with tab4:
        #     no = 4
        #     quarter(df, year, no)
    elif method5 == "Insurance Analysis" and method6 == "2019":
        st.write("There is no 2019 data")
        # year = 2019
        # df = top_insurance_table
        # cchoropleth(df, year)
        # tab1, tab2, tab3, tab4 = st.tabs(
        #     ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        # with tab1:
        #     no = 1
        #     quarter(df, year, no)
        # with tab2:
        #     no = 2
        #     quarter(df, year, no)
        # with tab3:
        #     no = 3
        #     quarter(df, year, no)
        # with tab4:
        #     no = 4
        #     quarter(df, year, no)
    elif method5 == "Insurance Analysis" and method6 == "2020":
        year = 2020
        df = top_insurance_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method5 == "Insurance Analysis" and method6 == "2021":
        year = 2021
        df = top_insurance_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method5 == "Insurance Analysis" and method6 == "2022":
        year = 2022
        df = top_insurance_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method5 == "Insurance Analysis" and method6 == "2023":
        year = 2023
        df = top_insurance_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)

    elif method5 == "Transaction Analysis" and method6 == "2018":
        year = 2018
        df = top_transaction_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method5 == "Transaction Analysis" and method6 == "2019":
        year = 2019
        df = top_transaction_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method5 == "Transaction Analysis" and method6 == "2020":
        year = 2020
        df = top_transaction_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method5 == "Transaction Analysis" and method6 == "2021":
        year = 2021
        df = top_transaction_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method5 == "Transaction Analysis" and method6 == "2022":
        year = 2022
        df = top_transaction_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)
    elif method5 == "Transaction Analysis" and method6 == "2023":
        year = 2023
        df = top_transaction_table
        cchoropleth(df, year)
        cchoropleth_am(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            quarter(df, year, no)
        with tab2:
            no = 2
            quarter(df, year, no)
        with tab3:
            no = 3
            quarter(df, year, no)
        with tab4:
            no = 4
            quarter(df, year, no)

    elif method5 == "User Analysis" and method6 == "2018":
        year = 2018
        df = top_users_table
        map_user_choropleth(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            user_reg_quarter(df, year, no)
        with tab2:
            no = 2
            user_reg_quarter(df, year, no)
        with tab3:
            no = 3
            user_reg_quarter(df, year, no)
        with tab4:
            no = 4
            user_reg_quarter(df, year, no)
    elif method5 == "User Analysis" and method6 == "2019":
        year = 2019
        df = top_users_table
        map_user_choropleth(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            user_reg_quarter(df, year, no)
        with tab2:
            no = 2
            user_reg_quarter(df, year, no)
        with tab3:
            no = 3
            user_reg_quarter(df, year, no)
        with tab4:
            no = 4
            user_reg_quarter(df, year, no)
    elif method5 == "User Analysis" and method6 == "2020":
        year = 2020
        df = top_users_table
        map_user_choropleth(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            user_reg_quarter(df, year, no)
        with tab2:
            no = 2
            user_reg_quarter(df, year, no)
        with tab3:
            no = 3
            user_reg_quarter(df, year, no)
        with tab4:
            no = 4
            user_reg_quarter(df, year, no)
    elif method5 == "User Analysis" and method6 == "2021":
        year = 2021
        df = top_users_table
        map_user_choropleth(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            user_reg_quarter(df, year, no)
        with tab2:
            no = 2
            user_reg_quarter(df, year, no)
        with tab3:
            no = 3
            user_reg_quarter(df, year, no)
        with tab4:
            no = 4
            user_reg_quarter(df, year, no)
    elif method5 == "User Analysis" and method6 == "2022":
        year = 2022
        df = top_users_table
        map_user_choropleth(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            user_reg_quarter(df, year, no)
        with tab2:
            no = 2
            user_reg_quarter(df, year, no)
        with tab3:
            no = 3
            user_reg_quarter(df, year, no)
        with tab4:
            no = 4
            user_reg_quarter(df, year, no)
    elif method5 == "User Analysis" and method6 == "2023":
        year = 2023
        df = top_users_table
        map_user_choropleth(df, year)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"])
        with tab1:
            no = 1
            user_reg_quarter(df, year, no)
        with tab2:
            no = 2
            user_reg_quarter(df, year, no)
        with tab3:
            no = 3
            user_reg_quarter(df, year, no)
        with tab4:
            no = 4
            user_reg_quarter(df, year, no)
#########################################


# 5th button in sidebar of streamlit
def show_down():
    question = st.selectbox("Choose the Question", ("1. Top 5 states highest transaction amount",
                                                    "2. Top 5 states lowest transaction amount",
                                                    "3. Top 5 districts with highest transaction amount",
                                                    "4. Top 5 districts with lowest transaction amount",
                                                    "5. Top 3 mobile brand",
                                                    "6. Top 5 states lowest transaction count in 2022",
                                                    "7. Top 5 states Highest transaction count in  2021",
                                                    "8. Top 5 States With highest AppOpens",
                                                    "9. Transaction type in 2021",
                                                    "10. Top 3 least used mobile brands"))

    if question == "1. Top 5 states highest transaction amount":
        hi_tr1 = aggregation_transaction_table[[
            "States", "Transaction_amount"]]
        hi_tr2 = hi_tr1.groupby("States")["Transaction_amount"].sum(
        ).sort_values(ascending=False)
        hi_tr3 = pd.DataFrame(hi_tr2).reset_index().head(5)

        fig_hi_tr = px.bar(hi_tr3, x="States", y="Transaction_amount", title="Top 5 states highest transaction amount",
                           color="Transaction_amount")
        return st.plotly_chart(fig_hi_tr)

    elif question == "2. Top 5 states lowest transaction amount":
        lo_tr1 = aggregation_transaction_table[[
            "States", "Transaction_amount"]]
        lo_tr2 = lo_tr1.groupby(
            "States")["Transaction_amount"].sum().sort_values(ascending=True)
        lo_tr3 = pd.DataFrame(lo_tr2).reset_index().head(5)
        fig_lo_tr = px.bar(lo_tr3, x="States", y="Transaction_amount", title="Top 5 states lowest transaction amount",
                           color="States")
        return st.plotly_chart(fig_lo_tr)

    elif question == "3. Top 5 districts with highest transaction amount":
        DH_TA = map_transaction_table[["Districts", "Transaction_amount"]]
        DH_TA1 = DH_TA.groupby("Districts")[
            "Transaction_amount"].sum().sort_values(ascending=False)
        DH_TA2 = pd.DataFrame(DH_TA1).reset_index().head(5)

        fig_DH_TA2 = px.pie(DH_TA2, values="Transaction_amount", names="Districts",
                            color="Districts", title="Districts with Highest Transaction Amount")
        return st.plotly_chart(fig_DH_TA2)

    elif question == "4. Top 5 districts with lowest transaction amount":
        DL_TA = map_transaction_table[["Districts", "Transaction_amount"]]
        DL_TA1 = DL_TA.groupby("Districts")[
            "Transaction_amount"].sum().sort_values(ascending=True)
        DL_TA2 = pd.DataFrame(DL_TA1).reset_index().head(5)

        fig_DL_TA2 = px.pie(DL_TA2, values="Transaction_amount", names="Districts",
                            color_discrete_sequence=px.colors.sequential.dense_r, title="Districts with Lowest Transaction Amount")
        return st.plotly_chart(fig_DL_TA2)

    elif question == "5. Top 3 mobile brand":
        tp_brand = aggregation_user_table[["Brands", "Transaction_count"]]
        tp_brand1 = tp_brand.groupby("Brands")[
            "Transaction_count"].sum().sort_values(ascending=False)
        tp_brand2 = pd.DataFrame(tp_brand1).reset_index().head(5)
        fig_brand = px.bar(tp_brand2, y="Brands", x="Transaction_count", color="Brands", orientation="h", hover_name="Brands",
                           title="Top 3 mobile brand"
                           )
        return st.plotly_chart(fig_brand)

    elif question == "6. Top 5 states lowest transaction count in 2022":
        sltc = map_transaction_table[map_transaction_table["Years"] == 2022]
        sltc1 = sltc[["States", "Transaction_count"]]

        sltc2 = sltc1.groupby("States")[
            "Transaction_count"].sum().sort_values(ascending=True)

        sltc3 = pd.DataFrame(sltc2).reset_index().head(5)

        fig_sltc3 = px.bar(sltc3, x="States", y="Transaction_count", title="Transaction type in 2022", color="States"
                           )
        return st.plotly_chart(fig_sltc3)

    elif question == "7. Top 5 states Highest transaction count in  2021":
        shtc = map_transaction_table[map_transaction_table["Years"] == 2021]
        shtc1 = shtc[["States", "Transaction_count"]]

        shtc2 = shtc1.groupby("States")[
            "Transaction_count"].sum().sort_values(ascending=True)

        shtc3 = pd.DataFrame(shtc2).reset_index().head(5)

        fig_shtc3 = px.bar(shtc3, x="States", y="Transaction_count", title="Highest Transaction type in 2021", color="States"
                           )
        return st.plotly_chart(fig_shtc3)

    elif question == "8. Top 5 States With highest AppOpens":
        HA = map_user_table[["States", "AppOpens"]]

        HA1 = HA.groupby("States")["AppOpens"].sum(
        ).sort_values(ascending=False)

        HA2 = pd.DataFrame(HA1).reset_index().head(5)

        fig_HA2 = px.bar(HA2, x="States", y="AppOpens",
                         title=" Top 5 States With highest AppOpens")

        return st.plotly_chart(fig_HA2)

    elif question == "9. Transaction type in 2021":
        TT = aggregation_transaction_table[aggregation_transaction_table["Years"] == 2021]
        TT1 = TT[[
            "Transaction_type", "Transaction_count"]]
        TT2 = TT1.groupby("Transaction_type")[
            "Transaction_count"].sum().sort_values(ascending=False)
        TT3 = pd.DataFrame(TT2).reset_index()
        fig_TT = px.bar(TT3, x="Transaction_type", y="Transaction_count", title="Transaction type in 2021", color="Transaction_type"
                        )
        return st.plotly_chart(fig_TT)

    elif question == "10. Top 3 least used mobile brands":
        ls_brand = aggregation_user_table[["Brands", "Transaction_count"]]
        ls_brand1 = ls_brand.groupby("Brands")[
            "Transaction_count"].sum().sort_values(ascending=True)
        ls_brand2 = pd.DataFrame(ls_brand1).reset_index().head(5)
        fig_brand = px.bar(ls_brand2, y="Brands", x="Transaction_count", color="Brands", orientation="h", hover_name="Brands",
                           title="Top 3 least used mobile brands"
                           )
        return st.plotly_chart(fig_brand)
#########################################


with st.sidebar:
    st.markdown("<h1 style='text-align:center;font-family:Georgia;color:red;background-color: #DCD494;border: 2px solid red;border-radius: 25px;,'>Phone_pe Analytics.🤳📲↔💵💰↔📲🤳</h1>",
                unsafe_allow_html=True)

    st.title("Press the button for the view the plot👇")
    show_table = st.radio(
        "Press the button for the view 👇",
        ["Data 💾📡", "Map 🗺📍", "Top ✈️🗼", "Map_ddd 🥽🕶️", "Question❓🙋‍♂"],
    )


if show_table == "Data 💾📡":
    show_agg()
elif show_table == "Map 🗺📍":
    mapLL()
elif show_table == "Top ✈️🗼":
    Top()
elif show_table == "Map_ddd 🥽🕶️":
    map_thirdd()
elif show_table == "Question❓🙋‍♂":
    show_down()
