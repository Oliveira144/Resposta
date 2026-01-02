import streamlit as st

st.title("🎯 FS Pro - Histórico Correto")

if 'h' not in st.session_state:
    st.session_state.h = []
    st.session_state.bank = 200

bank = st.number_input("💰 Bankroll", min_value=10)

# BOTÕES
c1,c2,c3 = st.columns(3)
if c1.button("🔴 BANK", use_container_width=True): 
    st.session_state.h.append('🔴')
    st.rerun()
if c2.button("🔵 PLAYER", use_container_width=True):
    st.session_state.h.append('🔵')
    st.rerun()
if c3.button("🟡 TIE", use_container_width=True):
    st.session_state.h.append('🟡')
    st.rerun()

# HISTÓRICO CORRIGIDO: RECENTE ←—————→ ANTIGO
h_display = st.session_state.h[-12:][::-1]  # REVERSE: novo ESQUERDA
if h_display:
    st.markdown("### 📊 **HISTÓRICO** ← RECENTE     ANTIGO →")
    st.markdown("**`" + "     ".join(h_display) + "`**")
    
    # STATS
    h = st.session_state.h[-12:]
    col1,col2,col3=st.columns(3)
    col1.metric("🔴", h.count('🔴'))
    col2.metric("🔵", h.count('🔵'))
    col3.metric("🟡", h.count('🟡'))

# ANÁLISE PADRÕES (histórico original ordem)
def analyze_patterns(hist):
    n = len(hist)
    if n < 3: return {}
    
    # BIG ROAD (último streak)
    streak=1; c=hist[-1]
    for i in range(1, min(10,n)):
        if hist[-i-1]==c: streak+=1
        else: break
    
    # CHOPPY
    chop=0
    for i in range(1,min(7,n)):
        if hist[-i]!=hist[-i-1]: chop+=1
    
    # COCKROACH
    cockroach = (n>=3 and hist[-3:]==['🔴','🔴','🔵']) or (n>=3 and hist[-3:]==['🔵','🔵','🔴'])
    
    return {
        'streak': streak,
        'color': c,
        'choppy': chop,
        'cockroach': cockroach
    }

# === SUGESTÃO GIGANTE CLARA ===
st.markdown("---")
st.markdown("### 🚀 **SUGESTÃO PRINCIPAL**")

h = st.session_state.h
if len(h) < 3:
    st.info("🔄 **3+ rodadas** para padrões precisos")
elif len(h) >= 3:
    analysis = analyze_patterns(h)
    
    # PRIORIDADE PADRÕES
    if analysis['streak'] >= 6:
        contra = "🔵

**PLAYER**

R$"+str(int(bank*0.02))
        st.error(f"## 🔥 **DRAGON RECOVERY**

{contra}")
    elif analysis['streak'] >= 4:
        contra = "🔵

**PLAYER**

R$"+str(int(bank*0.01))
        st.warning(f"## ⚡ **BIG ROAD 4+**

{contra}")
    elif analysis['cockroach']:
        st.info("## 🐛 **COCKROACH**

🔴

**BANK**

R$"+str(int(bank*0.008)))
    elif analysis['choppy'] >= 5:
        next_bet = "🔵 PLAYER" if analysis['color']=="🔴" else "🔴 BANK"
        amt = str(int(bank*0.005))
        st.info(f"## 🔄 **CHOPPY**

{next_bet}

**R${amt}**")
    else:
        contra = "🔵 PLAYER" if analysis['color']=="🔴" else "🔴 BANK"
        st.success(f"## ✅ **FLAT BET**

{contra}

R${int(bank*0.003)}")

# PADRÕES DETALHADOS
if len(h) >= 4:
    st.markdown("### 🔍 **PADRÕES ATIVOS**")
    analysis = analyze_patterns(h)
    
    pats = []
    if analysis['streak']>=4: pats.append(f"🔥 Big Road x{analysis['streak']}")
    if analysis['choppy']>=5: pats.append(f"🔄 Choppy x{analysis['choppy']}")
    if analysis['cockroach']: pats.append("🐛 Cockroach")
    if analysis['streak']>=6: pats.append("🐲 Dragon")
    
    for p in pats:
        st.caption(f"• **{p}**")

# CLEAR
if st.button("🗑️ Clear", type="secondary"):
    st.session_state.h = []
    st.rerun()

st.caption("**← RECENTE ESQUERDA** | Sugestão **HUGE** por padrões")
