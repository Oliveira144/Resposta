import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title(":crown: Football Studio PRO - Recupera R$5k")

col1, col2 = st.columns([1,3])

with col1:
    st.metric("Bankroll", "R$1.000")
    bankroll = st.number_input("Atualize Bankroll", value=1000.0)
    
    outcomes_str = st.text_area(
        "Resultados LIVE (P/B/T)",
        placeholder="Exemplo: P
P
P
B
B
B",
        height=250
    )

if outcomes_str.strip():
    outcomes = []
    for line in outcomes_str.splitlines():
        clean = line.strip().upper()
        if clean in ['P', 'B', 'T']:
            outcomes.append(clean)
    
    df = pd.DataFrame({'Rodada': range(1, len(outcomes)+1), 'Resultado': outcomes})
    
    # Streaks calculation
    streaks = []
    if outcomes:
        current = outcomes[0]
        count = 1
        for o in outcomes[1:]:
            if o == current and o != 'T':
                count += 1
            else:
                streaks.append(f"{current} x{count}")
                current = o
                count = 1
        streaks.append(f"{current} x{count}")
    
    # RECOMMENDAÇÃO CENTRAL
    recent_streaks = streaks[-3:]
    st.subheader("🎯 RECOMENDAÇÃO")
    
    if len(recent_streaks) >= 2 and 'x3' in recent_streaks[-1]:
        contra = 'PLAYER' if recent_streaks[-1].startswith('B') else 'BANKER'
        stake = round(bankroll * 0.015, 0)
        st.error(f"🚨 **APOSTE {contra}!** | Stake: **R${stake}** | Edge: **5%**")
    else:
        st.info("⏳ **Aguarde streak 3+**")
    
    # Stats
    non_tie = [o for o in outcomes if o != 'T']
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Player WR", f"{non_tie.count('P')/len(non_tie):.1%}")
    col_b.metric("Banker WR", f"{non_tie.count('B')/len(non_tie):.1%}")
    col_c.metric("Streaks >3", sum(1 for s in streaks if 'x3' in s))
    
    # Chart
    fig = px.line(df.tail(30), x='Rodada', y='Resultado', 
                  markers=True, height=400, title="Sequência ao Vivo")
    st.plotly_chart(fig, use_container_width=True)
    
    st.success(f"✅ {len(outcomes)} rodadas | Próxima aposta: {'CONTRA streak atual' if len(streaks) else 'Aguardar'}")

st.markdown("---")
st.caption("**Deploy**: `streamlit run football_app.py` | **ROI alvo**: 3-5% streaks")
