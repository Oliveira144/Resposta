import streamlit as st

st.title("Football Studio PRO")

if 'history' not in st.session_state:
    st.session_state.history = []

bankroll = st.number_input("Bankroll R$", 500)

# BOTÕES
col1, col2, col3 = st.columns(3)
if col1.button("🔴 BANK", use_container_width=True):
    st.session_state.history.append('B')
    st.rerun()
if col2.button("🔵 PLAYER", use_container_width=True):
    st.session_state.history.append('P')
    st.rerun()
if col3.button("🟡 TIE", use_container_width=True):
    st.session_state.history.append('T')
    st.rerun()

if st.button("Clear", type="secondary"):
    st.session_state.history = []
    st.rerun()

history = st.session_state.history[-12:]

# HISTORICO HORIZONTAL MAIS RECENTE ← ANTIGO
if history:
    st.subheader("Histórico")
    hist_emojis = []
    for res in reversed(history):  # Reverte: recente primeiro
        if res == 'B':
            hist_emojis.append('🔴')
        elif res == 'P':
            hist_emojis.append('🔵')
        else:
            hist_emojis.append('🟡')
    
    # 1 LINHA HORIZONTAL
    st.markdown("**" + " ".join(hist_emojis) + "**")
    
    # STREAK (sempre visível)
    if len(history) >= 3:
        streak = 1
        current = history[-1]
        for o in reversed(history[-6:]):
            if o == current and o != 'T':
                streak += 1
            else:
                break
        
        st.metric("Streak", f"{current} x{streak}")
        
        # SUGESTÃO SEMPRE
        if streak >= 3:
            bet = "🔵 PLAYER" if current == 'B' else "🔴 BANK"
            stake = int(bankroll * 0.01)
            st.error(f"🚨 **APOSTE {bet}!** R${stake}")
        elif streak == 2:
            bet = "🔵 PLAYER" if current == 'B' else "🔴 BANK"
            st.warning(f"⚠️ Prepare {bet}")
        else:
            st.info("⏳ Streak 1 - Aguarde")
    
    # Stats compacto
    p = history.count('P')
    b = history.count('B')
    total = p + b
    col1, col2 = st.columns(2)
    col1.metric("P%", f"{p/total:.0%}")
    col2.metric("Total", len(history))

st.caption("Histórico recente ← antigo | Sugestão sempre visível")
