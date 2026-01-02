import streamlit as st

st.title("Football Studio Live")

if 'history' not in st.session_state:
    st.session_state.history = []

bankroll = st.number_input("Bankroll R$", 500, 5000, 1000)

# BOTÕES CORRETOS
col_b, col_p, col_t = st.columns(3)
if col_b.button("🔴 BANK", use_container_width=True):
    st.session_state.history.append('B')
if col_p.button("🔵 PLAYER", use_container_width=True):
    st.session_state.history.append('P')
if col_t.button("🟡 TIE", use_container_width=True):
    st.session_state.history.append('T')

if st.button("🗑️ Clear"):
    st.session_state.history = []

history = st.session_state.history[-12:]

if history:
    st.subheader("📈 Histórico Horizontal (últimos 12)")
    
    # HORIZONTAL EMOJIS
    hist_cols = st.columns(len(history))
    for i, res in enumerate(history):
        if res == 'B':
            hist_cols[i].markdown("**🔴**")
        elif res == 'P':
            hist_cols[i].markdown("**🔵**")
        else:
            hist_cols[i].markdown("**🟡**")
    
    # STREAK DETECTOR (2 reds detectado)
    streak_len = 1
    current = history[-1]
    for o in reversed(history[-6:]):
        if o == current:
            streak_len += 1
        else:
            break
    
    st.metric("Streak Atual", f"{current} x{streak_len}")
    
    # ALERTA 2+ reds
    if streak_len >= 2:
        bet = "🔵 PLAYER" if current == 'B' else "🔴 BANK"
        stake = int(bankroll * 0.015)
        st.warning(f"⚠️ Streak {streak_len}! Prepare {bet} R${stake}")
    elif streak_len >= 3:
        bet = "🔵 PLAYER" if current == 'B' else "🔴 BANK"
        st.error(f"🚨 APOSTE {bet} AGORA!")
    else:
        st.info("⏳ Aguarde streak 3+")
    
    # Stats simples
    p = history.count('P')
    b = history.count('B')
    col1, col2 = st.columns(2)
    col1.metric("Player %", f"{p/(p+b):.0%}" if p+b else "0%")
    col2.metric("Total", len(history))

st.caption("🔴 Bank Vermelho | 🔵 Player Azul | 2 reds = alerta!")
