import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Cricket Performance Analytics Dashboard", layout="wide")

st.title("🏏 Cricket Performance Data Analysis Dashboard")
st.markdown("Analyze team performances, player statistics, and run metrics dynamically.")

csv_filename = "cricket_data.csv"

if not os.path.exists(csv_filename):
    st.error(f"❌ Error: '{csv_filename}' file not found in the project folder! Please create it.")
else:
    try:
        df = pd.read_csv(csv_filename)
        
        st.sidebar.header("Filter Options")
        teams_list = ["All"] + list(df['Team'].unique())
        selected_team = st.sidebar.selectbox("Select Team", options=teams_list)

        if selected_team != "All":
            filtered_df = df[df['Team'] == selected_team]
        else:
            filtered_df = df

        # 4. Top KPI Metrics Display
        st.subheader("📊 Team Key Performance Indicators (KPI)")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(label="Total Players Selected", value=len(filtered_df))
        with col2:
            st.metric(label="Total Runs Scored", value=int(filtered_df['Runs'].sum()))
        with col3:
            st.metric(label="Total Wickets Taken", value=int(filtered_df['Wickets'].sum()))
        with col4:
            st.metric(label="Average Strike Rate", value=f"{filtered_df['Strike_Rate'].mean():.2f}")

        st.markdown("---")

        st.subheader("📈 Visual Data Insights")
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("### Runs Scored by Players")
            fig_runs = px.bar(
                filtered_df[filtered_df['Runs'] > 0], 
                x='Player_Name', 
                y='Runs', 
                color='Team',
                text='Runs',
                title="Player vs Total Runs"
            )
            st.plotly_chart(fig_runs, use_container_width=True)

        with chart_col2:
            st.markdown("### Bowler Performance (Wickets vs Economy)")
            bowlers_df = filtered_df[filtered_df['Wickets'] > 0]
            if not bowlers_df.empty:
                fig_wickets = px.scatter(
                    bowlers_df, 
                    x='Economy', 
                    y='Wickets', 
                    size='Wickets',
                    hover_name='Player_Name', 
                    color='Player_Name',
                    title="Wickets vs Economy Rate"
                )
                st.plotly_chart(fig_wickets, use_container_width=True)
            else:
                st.info("No bowling data available for the selected filters.")

        st.markdown("---")

        st.subheader("📋 Detailed Player Statistics Table")
        st.dataframe(filtered_df.sort_values(by="Runs", ascending=False), use_container_width=True)

    except Exception as e:
        st.error(f"Something went wrong while loading data: {e}")
