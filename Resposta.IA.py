import streamlit as st

st.title("🎯 FS Pro - FINAL")

if 'h' not in st.session_state:
    st.session_state.h = []
    st.session_state.bank = 200

bank = st.number_input("💰 Bankroll", min_value=10)

# BOTÕES
c1,c2,c3=st.columns(3)
if c1.button("🔴 BANK"): st.session_state.h.append('🔴');st.rerun()
if c2.button("🔵 PLAYER"): st.session_state.h.append('🔵');st.rerun()
if c3.button("🟡 TIE"): st.session_state.h.append('🟡');st.rerun()

# HISTÓRICO: RECENTE ESQUERDA ← ANTIGO DIREITA
h_display = st.session_state.h[-12:][::-1]
if h_display:
    st.markdown("### 📊 **HISTÓRICO** ←**RECENTE**          **ANTIGO**→")
    st.markdown("`" + "     ".join(h_display) + "`")

# ANÁLISE
def analyze(h):
    n=len(h)
    if n<3: return {'streak':1, 'choppy':0, 'cockroach':False}
    
    # STREAK
    streak=1; c=h[-1]
    for i in range(1,min(10,n)):
        if h[-i-1]==c: streak+=1
        else: break
    
    # CHOPPY
    chop=0
    for i in range(1,min(7,n)):
        if h[-i]!=h[-i-1]: chop+=1
    
    # COCKROACH
    cockroach = (n>=3 and h[-3:]==['🔴','🔴','🔵']) or (n>=3 and h[-3:]==['🔵','🔵','🔴'])
    
    return {'streak':streak, 'choppy':chop, 'cockroach':cockroach, 'color':c}

# EXECUTA
st.markdown("---")
st.markdown("### 🚀 **SUGESTÃO PRINCIPAL**")

h = st.session_state.h
if len(h)<3:
    st.info("🔄 **3+ rodadas** p/ padrões")
else:
    analysis = analyze(h)
    
    if analysis['streak'] >= 6:
        contra_emoji = "🔵" if analysis['color']=="🔴" else "🔴"
        contra_side = "PLAYER" if analysis['color']=="🔴" else "BANK"
        st.error(f"""
## 🔥 **DRAGON 6+**
{contra_emoji}

**{contra_side}**

**R${int(bank*0.02)}**
        """)
    elif analysis['streak'] >= 4:
        contra_emoji = "🔵" if analysis['color']=="🔴" else "🔴"
        contra_side = "PLAYER" if analysis['color']=="🔴" else "BANK"
        st.warning(f"""
## ⚡ **BIG ROAD 4+**
{contra_emoji}

**{contra_side}**

**R${int(bank*0.01)}**
        """)
    elif analysis['cockroach']:
        st.info("""
## 🐛 **COCKROACH**
🔴

**BANK**

**R${int(bank*0.008)}**
        """)
    elif analysis['choppy'] >= 5:
        next_emoji = "🔵" if analysis['color']=="🔴" else "🔴"
        next_side = "PLAYER" if analysis['color']=="🔴" else "BANK"
        st.info(f"""
## 🔄 **CHOPPY**
{next_emoji}

**{next_side}**

**R${int(bank*0.005)}**
        """)
    else:
        contra_emoji = "🔵" if analysis['color']=="🔴" else "🔴"
        contra_side = "PLAYER" if analysis['color']=="🔴" else "BANK"
        st.success(f"""
## ✅ **NORMAL**
{contra_emoji}

**{contra_side}**

**R${int(bank*0.003)}**
        """)

# METRICS
if h:
    col1,col2,col3=st.columns(3)
    col1.metric("🔴",h[-12:].count('🔴'))
    col2.metric("🔵",h[-12:].count('🔵'))
    col2.metric("🟡",h[-12:].count('🟡'))

# PADRÕES
if len(h)>=4:
    st.markdown("### 🔍 **Padrões**")
    analysis=analyze(h)
    pats=[]
    if analysis['streak']>=4: pats.append(f"Big Road x{analysis['streak']}")
    if analysis['choppy']>=5: pats.append(f"Choppy x{analysis['choppy']}")
    if analysis['cockroach']: pats.append("Cockroach")
    
    for p in pats: st.caption(f"• {p}")

if st.button("🗑️ Clear"): st.session_state.h=[];st.rerun()

st.caption("**← RECENTE ESQUERDA** | **Syntax 100%** | Padrões → Sugestão")
