"""
Module name: dashboard.py
Author: Michele Grieco
Description:
    This module contains the ReputationDashboard class for managing and displaying
    the reputation monitoring dashboard using Streamlit. It includes methods for
    data loading, filtering, and visualization.
Usage:
    from view.dashboard import ReputationDashboard
    dashboard = ReputationDashboard()
    dashboard.run()
"""

import streamlit as st # for dashboard
import pandas as pd # for data manipulation
import matplotlib.pyplot as plt # for plotting
import altair as alt # for interactive visualizations
from datetime import datetime, timedelta
import numpy as np # for numerical operations
from configuration.config import DASHBOARD_TITLE, TARGET_COMPANY
from tools.score_calculator import ReputationScoreCalculator
from tools.sentiment_analysis import SentimentAnalyzer

class ReputationDashboard:
    """
    Class for managing and displaying the reputation monitoring dashboard
    """
    
    def __init__(self) -> None:
        """
        Initialize the dashboard with the configuration and data loading
        
        Args:
            title (str): Title of the dashboard
            target_company (str): Company being monitored
            score_calculator (ReputationScoreCalculator): Instance for score calculations
            df (pandas.DataFrame): Dataframe to hold historical scores
        """
        self.title = DASHBOARD_TITLE
        self.target_company = TARGET_COMPANY
        self.score_calculator = ReputationScoreCalculator()
        self.df = None
        
    def _setup_page(self) -> None:
        """
        Configure the Streamlit page settings
        
        Args:
            title (str): Title of the dashboard
            icon (str): Icon for the dashboard
            layout (str): Layout setting for the dashboard
        Returns:
            None
        """
        st.set_page_config(
            page_title=self.title,
            page_icon="📊",
            layout="wide"
        )
        
        st.title(self.title)
        st.markdown(f"Online reputation monitoring for **{self.target_company}**")

    def _load_data(self) -> bool:
        """
        Load and preprocess historical score data
        
        Args:
            None
        Returns:
            bool: True if data loaded successfully, False otherwise
        """
        self.df = self.score_calculator.get_historical_scores()
        
        if self.df.empty:
            st.warning("No data available, run data collection first.")
            return False
        
        # Convert timestamp to datetime    
        self.df['timestamp'] = pd.to_datetime(self.df['datetime'])
        
        # Add sentiment labels
        self.df['sentiment_label'] = self.df['score'].apply(SentimentAnalyzer.get_sentiment_label)
        
        return True
        
    def _create_filters(self) -> str:
        """
        Create and handle time period filters
        
        Args:
            None
        Returns:
            str: Selected time period
        """
        col1, col2 = st.columns(2)
        
        with col1:
            period = st.selectbox(
                "Select time period",
                ["Last 7 days", "Last 30 days", "Last 90 days", "All"]
            )
            
        with col2:
            refresh = st.button("Update Data")
            
        return period
        
    def _filter_data(self, period) -> pd.DataFrame | None:
        """
        Filter data based on selected time period
        
        Args:
            period (str): Selected time period
        Returns:
            pandas.DataFrame: Filtered dataframe
        """
        if period == "Last 7 days":
            cutoff = datetime.now() - timedelta(days=7)
            return self.df[self.df['timestamp'] >= cutoff] # type: ignore
        elif period == "Last 30 days":
            cutoff = datetime.now() - timedelta(days=30)
            return self.df[self.df['timestamp'] >= cutoff] # type: ignore
        elif period == "Last 90 days":
            cutoff = datetime.now() - timedelta(days=90)
            return self.df[self.df['timestamp'] >= cutoff] # type: ignore
        else:
            return self.df
        
    def run(self):
        """
        Run the dashboard
        
        Args:
            None
        Returns:
            None
        """
        self._setup_page()
        
        if not self._load_data():
            return
        
        period = self._create_filters()
        filtered_df = self._filter_data(period)
        
        # Add graph visualization using filtered_df
        
        
def run_dashboard() -> None:
    """
    Create and run the dashboard
    Args:
        None
    Returns:
        None
    """
    dahsboard = ReputationDashboard()
    dahsboard.run()