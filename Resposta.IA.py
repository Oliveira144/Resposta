import streamlit as st

st.title("Football Studio")

if 'results' not in st.session_state:
    st.session_state.results = []

bankroll = st.number_input("Bankroll", 100, 5000, 1000)

col1, col2, col3 = st.columns(3)
if col1.button("🔴 BANK", use_container_width=True):
    st.session_state.results.append('B')
if col2.button("🔵 PLAYER", use_container_width=True):
    st.session_state.results.append('P')
if col3.button("🟡 TIE", use_container_width=True):
    st.session_state.results.append('T')

if st.button("LIMPAR"):
    st.session_state.results = []

results = st.session_state.results[-15:]

if results:
    st.subheader("Histórico")
    # Horizontal simples
    for r in results:
        if r == 'B':
            st.markdown("🔴 **B**")
        elif r == 'P':
            st.markdown("🔵 **P**")
        else:
            st.markdown("🟡 **T**")
    
    # Streak
    streak = 1
    cur = results[-1]
    for o in reversed(results[-8:]):
        if o == cur:
            streak += 1
        else:
            break
    
    if streak >= 3:
        bet = "🔵 PLAYER" if cur == 'B' else "🔴 BANK"
        st.error(f"APOSTE {bet}!")
    else:
        st.info(f"Streak {cur} x{streak}")

st.caption("Botões live!")
