import streamlit as st

st.title("Football Studio Live")

if 'history' not in st.session_state:
    st.session_state.history = []

bankroll = st.number_input("Bankroll R$", 500, 5000, 1000)

# Botões
col1, col2, col3 = st.columns(3)
if col1.button("🔴 BANK"):
    st.session_state.history.append('B')
if col2.button("🔵 PLAYER"):
    st.session_state.history.append('P')
if col3.button("🟡 TIE"):
    st.session_state.history.append('T')

if st.button("Clear"):
    st.session_state.history = []

history = st.session_state.history[-10:]

# Sugestão direta TOPO
st.markdown("### 🚨 SUGESTÃO")
if len(history) >= 3:
    streak = 1
    current = history[-1]
    for o in reversed(history[-5:]):
        if o == current:
            streak += 1
        else:
            break
    
    if streak >= 3:
        bet = "PLAYER 🔵" if current == 'B' else "BANK 🔴"
        stake = int(bankroll * 0.01)
        st.error(f"**{bet} R${stake}**")
    else:
        st.info("**Aguarde streak 3+**")

# Histórico horizontal RECENTE ← ANTIGO
if history:
    st.subheader("Histórico")
    hist_rev = list(reversed(history[-8:]))
    hist_emojis = ""
    for res in hist_rev:
        if res == 'B':
            hist_emojis += "🔴 "
        elif res == 'P':
            hist_emojis += "🔵 "
        else:
            hist_emojis += "🟡 "
    st.markdown(f"**{hist_emojis}**")

# Stats
p = history.count('P')
b = history.count('B')
col1, col2 = st.columns(2)
col1.metric("Player", f"{p}")
col2.metric("Bank", f"{b}")

st.caption("Botões live | Sugestão sempre topo")
