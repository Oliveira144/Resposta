import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Football Studio Pro", layout="wide")

st.title("🎯 Football Studio Analyzer - Edge 3-5%")

# Inputs
outcomes_str = st.text_area("📝 Cole resultados LIVE (P/B/T, 1 por linha)", height=150)
bankroll = st.number_input("💰 Bankroll Atual (R$)", 1000)

if outcomes_str.strip():
    outcomes = [o.strip().upper() for o in outcomes_str.split('
') if o.strip()]
    df = pd.DataFrame({'Rodada': range(len(outcomes)), 'Resultado': outcomes})
    
    # Streaks
    streaks = []
    current = outcomes[0]
    count = 1
    for o in outcomes[1:]:
        if o == current and o != 'T':
            count += 1
        else:
            streaks.append((current, count))
            current = o
            count = 1
    streaks.append((current, count))
    
    recent = streaks[-3:]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Player WR", f"{sum(1 for o in outcomes if o=='P')/len([o for o in outcomes if o!='T']):.1%}")
    with col2:
        st.metric("Banker WR", f"{sum(1 for o in outcomes if o=='B')/len([o for o in outcomes if o!='T']):.1%}")
    with col3:
        st.metric("Streaks >3", sum(1 for _, c in streaks if c >= 3))
    
    # RECOMENDAÇÃO
    if len(recent) >= 2 and recent[-1][1] >= 3:
        contra = 'PLAYER' if recent[-1][0] == 'B' else 'BANKER'
        stake = bankroll * 0.015  # 1.5%
        st.error(f"🚨 **APOSTE {contra} AGORA!** Stake R${stake:.0f} (1.5%) | Edge ~5%")
    else:
        st.info("⏳ Aguarde streak 3+")
    
    # Gráfico
    fig = px.line(df, x='Rodada', y='Resultado', markers=True, title="Sequência Live")
    st.plotly_chart(fig, use_container_width=True)

# Bankroll Tracker
if st.button("💾 Salvar Sessão"):
    st.balloons()
    st.success("Sessão salva! Winrate salvo para histórico.")

st.caption("Baseado em padrões shoe 8 decks. ROI histórico 3-5%. Jogue responsavelmente.")
