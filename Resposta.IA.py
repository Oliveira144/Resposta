import streamlit as st

st.title("FS Live")

if 'h' not in st.session_state:
    st.session_state.h = []

bankroll = st.number_input("R$", 1000)

# BOTÕES
c1, c2, c3 = st.columns(3)
if c1.button("🔴 BANK"):
    st.session_state.h.append('B')
if c2.button("🔵 PLAYER"):
    st.session_state.h.append('P')
if c3.button("🟡 TIE"):
    st.session_state.h.append('T')

if st.button("Clear"):
    st.session_state.h = []

h = st.session_state.h[-10:]

# SUGESTÃO DIRETA TOPO
if len(h) >= 3:
    s = 1
    c = h[-1]
    for o in reversed(h[-5:]):
        if o == c:
            s += 1
        else:
            break
    
    st.markdown("### 🚨 **SUGESTÃO**")
    if s >= 3:
        bet = "PLAYER 🔵" if c == 'B' else "BANK 🔴"
        stake = int(bankroll * 0.01)
        st.error(f"**{bet} R${stake} AGORA**")
    else:
        st.info("**Aguarde streak 3+**")

# HISTORICO ESQUERDA→DIREITA RECENTE→ANTIGO
if h:
    st.subheader("Histórico ← Recente")
    hist_rev = list(reversed(h[-8:]))  # Recente esquerda
    hist_str = " ".join(['🔴B' if x=='B' else '🔵P' if x=='P' else '🟡T' for x in hist_rev])
    st.markdown(f"**{hist_str}**")

# Stats baixo
p_win = h.count('P') / (h.count('P') + h.count('B'))
st.caption(f"P win {p_win:.0%} | {len(h)} rodadas")
