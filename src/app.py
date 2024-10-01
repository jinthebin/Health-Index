import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os
from data_read import health_ind, df4, glossary, exc4

st.set_page_config(layout="wide", page_title="Health Index - UK")

st.title("Health across the UK")


with st.expander("Click here for additional information"):
    st.write("Some really useful information")
    st.link_button(label="Find out more", 
                   url="https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/articles/howhealthhaschangedinyourarea2015to2021/2023-06-16",
                   help="Links to ONS website where the data is sourced from.")
    # st.image("https://cdn.ons.gov.uk/assets/images/ons-logo/v2/ons-logo.svg")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["UK wide data by year",
     "Indices by region",
     "Glossary",
     "Overall Health Index Scores",
     "KPIs"]
     )

with tab1:

    st.divider()

    year_select = st.selectbox("Please select the year",
                             health_ind["Year"].unique()
                             )
    st.plotly_chart(
        px.bar(
            health_ind,
            x = "Area name",
            y = "Value",
            color= "Indicator name",
            title=f"Health across UK for {year_select}", 

        )
    )

with tab2:

    indicator_select = st.selectbox("Please select indicator(s)",
                                health_ind["Indicator name"].unique()
                                )
    loc_select = st.multiselect("Please select a city",
                            health_ind["Area name"].unique())

    health_df = health_ind[health_ind["Indicator name"]==indicator_select]
    health_df2 = health_df[health_df["Area name"].isin(loc_select)]
    col_1, col_2 = st.columns([0.5, 0.5])
    with col_1:

        # st.divider()

        st.plotly_chart(
            px.line(health_df2, 
                        x="Year", 
                        y="Value", 
                        color="Area name",
                        markers=True,
                        symbol="Area name",
                        title=f'Health index for indicator {indicator_select} for {loc_select} over time')
        )

    with col_2:



        st.dataframe(
            health_df2,
            use_container_width=True
            ,
            column_config={
                "Year": st.column_config.NumberColumn(
                    "Year",
                    format="%f"
                )
            }
            )
with tab3:
    # gloassry = pd.read_excel("dat/healthindex.xlsx", 
    #                          sheet_name='Table_1_Indicator_details', 
    #                          header=2,
    #                          usecols="A:J"
    #                          )
    
    gloassry = (glossary.rename(columns={"Indicator (component) name": "Indicator"})) #tranforming dataframe - renaming columns
    st.dataframe(
            glossary,
            use_container_width=True
            )

with tab4:
    #need to use selenium to crawl on ONS website:
    #https://stackoverflow.com/questions/16627227/how-do-i-avoid-http-error-403-when-web-scraping-with-python#:~:text=This%20is%20probably%20because%20of%20mod_security
    #https://www.freecodecamp.org/news/better-web-scraping-in-python-with-selenium-beautiful-soup-and-pandas-d6390592e251
    #exc4 = "https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/healthindexscoresengland/current/healthindexscoresengland.xlsx"
    # exc4 = "dat/healthindexscoresengland.xlsx"
    # df4 = pd.read_excel(exc4, sheet_name="Table_2_Index_scores", header=2 )

    # df4 = (df4.rename(columns={"Area Type [Note 3]": "Area Type"})) #tranforming dataframe - renaming columns

    areatyp_select = st.selectbox("Please select an Area Type",
                                df4["Area Type"].unique()
                                )
    df4 = df4[df4["Area Type"]==areatyp_select]

    area_select = st.multiselect("Please select areas",
                                df4["Area Name"].unique()
                                )
    # if area_select is None:
    #     area_select = df4["Area Name"].unique()
    # else:


    df4 = df4[df4["Area Name"].isin(area_select)]
    #reverse-pivot the dataframe 

    df = (df4.melt(id_vars=['Area Code','Area Name','Area Type'], var_name='Year', value_name='Health Index')
            .sort_values(['Area Name','Year'])
            .reset_index(drop=True))

    col_1, col_2 = st.columns([0.3, 0.7])
    with col_1:

        st.dataframe(
                df,
                use_container_width=True
                )
    with col_2:
        st.plotly_chart(
                px.line(df, 
                            x="Year", 
                            y="Health Index", 
                            color="Area Name",
                            markers=True,
                            symbol="Area Name",
                            title=f'Overall Health Index for area type {areatyp_select}, over time')
            )
    st.header("Top areas by overall Health index for given year:", divider=True)
    year_sel = st.selectbox("Please select year",
                                df["Year"].unique()
                                )
    df_top_yr = df[df["Year"]==year_sel]
    st.dataframe(
        # df['Health Index'].nlargest(n=10)
        df_top_yr.nlargest(n=10, columns=['Health Index'], keep='all')
        
    )


with tab5:
    
    col1, col2, col3 = st.columns(3)

    col1.metric(label="KPI 1", value=52)

    col2.metric(label="KPI 2", value=30, delta=-5)

    col2.metric(label="KPI 3", value=12, delta=-7)

    col3.metric(label="KPI 4", value=1302)



