#This python file is used for creating the web applications and showing the visulizations.........\
from phone_pe import *
from sql import *
import streamlit as st
import plotly.express as px

st.set_page_config(page_title= "Phonepe Pulse Data Visualization and Exploration",
                   page_icon= "🇮🇳",
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app was created by `Shiva Raghav `!
                                        https://github.com/PhonePe/pulse"""}
                               )



tab_titles=["Home","Top Charts","Visualization"]

tabs = st.tabs(tab_titles)

with tabs[0]:
    st.sidebar.image("https://cdn.dribbble.com/users/1902890/screenshots/15619502/media/4110e14facc720955ac1ad0ae1589477.gif",width=310)

    # st.image("phonepeimg.png")
    st.title(" :violet[Phonepe Pulse Data Visualization and Exploration ]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, Streamlit, and Plotly.")
        st.markdown(
            "### :violet[Overview :] This visualization allows you to explore and analyze PhonePe's Pulse data from 2018 to 2022. With interactive charts and various metrics to choose, you can gain insights into PhonePe's business performance and growth over time.")

    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")

        st.image("https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif", width=450)

st.sidebar.header(":violet[Phonepe_Pulse]")

with tabs[1]:
    st.markdown("## :violet[Top Charts bsaed on States and Districts data]")
    Type = st.sidebar.selectbox("**Type**", ("TRANSACTION", "USERS"),key="selectbox1")
    colum1, colum2 = st.columns([1, 1.5], gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022,key="slider1")
        Quarter = st.slider("Quarter", min_value=1, max_value=4,key="slider2")

    with colum2:
        st.info(
            """
            #### From this Tab we can get insights like :
            - Overall ranking on a particular Year and Quarter.
            - Top 10 State, District based on Total number of transaction and Total amount spent on phonepe.
            - Top 10 State, District based on Total phonepe users and their app opening frequency.
            - Top 10 mobile brands and its percentage of users.
            """, icon="🔍"
        )

    # Top Charts bsaed on States and Districts data - TRANSACTIONS
    if Type == "TRANSACTION":
        col1, col2 = st.columns([1, 1], gap="medium")

        with col1:
            st.markdown("### :violet[State]")
            cursor.execute(
                f"select State, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amounts) as Total from agg_trans where year = {Year} and quarter = {Quarter} group by State order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count', 'Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                         names='State',
                         title='Top 10 ',
                         color_discrete_sequence=px.colors.sequential.Viridis,
                         # color_discrete_sequence=px.colors.sequential.Purples,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

            fig = px.bar(df,
                         title='top 10 ',
                         x="State",
                         y="Total_Amount",
                         orientation='v',
                         color='Total_Amount',
                         color_continuous_scale=px.colors.sequential.Viridis)

            st.plotly_chart(fig, use_container_width=False)

        with col2:
            st.markdown("### :violet[District]")
            cursor.execute(f"select District , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by District order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                         names='District',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Viridis,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

            fig = px.bar(df,
                         title='top 10',
                         x="District",
                         y="Total_Amount",
                         orientation='v',
                         color='Total_Amount',
                         color_continuous_scale=px.colors.sequential.Viridis)

            st.plotly_chart(fig, use_container_width=False)

    # Top Charts - USERS
    if Type == "USERS":
        col1, col2, col3 = st.columns([1, 1, 1], gap="small")

        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2, 3, 4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                cursor.execute(
                    f"select brand, sum(Count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brand order by Total_Count desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Users', 'Avg_Percentage'])
                fig = px.pie(df, values='Total_Users',
                             names='Brand',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Viridis,
                             hover_data=['Avg_Percentage'],
                             labels={'Avg_Percentage': 'Avg_Percentage'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)


        with col2:
            st.markdown("### :violet[District]")
            cursor.execute(
                f"select District, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by District order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users', 'Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)

            fig = px.pie(df, values='Total_Users',
                         names='District',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Viridis,
                         hover_data=['Total_Users'],
                         labels={'Total_Users': 'Total_Users'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            st.markdown("### :violet[State]")
            cursor.execute(
                f"select State, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by State order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                         names='State',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Appopens'],
                         labels={'Total_Appopens': 'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    Year1 = st.slider("**Year**", min_value=2018, max_value=2022,key="slider3")
    Quarter1 = st.slider("Quarter", min_value=1, max_value=4,key="slider4")
    # Type = st.sidebar.selectbox("**Type**", ("TRANSACTION", "USERS"),key="selectbox2")
    col1, col2 = st.columns(2)
    india_states = json.load(open(r"C:\Users\SHIVA\Downloads\states_india.geojson",'r'))

    # EXPLORE DATA - TRANSACTIONS
    if Type == "TRANSACTION":
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            cursor.execute(
                f"select State, sum(Count) as Total_Transactions, sum(Amount) as Total_amount from map_trans where year = {Year1} and quarter = {Quarter1} group by State order by State")
            df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
            # st.dataframe(df1)
            df2 = pd.read_csv(r'C:\Users\SHIVA\Documents\statenames.csv')
            df1.State = df2
            # st.dataframe(df1)
            fig = px.choropleth(df1,
                                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                    featureidkey='properties.ST_NM',
                                    locations='State',
                                    color='Total_amount',
                                    color_continuous_scale='plotly3')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            cursor.execute(
                f"select State, sum(Count) as Total_Transactions, sum(Amount) as Total_amount from map_trans where year = {Year1} and quarter = {Quarter1} group by State order by State")
            df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv(r'C:\Users\SHIVA\Documents\statenames.csv')
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            # st.dataframe(df1)
            df1.State = df2
            # st.dataframe(df1)

            fig = px.choropleth(df1,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_Transactions',
                                color_continuous_scale='plotly3')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

        # BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        cursor.execute(
            f"select Transaction_method, sum(Transaction_count) as Total_Transactions, sum(Transaction_amounts) as Total_amount from agg_trans where year= {Year1} and quarter = {Quarter1} group by transaction_method order by Transaction_method")
        df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_type', 'Total_Transactions', 'Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=False)
    #
    #     # BAR CHART TRANSACTIONS - DISTRICT WISE DATA
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                                      ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam',
                                       'bihar',
                                       'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi',
                                       'goa', 'gujarat', 'haryana',
                                       'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala',
                                       'ladakh', 'lakshadweep',
                                       'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                       'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                       'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand',
                                       'west-bengal'), index=30)

        cursor.execute(
            f"select State, District,Year,Quarter, sum(Count) as Total_Transactions, sum(Amount) as Total_amount from map_trans where year = {Year1} and quarter = {Quarter1} and State = '{selected_state}' group by State, District,Year,Quarter order by State,District")

        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'District', 'Year', 'Quarter',
                                                         'Total_Transactions', 'Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

    # # EXPLORE DATA - USERS
    if Type == "USERS":
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        if Year1 == 2018 and Quarter1 in [1,2, 3, 4] or Year1 == 2019 and Quarter1 == 1 :
            st.markdown("#### Sorry No Data to Display ")

        else:
            # Overall State Data - TOTAL APPOPENS - INDIA MAP
            # st.markdown("## :violet[Overall State Data - User App opening frequency]")
            cursor.execute(
                f"select State, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year1} and quarter = {Quarter1} group by State order by State")
            df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
            df2 = pd.read_csv(r'C:\Users\SHIVA\Documents\statenames.csv')
            df1.Total_Appopens = df1.Total_Appopens.astype(float)
            df1.State = df2
            fig = px.choropleth(df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Total_Appopens',
                            color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

        # # BAR CHART TOTAL UsERS - DISTRICT WISE DATA
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                                      ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam',
                                       'bihar',
                                       'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi',
                                       'goa', 'gujarat', 'haryana',
                                       'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala',
                                       'ladakh', 'lakshadweep',
                                       'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                       'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                       'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand',
                                       'west-bengal'), index=30)

        cursor.execute(
            f"select District,sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where Year = {Year1} and Quarter = {Quarter1} and State = '{selected_state}' group by State, District,Year,Quarter order by State,District")

        df = pd.DataFrame(cursor.fetchall(),
                          columns=[ 'District', 'Total_Users', 'Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)

        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)
