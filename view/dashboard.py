import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from datetime import datetime, timedelta
import numpy as np
from config import DASHBOARD_TITLE, TARGET_COMPANY
from score_calculator import get_historical_scores
from sentiment_analysis import get_sentiment_label

def run_dashboard():
    """
    Avvia la dashboard Streamlit per visualizzare l'andamento del punteggio reputazionale
    """
    st.set_page_config(
        page_title=DASHBOARD_TITLE,
        page_icon="📊",
        layout="wide"
    )

    st.title(DASHBOARD_TITLE)
    st.markdown(f"Monitoraggio della reputazione online per **{TARGET_COMPANY}**")

    # Carica i dati storici
    df = get_historical_scores()

    if df.empty:
        st.warning("Nessun dato disponibile. Esegui prima l'analisi per raccogliere i dati.")
        return

    # Converti la colonna timestamp in datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Aggiungi una colonna per il sentiment label
    df['sentiment_label'] = df['score'].apply(get_sentiment_label)

    # Filtra i dati per intervallo di tempo
    col1, col2 = st.columns(2)
    with col1:
        period = st.selectbox(
            "Seleziona periodo",
            ["Ultimi 7 giorni", "Ultimi 30 giorni", "Ultimi 90 giorni", "Tutto"]
        )

    with col2:
        refresh = st.button("Aggiorna dati")

    # Applica il filtro
    if period == "Ultimi 7 giorni":
        cutoff = datetime.now() - timedelta(days=7)
        filtered_df = df[df['timestamp'] >= cutoff]
    elif period == "Ultimi 30 giorni":
        cutoff = datetime.now() - timedelta(days=30)
        filtered_df = df[df['timestamp'] >= cutoff]
    elif period == "Ultimi 90 giorni":
        cutoff = datetime.now() - timedelta(days=90)
        filtered_df = df[df['timestamp'] >= cutoff]
    else:
        filtered_df = df