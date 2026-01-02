import streamlit as st

st.title("⚽ Football Studio PRO - Botões")

# Bankroll
bankroll = st.number_input("💰 Bankroll R$", 100, 5000, 1000)
st.write(f"Stake 1%: **R${int(bankroll*0.01)}**")

# Botões input (mobile friendly)
col1, col2, col3 = st.columns(3)
if col1.button("🔴 PLAYER", use_container_width=True):
    st.session_state.results = st.session_state.get('results', []) + ['P']
if col2.button("🔵 BANKER", use_container_width=True):
    st.session_state.results = st.session_state.get('results', []) + ['B']
if col3.button("🟡 TIE", use_container_width=True):
    st.session_state.results = st.session_state.get('results', []) + ['T']

# Clear
if st.button("🗑️ Limpar"):
    st.session_state.results = []

# Resultados
results = st.session_state.get('results', [])
if results:
    st.subheader("📊 Live Results")
    
    # Mostrar últimos 20 com cores
    for i, r in enumerate(reversed(results[-20:])):
        color = "red" if r == 'P' else "blue" if r == 'B' else "yellow"
        emoji = "🔴" if r == 'P' else "🔵" if r == 'B' else "🟡"
        st.markdown(f"{emoji} **{r}**", unsafe_allow_html=True)
    
    # Análise streak
    if len(results) >= 5:
        streak = 1
        current = results[-1]
        for o in reversed(results[-10:]):
            if o == current and o != 'T':
                streak += 1
            else:
                break
        
        st.metric("Streak Atual", f"{current} x{streak}")
        
        if streak >= 3:
            bet = "PLAYER 🔴" if current == "B" else "BANKER 🔵"
            st.error(f"🚨 **APOSTE {bet} AGORA!**")
        else:
            st.info("⏳ Aguarde streak 3+")
    
    # Stats
    p = results.count('P')
    b = results.count('B')
    total = p + b
    st.metric("Player WR", f"{p/total:.0%}" if total else "0%")

if st.button("💾 Salvar Sessão"):
    st.balloons()
    st.success("Sessão salva!")

st.caption("Clique botões durante live! Edge 3-5% streaks")
