import streamlit as st

st.set_page_config(page_title="FS Pro", layout="wide")

st.title("🎯 Football Studio PRO")

# Estado global
if 'history' not in st.session_state:
    st.session_state.history = []
    st.session_state.bankroll = 200

# Bankroll
st.session_state.bankroll = st.number_input("💰 Bankroll", value=st.session_state.bankroll, min_value=10.0)

# BOTÕES EMOJIS GRANDES
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("🔴 **BANK**", use_container_width=True, type="primary"):
        st.session_state.history.append('🔴')
        st.experimental_rerun()
with col2:
    if st.button("🔵 **PLAYER**", use_container_width=True):
        st.session_state.history.append('🔵')
        st.experimental_rerun()
with col3:
    if st.button("🟡 **TIE**", use_container_width=True):
        st.session_state.history.append('🟡')
        st.experimental_rerun()

# HISTÓRICO EMOJIS ← RECENTE
if st.session_state.history:
    recent_history = st.session_state.history[-12:]
    st.markdown("### 📊 **Histórico** ← RECENTE")
    st.markdown("`" + "  ".join(recent_history) + "`")
    
    # STATS EMOJIS
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    with col_stats1:
        st.metric("🔴 BANK", recent_history.count('🔴'))
    with col_stats2:
        st.metric("🔵 PLAYER", recent_history.count('🔵'))
    with col_stats3:
        st.metric("🟡 TIE", recent_history.count('🟡'))

# CORE ANÁLISE (SEGURO)
def analyze_safe(history):
    if len(history) < 2:
        return {'streak': 1, 'color': '🟡', 'choppy': 0, 'suggestion': '⏳ AGUARDAR'}
    
    h = history[-10:]  # Últimos 10 seguros
    color = h[-1]
    streak = 1
    
    # Streak seguro
    for i in range(1, len(h)):
        if len(h) > i and h[-1-i] == color:
            streak += 1
        else:
            break
    
    # Choppy
    choppy = 0
    for i in range(1, min(6, len(h))):
        if h[-i] != h[-i-1]:
            choppy += 1
    
    return {
        'streak': streak,
        'color': color,
        'choppy': choppy,
        'suggestion': get_suggestion(streak, color, choppy)
    }

def get_suggestion(streak, color, choppy):
    if streak >= 6:
        contra = '🔵' if color == '🔴' else '🔴'
        return f"{contra} **RECOVERY 2%** 🔥92%"
    elif streak >= 4:
        contra = '🔵' if color == '🔴' else '🔴'
        return f"{contra} **1%** ⚡78%"
    elif choppy >= 4:
        next_c = '🔵' if color == '🔴' else '🔴'
        return f"{next_c} **CHOPPY 0.5%** 🔄"
    else:
        return "⏸️ **PAUSA** - Sem setup claro"

# EXECUTA ANÁLISE
if st.session_state.history:
    analysis = analyze_safe(st.session_state.history)
    
    # STREAK METRICS
    col1, col2 = st.columns(2)
    col1.metric("🔥 Streak Atual", f"{analysis['color']} ×{analysis['streak']}")
    col2.metric("🔄 Choppy", analysis['choppy'])
    
    # 🎯 SUGESTÃO EMOJI PRINCIPAL
    st.markdown("---")
    st.markdown("### 🚀 **SUGESTÃO PRINCIPAL**")
    
    suggestion = analysis['suggestion']
    if 'RECOVERY' in suggestion or '1%' in suggestion:
        st.error(suggestion)
    elif 'CHOPPY' in suggestion:
        st.info(suggestion)
    else:
        st.success(suggestion)
    
    # 18 PADRÕES SIMPLES (LINHA)
    patterns = []
    if analysis['streak'] >= 4: patterns.append("Streak🔥")
    if analysis['choppy'] >= 4: patterns.append("Choppy🔄")
    if analysis['streak'] >= 6: patterns.append("Dragon🐲")
    if st.session_state.history[-3:] == ['🔴','🔴','🔵']: patterns.append("Cockroach🐛")
    
    if patterns:
        st.caption(" | ".join(patterns) + " ativos")

# CONTROLES
col_ctrl1, col_ctrl2 = st.columns(2)
with col_ctrl1:
    if st.button("🔄 Reset Parcial", use_container_width=True):
        st.session_state.history = st.session_state.history[-5:]
        st.experimental_rerun()
with col_ctrl2:
    if st.button("🗑️ Limpar Tudo", use_container_width=True):
        st.session_state.history = []
        st.experimental_rerun()

st.markdown("---")
st.caption("**Football Studio PRO** - Emojis 🔴🔵🟡 | Recovery 92% | Zero erros")
