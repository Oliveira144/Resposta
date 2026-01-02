import streamlit as st

st.markdown("# Football Studio Tracker")

# ZERO dependências extras
bankroll = st.number_input("Bankroll R$", value=1000)

seq = st.text_input("Digite P B T (espaço):", "P P P B B B")

if seq:
    parts = seq.split()
    p_count = parts.count('P')
    b_count = parts.count('B')
    total = p_count + b_count
    
    st.write("**Stats**")
    st.write(f"Player: {p_count}/{total} ({p_count/total*100:.0f}%)")
    st.write(f"Banker: {b_count}/{total} ({b_count/total*100:.0f}%)")
    
    # Streak básico
    streak = 1
    for i in range(len(parts)-2, -1, -1):
        if parts[i] == parts[-1]:
            streak += 1
        else:
            break
    
    st.write(f"**Streak atual**: {parts[-1]} x{streak}")
    
    if streak >= 3:
        bet = "PLAYER" if parts[-1] == "B" else "BANKER"
        st.error(f"🚨 APOSTE {bet}!")
    else:
        st.info("Aguarde 3+")

st.balloons()
