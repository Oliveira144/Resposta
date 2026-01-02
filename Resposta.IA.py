import streamlit as st

st.title("🎯 FS - Sugestão por Padrões")

if 'h' not in st.session_state:
    st.session_state.h = []
    st.session_state.bank = 200

bank = st.number_input("💰 Bankroll", min_value=10)

# BOTÕES
c1,c2,c3=st.columns(3)
if c1.button("🔴 BANK"): st.session_state.h.append('🔴');st.rerun()
if c2.button("🔵 PLAYER"): st.session_state.h.append('🔵');st.rerun()
if c3.button("🟡 TIE"): st.session_state.h.append('🟡');st.rerun()

h = st.session_state.h[-15:]
if h:
    st.caption("📊 " + " ".join(h))

# === ANÁLISE 18 PADRÕES ===
def analyze_patterns(hist):
    n = len(hist)
    patterns = {}
    
    # 1. BIG ROAD (streak)
    streak=1; c=hist[-1]
    for i in range(1,min(10,n)):
        if n>i and hist[n-i-1]==c: streak+=1
        else: break
    patterns['bigroad'] = streak
    
    # 2. CHOPPY
    chop=0
    for i in range(1,min(7,n)):
        if hist[n-i]!=hist[n-i-1]: chop+=1
    patterns['choppy'] = chop
    
    # 3. COCKROACH (BBP ou PPB)
    cockroach = (n>=3 and hist[-3:]==['🔴','🔴','🔵']) or (n>=3 and hist[-3:]==['🔵','🔵','🔴'])
    patterns['cockroach'] = cockroach
    
    # 4. DRAGON (6+)
    patterns['dragon'] = streak >= 6
    
    # 5. MIRROR
    mirror = n>=8 and hist[-4:]==hist[-8:-4]
    patterns['mirror'] = mirror
    
    # 6. RED LINE (cortes horizontais)
    redline = chop >= 5
    patterns['redline'] = redline
    
    return patterns

# EXECUTA
if len(h)>=3:
    pats = analyze_patterns(h)
    
    st.markdown("### 🔍 **PADRÕES DETECTADOS**")
    
    # Lista padrões ativos
    active_patterns = []
    if pats['bigroad']>=4: active_patterns.append(f"1. Big Road x{pats['bigroad']}")
    if pats['choppy']>=4: active_patterns.append(f"2. Choppy x{pats['choppy']}")
    if pats['cockroach']: active_patterns.append("4. Cockroach")
    if pats['dragon']: active_patterns.append("5. Dragon")
    if pats['mirror']: active_patterns.append("6. Mirror")
    if pats['redline']: active_patterns.append("7. Red Line")
    
    for p in active_patterns:
        st.caption(p)
    
    # === SUGESTÃO BASEADA PADRÕES ===
    st.markdown("---")
    st.markdown("### 🚀 **SUGESTÃO POR PADRÕES**")
    
    color = h[-1]
    streak = pats['bigroad']
    
    if pats['dragon']:  # PRIORIDADE 1
        contra = "🔵 PLAYER" if color=="🔴" else "🔴 BANK"
        st.error(f"**{contra}** R${int(bank*0.02)} - DRAGON RECOVERY")
        
    elif streak >= 4:  # PRIORIDADE 2
        contra = "🔵 PLAYER" if color=="🔴" else "🔴 BANK"
        st.warning(f"**{contra}** R${int(bank*0.01)} - BIG ROAD")
        
    elif pats['cockroach']:  # PRIORIDADE 3
        if h[-1]=='🔵': st.info("**🔴 BANK** R${int(bank*0.008)} - Cockroach segue")
        else: st.info("**🔵 PLAYER** R${int(bank*0.008)} - Cockroach segue")
        
    elif pats['choppy'] >= 5:  # PRIORIDADE 4
        next_bet = "🔵 PLAYER" if color=="🔴" else "🔴 BANK"
        st.info(f"**{next_bet}** R${int(bank*0.005)} - CHOPPY")
        
    elif pats['mirror']:  # PRIORIDADE 5
        st.success(f"**{color}** R${int(bank*0.003)} - MIRROR repete")
        
    else:
        contra = "🔵 PLAYER" if color=="🔴" else "🔴 BANK"
        st.success(f"**{contra} FLAT** R${int(bank*0.003)}")
    
else:
    st.info("**3+ rodadas** para análise padrões")

# STATS
if h:
    c1,c2,c3=st.columns(3)
    c1.metric("🔴",h.count('🔴'))
    c2.metric("🔵",h.count('🔵'))
    c3.metric("🟡",h.count('🟡'))

if st.button("🗑️ Clear"): 
    st.session_state.h=[]
    st.rerun()

st.caption("**Sugestão = f(Padrões)** Dragon>BigRoad>Cockroach>Choppy...")
