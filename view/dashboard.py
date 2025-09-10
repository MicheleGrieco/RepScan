import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from datetime import datetime, timedelta
import numpy as np
from configuration.config import DASHBOARD_TITLE, TARGET_COMPANY
from tools.score_calculator import ReputationScoreCalculator
from tools.sentiment_analysis import SentimentAnalyzer

def run_dashboard() -> None:
    """
    Run Streamlit dashboard to visualize reputation score trends
    """
    st.set_page_config(
        page_title=DASHBOARD_TITLE,
        page_icon="📊",
        layout="wide"
    )

    st.title(DASHBOARD_TITLE)
    st.markdown(f"Online reputation monitoring for **{TARGET_COMPANY}**")

    # Load historical scores
    df = ReputationScoreCalculator().get_historical_scores()

    if df.empty:
        st.warning("No data available, run data collection analysis first.")
        return

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Add sentiment labels
    df['sentiment_label'] = df['score'].apply(SentimentAnalyzer.get_sentiment_label)

    # Time period filter
    col1, col2 = st.columns(2)
    with col1:
        period = st.selectbox(
            "Select time period",
            ["Last 7 days", "Last 30 days", "Last 90 days", "Everytime"]
        )

    # Refresh button
    with col2:
        refresh = st.button("Update Data")

    # Apply time period filter
    if period == "Last 7 days":
        cutoff = datetime.now() - timedelta(days=7)
        filtered_df = df[df['timestamp'] >= cutoff]
    elif period == "Last 30 days":
        cutoff = datetime.now() - timedelta(days=30)
        filtered_df = df[df['timestamp'] >= cutoff]
    elif period == "Last 90 days":
        cutoff = datetime.now() - timedelta(days=90)
        filtered_df = df[df['timestamp'] >= cutoff]
    else:
        filtered_df = df