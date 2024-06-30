import streamlit as st
import pandas as pd
import plotly.express as px
import pymysql
import numpy as np
import requests
import json
import pyodbc


 
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Sudhakar\\SQLEXPRESS01;DATABASE=Local_database;UID=sa;PWD=123')
cursor = conn.cursor()



# Comfiguring Streamlit GUI 
st.set_page_config(layout='wide')

# title
st.header(':violet[Phonepe Pulse Data Visualization ]')
st.write('**(Note)**:-This data between **2018** to **2024(Till Qtr 1)** in **All Over INDIA**')

# Selection option
option = st.radio('**Select your option**',('All India','Top Ten categories'),horizontal=True)



if option == 'All India':

    # Select tab
    tab1, tab2 = st.tabs(['Transaction','User'])

    with tab1:
        col1,col2,col3 = st.columns([0.3, 0.3, 0.5])

        with col1:
            ina_tran_year = st.selectbox('**Select Transaction Year**',('2018','2019','2020','2021','2022','2023','2024'),key='ina_tran_year')

        with col2:
            ina_tran_qter = st.selectbox('**Select Quarter**',('1','2','3','4'),key='ina_tran_qter')

        with col3:
            ina_tran_type = st.selectbox('**Select Transaction Type**',('Merchant payments','Financial Services','Recharge & bill payments',
                                                                       'Peer-to-peer payments','Others'))
            

        #SQL Query Execution

        # SQL Query Execution
        def execute_query(query):
            cursor.execute(query)
            return cursor.fetchall()



        # Transaction  Bar Chart Query
        ina_tran_qry_result = execute_query (f"Select States, Transaction_amount  from Aggregate_Transaction where Year = '{ina_tran_year}' AND Quarter = '{ina_tran_qter} 'AND Transaction_type = '{ina_tran_type}'")
        if ina_tran_qry_result:

            df_ina_tran_qry_result = pd.DataFrame(np.array(ina_tran_qry_result), columns=['States', 'Transaction_amount'])
            df_ina_tran_qry_result1 = df_ina_tran_qry_result.set_index(pd.Index(range(1, len(df_ina_tran_qry_result) + 1)))
        else:
            df_ina_tran_qry_result1 = pd.DataFrame(columns=['States', 'Transaction_amount'])

        # Transaction Table Query
        ina_tran_table_qry_result= execute_query(f"Select States, Transaction_count, Transaction_amount  from Aggregate_Transaction where Year = '{ina_tran_year}' AND Quarter = '{ina_tran_qter} 'AND Transaction_type = '{ina_tran_type}'")
        if ina_tran_table_qry_result:

            df_ina_tran_table_qry_result = pd.DataFrame(np.array(ina_tran_table_qry_result),columns=['States','Transaction_count','Transaction_amount'])
            df_ina_tran_table_qry_result1 = df_ina_tran_table_qry_result.set_index(pd.Index(range(1, len(df_ina_tran_table_qry_result)+1)))
        else:
            df_ina_tran_table_qry_result1 = pd.DataFrame(columns=['States','Transaction_count','Transaction_amount'])

        #  Total Transaction Amount Query
        ina_tran_amt_qry_result= execute_query (f"Select SUM(Transaction_amount), AVG(Transaction_amount)  from Aggregate_Transaction where Year = '{ina_tran_year}' AND Quarter = '{ina_tran_qter} 'AND Transaction_type = '{ina_tran_type}'")
        if ina_tran_amt_qry_result: 

            df_ina_tran_amt_qry_result = pd.DataFrame(np.array(ina_tran_amt_qry_result),columns=['Total Amount','Average Amount'])
            df_ina_tran_amt_qry_result1 = df_ina_tran_amt_qry_result.set_index(['Average Amount'])
        else:
            df_ina_tran_amt_qry_result1 = pd.DataFrame(columns=['Total Amount','Average Amount'])

            
        # Total Transaction Count Query
        ina_tran_cunt_qry_result = execute_query (f"Select SUM(Transaction_count), AVG(Transaction_count)  from Aggregate_Transaction where Year = '{ina_tran_year}' AND Quarter = '{ina_tran_qter} 'AND Transaction_type = '{ina_tran_type}'")
        if ina_tran_cunt_qry_result:

            df_ina_tran_cunt_qry_result = pd.DataFrame(np.array(ina_tran_cunt_qry_result),columns=['Total Transaction Count','Average Transaction Count'])
            df_ina_tran_cunt_qry_result1 = df_ina_tran_cunt_qry_result.set_index(['Average Transaction Count'])
        else:
            df_ina_tran_cunt_qry_result1 = pd.DataFrame(columns=['Total Transaction Count','Average Transaction Count'])


        # Select Visual Type

        tab1_1 , tab1_2 , tab1_3 = st.tabs(['Geo visualization','Bar chart','Total calculation'])

        with tab1_1 :

            geojson_file_path ="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(geojson_file_path)
            data = json.loads(response.content)

            States_name_tra = [feature["properties"]["ST_NM"] for feature in data["features"]]
            States_name_tra.sort()

            df_states_name_tra = pd.DataFrame({'States': States_name_tra})

            # Ensure column exists in both DataFrames for merge
            if 'States' in df_states_name_tra.columns and 'States' in df_ina_tran_qry_result.columns:
                df_states_name_tra = df_states_name_tra.merge(df_ina_tran_qry_result, on='States', how='left')
            else:
                st.write("Merge operation failed: 'States' column missing in one of the DataFrames")               

          
            
            fig_tran = px.choropleth(
                data_frame=df_states_name_tra,     
                geojson=data,
                featureidkey='properties.ST_NM',
                locations='States',
                color='Transaction_amount',
                color_continuous_scale='cividis',
                title = 'Transaction Analysis'           
        )
        fig_tran.update_geos(fitbounds="locations", visible=False)
        #st.plotly_chart(fig_tran, use_container_width=True)
        fig_tran.update_layout(title_font=dict(size=33),title_font_color='#6739b7',height=800)
        st.plotly_chart(fig_tran,use_container_width=True)


        # Bar Chart Analysis

        with tab1_2:
            df_ina_tran_qry_result1['States']= df_ina_tran_qry_result1['States'].astype(str)
            df_ina_tran_qry_result1['Transaction_amount'] = df_ina_tran_qry_result1['Transaction_amount'].astype(float)

            bar_fig = px.bar(df_ina_tran_qry_result1 , x='States', y='Transaction_amount' , color='Transaction_amount',color_continuous_scale='thermal',
                             title='Transaction Analysis Chart',height=700)
            bar_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
            st.plotly_chart(bar_fig,use_container_width=True)

        # All India Total Calcuation

        with tab1_3:

            st.header(':violet[Total Transaction Calcuation]')

            col4,col5 = st.columns(2)

            with col4:
                st.subheader ('Transaction Aanlysis Details')
                st.dataframe (df_ina_tran_table_qry_result1)

            with col5:
                st.subheader ('Transaction Amount')
                st.dataframe (df_ina_tran_amt_qry_result1)
                st.subheader ('Transaction Count')
                st.dataframe (df_ina_tran_cunt_qry_result1)



                        #----------------------- All  Over India user -----------------------#

    with tab2:
        col_1, col_2 = st.columns(2)

        with col_1:
                        
            ina_user_year = st.selectbox('**Select User Year**',('2018','2019','2020','2021','2022','2023','2024'),key='ina_user_year')

        with col_2:
            ina_user_qter = st.selectbox('**Select Quarter**',('1','2','3','4'),key='ina_user_qter')

        # Visual Tabs
        tab2_1, tab2_2, tab2_3 = st.tabs(['Geo visualization','Bar chart','Total calculation'])

        with tab2_1:
            try:

            # user sql query execute
                ina_user_qry_result = execute_query (f"Select States, SUM(User_count)  from Aggregate_User where Year = '{ina_user_year}' AND Quarter = '{ina_user_qter}' GROUP BY States")
                if ina_user_qry_result:

                    df_ina_user_qry_result = pd.DataFrame(np.array(ina_user_qry_result), columns=['States', 'User_count'])
                    df_ina_user_qry_result1 = df_ina_user_qry_result.set_index(pd.Index(range(1, len(df_ina_user_qry_result) + 1)))
                else:
                    df_ina_user_qry_result1 = pd.DataFrame(columns=['States', 'User_count'])



                # ------    /  Geo visualization dashboard for User  /   ---- #   

                States_name_user = [feature["properties"]["ST_NM"] for feature in data["features"]]
                States_name_user.sort()

                df_States_name_user = pd.DataFrame({'States': States_name_user})            

                

                # Ensure column exists in both DataFrames for merge             
                if 'States' in df_States_name_user.columns and 'States' in df_ina_user_qry_result.columns:
                    df_states_name_user = df_States_name_user.merge(df_ina_user_qry_result, on='States', how='left')
                else:
                    st.write("Merge operation failed: 'States' column missing in one of the DataFrames")
    


                fig_user = px.choropleth(
                    data_frame=df_states_name_user,     
                    geojson=data,
                    featureidkey='properties.ST_NM',
                    locations='States',
                    color='User_count',
                    color_continuous_scale='cividis',
                    title='User Analysis'           
                )
                fig_user.update_geos(fitbounds="locations", visible=False)
                fig_user.update_layout(title_font=dict(size=33), title_font_color='#6739b7', height=800)
                st.plotly_chart(fig_user, use_container_width=True) 

            except Exception as e:
                st.error("For the selected 2023 and 2024 User transaction data not available in Database.")         



        with tab2_2:
        # Bar Chart Analysis
            try:

                ina_user_qry_result = execute_query (f"Select States, SUM(User_count)  from Aggregate_User where Year = '{ina_user_year}' AND Quarter = '{ina_user_qter}' GROUP BY States")
                if ina_user_qry_result:

                    df_ina_user_qry_result = pd.DataFrame(np.array(ina_user_qry_result), columns=['States', 'User_count'])
                    df_ina_user_qry_result1 = df_ina_user_qry_result.set_index(pd.Index(range(1, len(df_ina_user_qry_result) + 1)))
                else:
                    df_ina_user_qry_result1 = pd.DataFrame(columns=['States', 'User_count'])


                df_ina_user_qry_result1['States']= df_ina_user_qry_result1['States'].astype(str)
                df_ina_user_qry_result1['User_count'] = df_ina_user_qry_result1['User_count'].astype(int)

                user_bar_fig = px.bar(df_ina_user_qry_result1 , x='States', y='User_count' , color='User_count',color_continuous_scale='thermal',
                                title='User Analysis Chart',height=700)
                user_bar_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                st.plotly_chart(user_bar_fig,use_container_width=True)

            except Exception as e:
                st.error("For the selected 2023 and 2024 User transaction data not available in Database.")  

        with tab2_3:
            try:
                # Total User Calculation
                ina_user_tot_result = execute_query(f"Select SUM(User_count), AVG(User_count) from Aggregate_User where Year = '{ina_user_year}' AND Quarter = '{ina_user_qter}'")
                if ina_user_tot_result:
                    df_ina_user_tot_result = pd.DataFrame(np.array(ina_user_tot_result), columns=['Total User', 'Average User'])
                    df_ina_user_tot_result1 = df_ina_user_tot_result.set_index(['Average User'])
                else:
                    df_ina_user_tot_result1 = pd.DataFrame(columns=['Total User', 'Average User'])

                # All India Total Calculation
                st.header(':violet[Total User Calculation]')

                col_3, col_4 = st.columns(2)

                with col_3:
                    st.subheader('User Analysis Details')
                    st.dataframe(df_ina_user_qry_result1)

                with col_4:
                    st.subheader('Total User Count')
                    st.dataframe(df_ina_user_tot_result1['Total User'])                   

            except Exception as e:
                 st.error("For the selected 2023 and 2024 User transaction data not available in Database.")


                 #---------------------------------- Top Ten categories  -------------------------------------#

else:

    tab3, tab4 = st.tabs(['Transaction','User'])

    with tab3:
        top_tran_year = st.selectbox('**Select User Year**',('2018','2019','2020','2021','2022','2023','2024'),key='top_tran_year')


        # SQL Query Execution










