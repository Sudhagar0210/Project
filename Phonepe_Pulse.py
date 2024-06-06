import streamlit as st
import pandas as pd
import plotly.express as px
import json
import requests
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Database connection
db_config = {
    'server': 'Sudhakar\\SQLEXPRESS01',
    'database': 'Local_database',
    'username': 'sa',
    'password': '123'
}
# SQL Server database
connection_string = f"mssql+pyodbc://{db_config['username']}:{db_config['password']}@{db_config['server']}/{db_config['database']}?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(connection_string)

# Title of Streamlit
st.title("Phonepe Pulse Data Visualization")

# Fetch the geojson data
geojson_file_path = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
response = requests.get(geojson_file_path)
data = json.loads(response.content)

States = [feature["properties"]["ST_NM"] for feature in data["features"]]
States.sort()

# Fetch data from the database
def fetch_data(query):
    try:
        return pd.read_sql(query, engine)
    except SQLAlchemyError as e:
        st.error(f"Error: {str(e)}")
        return pd.DataFrame()

# Queries
queries = {
    "Transaction": "select * from Aggregate_Transaction",
    "User": "SELECT * FROM Aggregate_User",
    "Insurance": "SELECT * FROM Aggregate_Insurance"
}

# Selectbox for visualization
visual = st.sidebar.selectbox(
    "Select Visualization:",
    ("Select", "Insurance", "Payments")
)

if visual == "Select":
    st.stop()
elif visual == "Insurance":
    df = fetch_data(queries["Insurance"])
elif visual == "Payments":
    payment_type = st.sidebar.selectbox(
        "Select Payment Type:",
        ("Transaction", "User")
    )
    if payment_type == "Transaction":
        df = fetch_data(queries["Transaction"])
    elif payment_type == "User":
        df = fetch_data(queries["User"])
else:
    df = None

#  Data exploration
st.sidebar.title("Explore Data Visualization")

# Year and Quarter options
years = ["Select", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]
quarters = ["Select", "Q1 (Jan-Mar)", "Q2 (Apr-Jun)", "Q3 (Jul-Sep)", "Q4 (Oct-Dec)"]

if visual == "Payments":
    selected_year = st.sidebar.selectbox("Select Year:", years)
    if selected_year != "Select":
        selected_quarter = st.sidebar.selectbox("Select Quarter:", quarters)
    else:
        selected_quarter = "Select"

# Button to submit selections
submit_button = st.sidebar.button("Submit")

# Apply filters and visualize data
if submit_button and df is not None and not df.empty:
    if visual == "Insurance":
        max_value = df["Transaction_amount"].max()
        fig = px.choropleth(
            df,
            geojson=data,
            featureidkey='properties.ST_NM',
            locations='States',
            color='Transaction_amount',
            color_continuous_scale='cividis',
            range_color=(0, max_value)
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)

    elif visual == "Payments":
        if payment_type == "Transaction" and selected_year != "Select":
            try:
                df['Year'] = df['Date'].dt.year
                df['Month'] = df['Date'].dt.month
            except Exception as e:
                st.error(f"Error in extracting Year and Month: {str(e)}")

            filtered_df = df[df["Year"] == int(selected_year)]
            if selected_quarter != "Select":
                quarters_map = {
                    "Q1 (Jan-Mar)": [1, 2, 3],
                    "Q2 (Apr-Jun)": [4, 5, 6],
                    "Q3 (Jul-Sep)": [7, 8, 9],
                    "Q4 (Oct-Dec)": [10, 11, 12]
                }
                filtered_df = filtered_df[filtered_df["Month"].isin(quarters_map[selected_quarter])]
            max_value = filtered_df["Transaction_amount"].max()
            fig = px.choropleth(
                filtered_df,
                geojson=data,
                featureidkey='properties.ST_NM',
                locations='States',
                color='Transaction_amount',
                color_continuous_scale='cividis',
                range_color=(0, max_value)
            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

        elif payment_type == "User" and selected_year != "Select":
            try:
                df['Year'] = df['Date'].dt.year
                df['Month'] = df['Date'].dt.month
            except Exception as e:
                st.error(f"Error in extracting Year and Month: {str(e)}")

            filtered_df = df[df["Year"] == int(selected_year)]
            if selected_quarter != "Select":
                quarters_map = {
                    "Q1 (Jan-Mar)": [1, 2, 3],
                    "Q2 (Apr-Jun)": [4, 5, 6],
                    "Q3 (Jul-Sep)": [7, 8, 9],
                    "Q4 (Oct-Dec)": [10, 11, 12]
                }
                filtered_df = filtered_df[filtered_df["Month"].isin(quarters_map[selected_quarter])]
            fig = px.choropleth(
                filtered_df,
                geojson=data,
                featureidkey='properties.ST_NM',
                locations='States',
                color='Transaction_amount',
                color_continuous_scale='cividis'
            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)