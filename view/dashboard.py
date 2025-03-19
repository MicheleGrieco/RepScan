import streamlit as st
import pandas as pd

def run_dashboard(reputation_scores_history):
    st.title("RepScan Dashboard: Trend della Reputazione Aziendale")
    st.write("Visualizza il trend del punteggio reputazionale nel tempo.")

    # reputation_scores_history: lista di dizionari con chiavi "timestamp" e "score"
    df = pd.DataFrame(reputation_scores_history)
    if df.empty:
        st.write("Nessun dato disponibile.")
        return

    # Converte la colonna 'timestamp' in formato datetime e ordina i dati
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')

    st.line_chart(df.set_index('timestamp')['score'])
    st.write("Dati grezzi:")
    st.dataframe(df)

if __name__ == "__main__":
    # Dati di esempio reali (puoi sostituirli con dati storici effettivi)
    reputation_scores_history = [
        {"timestamp": "2023-03-01 12:00:00", "score": 0.45},
        {"timestamp": "2023-03-02 12:00:00", "score": 0.50},
        {"timestamp": "2023-03-03 12:00:00", "score": 0.40},
        {"timestamp": "2023-03-04 12:00:00", "score": 0.35},
    ]
    run_dashboard(reputation_scores_history)
