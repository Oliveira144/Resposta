import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🎯 Football Studio Analyzer - Recupera R$5k")

# INPUTS
outcomes_str = st.text_area(
    "📝 Resultados LIVE (P/B/T, 1 por linha)", 
    height=200,
    placeholder="P
B
P
B
B"
)

bankroll = st.number_input("💰 Bankroll (R$)", value=1000.0)

if outcomes_str.strip():
    # CORRIGIDO: Split seguro
    outcomes = []
    for line in outcomes_str.split("
"):
        clean = line.strip().upper()
        if clean in ['P', 'B', 'T']:
            outcomes.append(clean)
    
    if len(outcomes) >= 10:
        df = pd.DataFrame({'Rodada': range(len(outcomes)), 'Resultado': outcomes})
        
        # Streaks
        streaks = []
        if outcomes:
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
        
        # RECOMENDAÇÃO
        recent_streaks = streaks[-3:]
        col1, col2 = st.columns(2)
        
        if len(recent_streaks) >= 2 and recent_streaks[-1][1] >= 3:
            contra = 'PLAYER' if recent_streaks[-1][0] == 'B' else 'BANKER'
            stake = bankroll * 0.015
            col1.error(f"🚨 **APOSTE {contra}!** Stake: R${stake:.0f}")
            col1.metric("Edge Estimado", "5%")
        else:
            col1.warning("⏳ Aguarde streak 3+")
        
        # Stats
        non_tie = [o for o in outcomes if o != 'T']
        col2.metric("Player Winrate", f"{non_tie.count('P')/len(non_tie):.1%}")
        col2.metric("Banker Winrate", f"{non_tie.count('B')/len(non_tie):.1%}")
        
        # Gráfico
        fig = px.line(df.tail(20), x='Rodada', y='Resultado', 
                     markers=True, title="Últimas 20 Rodadas")
        st.plotly_chart(fig, use_container_width=True)
        
        st.success(f"📊 {len(outcomes)} rodadas processadas | Streaks >3: {sum(c >= 3 for _, c in streaks)}")

st.caption("Deploy: streamlit run app.py | ROI alvo 3-5% com streaks")
