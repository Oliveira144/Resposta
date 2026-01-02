import streamlit as st

st.title("FS - 4 Padrões Simples")

bank = st.number_input("Bankroll", 200)

if 'h' not in st.session_state: st.session_state.h = []

c1,c2,c3=st.columns(3)
if c1.button("🔴 B"): st.session_state.h.append('🔴');st.rerun()
if c2.button("🔵 P"): st.session_state.h.append('🔵');st.rerun()
if c3.button("🟡 T"): st.session_state.h.append('🟡');st.rerun()

h = st.session_state.h[-10:][::-1]
st.caption("← RECENTE " + " | ".join(h))

# ANÁLISE 4 PADRÕES
if len(st.session_state.h)>=3:
    # 1. BIG ROAD
    streak=1; last=st.session_state.h[-1]
    for i in range(1,min(7,len(st.session_state.h))):
        if st.session_state.h[-i-1]==last: streak+=1
        else: break
    
    # 2. CHOPPY
    chop=0
    for i in range(1,min(6,len(st.session_state.h))):
        if st.session_state.h[-i]!=st.session_state.h[-i-1]: chop+=1
    
    # 3. COCKROACH
    cock = len(st.session_state.h)>=3 and st.session_state.h[-3:]==['🔴','🔴','🔵']
    
    st.subheader("📊 PADRÕES:")
    col1,col2=st.columns(2)
    col1.metric("Streak", streak)
    col2.metric("Choppy", chop)
    
    if cock: st.error("🐛 COCKROACH!")
    
    # BET
    st.markdown("### 🎯 **APOSTA**")
    if streak>=5:
        bet = "🔵" if last=="🔴" else "🔴"
        st.error(f"**{bet} R${int(bank*0.02)}** - DRAGON")
    elif streak>=3:
        bet = "🔵" if last=="🔴" else "🔴"
        st.warning(f"**{bet} R${int(bank*0.01)}** - STREAK")
    elif chop>=4:
        bet = "🔵" if last=="🔴" else "🔴"
        st.info(f"**{bet} R${int(bank*0.005)}** - CHOPPY")
    elif cock:
        st.success("**🔴 BANK R${int(bank*0.008)}** - COCKROACH")
    else:
        bet = "🔵" if last=="🔴" else "🔴"
        st.success(f"**{bet} R${int(bank*0.003)}**")

if st.button("Clear"): st.session_state.h=[];st.rerun()
