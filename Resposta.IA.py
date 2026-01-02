import streamlit as st

st.title("Football Studio - 18 Padrões PRO")

# Estado
if 'history' not in st.session_state:
    st.session_state.history = []
    st.session_state.bankroll = 200

bankroll = st.number_input("Bankroll", value=st.session_state.bankroll)

# Botões
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔴 BANK", use_container_width=True):
        st.session_state.history.append('B')
        st.rerun()
with col2:
    if st.button("🔵 PLAYER", use_container_width=True):
        st.session_state.history.append('P')
        st.rerun()
with col3:
    if st.button("🟡 TIE", use_container_width=True):
        st.session_state.history.append('T')
        st.rerun()

h = st.session_state.history[-20:]  # Últimos 20 para padrões
st.caption("Histórico: " + " ".join(h))

# FUNÇÃO PADRÕES (18 DETECTADOS)
def detect_patterns(history):
    patterns = {}
    
    # 1. BIG ROAD (streak principal)
    streak = 1
    color = history[-1]
    for i in range(2, min(11, len(history)+1)):
        if history[-i] == color:
            streak += 1
        else:
            break
    patterns['Big Road'] = f"{color} x{streak}"
    
    # 2. STREAK BREAKER (quebra após 4+)
    if streak >= 4:
        patterns['Streak Breaker'] = "Alta prob contrária"
    
    # 3. CHOPPY (BPBPBP)
    choppy = 0
    for i in range(1, min(7, len(history))):
        if history[-i] != history[-(i+1)]:
            choppy += 1
    if choppy >= 5:
        patterns['Choppy'] = "Continue alternado"
    
    # 4. DOUBLE (BB ou PP)
    double = sum(1 for i in range(1, min(6, len(history))) if history[-i] == history[-(i+1)])
    if double >= 3:
        patterns['Double'] = f"Dobras x{double}"
    
    # 5. TRIPLE (BBB/PPP)
    triple = sum(1 for i in range(1, min(8, len(history))) if history[-i] == history[-(i+1)] == history[-(i+2)])
    if triple >= 1:
        patterns['Triple'] = "Triplas ativas"
    
    # 6. QUAD (BBBB/PPP)
    quad = 0
    for i in range(1, min(10, len(history)-2)):
        if history[-i] == history[-(i+1)] == history[-(i+2)] == history[-(i+3)]:
            quad += 1
    if quad >= 1:
        patterns['Quad'] = "4+ streak"
    
    # 7. RUN (sequência longa 6+)
    if streak >= 6:
        patterns['Run'] = "Recovery contrária"
    
    # 8. ZIGZAG (BPPBPP)
    zigzag = 0
    for i in range(2, min(8, len(history))):
        if history[-i] != history[-(i-1)] == history[-(i-2)]:
            zigzag += 1
    if zigzag >= 2:
        patterns['Zigzag'] = "Padrão 1-2"
    
    # 9. PING PONG (BPBP 4+)
    pingpong = 0
    for i in range(1, min(9, len(history))):
        if history[-i] != history[-(i+1)]:
            pingpong += 1
        else:
            break
    if pingpong >= 4:
        patterns['Ping Pong'] = "Alternado forte"
    
    # 10. LEFT SIDE (mais BANK lado esquerdo)
    b_left = h[:10].count('B') if len(h) >= 10 else 0
    if b_left >= 6:
        patterns['Left Bias'] = "BANK dominante"
    
    # 11. RIGHT SIDE (PLAYER forte)
    p_right = h[-10:].count('P') if len(h) >= 10 else 0
    if p_right >= 6:
        patterns['Right Bias'] = "PLAYER dominante"
    
    # 12. TIE BREAKER (T após streak)
    recent_tie = 'T' in h[-5:]
    if recent_tie and streak >= 3:
        patterns['Tie Breaker'] = "T resetou"
    
    # 13. MIRROR (simetria últimos 4)
    if len(h) >= 8:
        mirror = h[-4:] == h[-8:-4]
        if mirror:
            patterns['Mirror'] = "Repetição 4"
    
    # 14. FOLLOW THE DRAGON (continua streak 5+)
    if streak >= 5:
        patterns['Dragon'] = f"Dragon {color}"
    
    # 15. RED LINE (cortes horizontais)
    cuts = sum(1 for i in range(1, min(6, len(h))) if h[-i] != h[-(i+1)])
    if cuts >= 4:
        patterns['Red Line'] = "Muitos cortes"
    
    # 16. BLUE LINE (cortes verticais)
    if len(h) >= 12:
        blue_cuts = 0
        for col in range(0, 12, 2):
            if h[col:col+2] and h[col] != h[col+1]:
                blue_cuts += 1
        if blue_cuts >= 3:
            patterns['Blue Line'] = "Cortes verticais"
    
    # 17. COCKROACH (PBP após BB)
    if len(h) >= 5 and h[-3:] == ['B','B','P']:
        patterns['Cockroach'] = "PBP padrão"
    
    # 18. SHOE END (Ties finais)
    ties_end = h[-4:].count('T')
    if ties_end >= 2:
        patterns['Shoe End'] = "Finalizando shoe"
    
    return patterns

# Detecta padrões
if h:
    patterns = detect_patterns(h)
    
    # TOP 3 PADRÕES ATIVOS
    st.subheader("🔍 PADRÕES DETECTADOS")
    for i, (p, desc) in enumerate(list(patterns.items())[:6]):
        with st.container():
            col1, col2 = st.columns([2,3])
            with col1:
                st.write(f"**{i+1}. {p}**")
            with col2:
                st.caption(desc)
    
    # SUGESTÃO PRINCIPAL
    st.subheader("🎯 SUGESTÃO ATUAL")
    
    streak = 1
    color = h[-1]
    for i in range(2, min(11, len(h)+1)):
        if h[-i] == color:
            streak += 1
        else:
            break
    
    if streak >= 6:
        bet = "PLAYER" if color == 'B' else "BANK"
        st.error(f"🚨 **{bet} R${int(bankroll*0.02)}** - Recovery 6+")
    elif streak >= 4:
        bet = "PLAYER" if color == 'B' else "BANK" 
        st.warning(f"⚠️ **{bet} R${int(bankroll*0.01)}** - Streak 4-5")
    elif 'Choppy' in patterns or 'Ping Pong' in patterns:
        next_bet = "PLAYER" if color == 'B' else "BANK"
        st.info(f"🔄 **{next_bet} R${int(bankroll*0.005)}** - Choppy")
    else:
        st.success("⏳ **Aguardar** - Sem setup claro")

# Stats
if h:
    col1, col2, col3 = st.columns(3)
    col1.metric("BANK", h.count('B'))
    col2.metric("PLAYER", h.count('P'))
    col3.metric("TIE", h.count('T'))

# Reset
if st.button("🗑️ Clear All"):
    st.session_state.history = []
    st.rerun()

st.caption("**18 Padrões Football Studio** - Big Road, Choppy, Streak Breaker, Ping Pong, Dragon, Mirror...")
