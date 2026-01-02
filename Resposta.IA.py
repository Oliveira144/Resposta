import streamlit as st

st.title("FS Live")

bankroll = st.number_input("R$", 500)

# Botões
col1, col2, col3 = st.columns(3)
if col1.button("🔴 B"):
    st.session_state.h = st.session_state.get('h', []) + ['B']
if col2.button("🔵 P"):
    st.session_state.h = st.session_state.get('h', []) + ['P']
if col3.button("🟡 T"):
    st.session_state.h = st.session_state.get('h', []) + ['T']

if st.button("Clear"):
    st.session_state.h = []

h = st.session_state.get('h', [])[-10:]

if h:
    # HISTORICO 1 LINHA HORIZONTAL
    st.text("Histórico:")
    hist_str = " ".join(['🔴' if x=='B' else '🔵' if x=='P' else '🟡' for x in h])
    st.markdown(f"**{hist_str}**")
    
    # Streak rápido
    s = 1
    c = h[-1]
    for o in reversed(h[-5:]):
        if o == c:
            s += 1
        else:
            break
    
    if s >= 3:
        bet = "🔵 P" if c == 'B' else "🔴 B"
        st.error(f"🚨 {bet}!")
    else:
        st.info(f"{c} x{s}")
    
    st.caption(f"P: {h.count('P')}/{len([x for x in h if x != 'T'])}")

st.markdown("---")
