import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Football Studio PRO")

# SIMPLES - SEM multiline problem
outcomes_str = st.text_area("Digite resultados (P B T):", "P P P B B B")
bankroll = st.slider("Bankroll R$", 100, 5000, 1000)

if outcomes_str:
    outcomes = [o.strip().upper() for o in outcomes_str.split() if o in ['P','B','T']]
    
    if len(outcomes) > 5:
        df = pd.DataFrame({'rodada':range(len(outcomes)), 'res':outcomes})
        
        # Streaks simples
        streak = 1
        current = outcomes[-1]
        for o in reversed(outcomes[-10:]):
            if o != current:
                break
            streak += 1
        
        st.subheader("RECOMENDACAO")
        if streak >= 3:
            bet = "PLAYER" if current == "B" else "BANKER"
            stake = bankroll * 0.01
            st.error(f"APOSTE {bet}! Stake R${stake:.0f}")
        else:
            st.info("Aguarde streak 3+")
        
        # Chart
        fig = px.scatter(df.tail(20), x='rodada', y='res', size_max=10)
        st.plotly_chart(fig)
        
        st.success(f"{len(outcomes)} rodadas | Streak atual: {current} x{streak}")

st.caption("Teste: digite P P P B B B")
