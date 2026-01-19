import streamlit as st
from collections import Counter, deque

# =====================================================
# CONFIG STREAMLIT
# =====================================================
st.set_page_config(layout="wide", page_title="Football Studio PRO")
st.title("⚽ Football Studio PRO – IA Completa")

# =====================================================
# MOTOR DE ANÁLISE (COMPLETO)
# =====================================================

class Ciclo:
    def __init__(self, padrao, bloco, empate):
        self.padrao = padrao
        self.bloco = bloco
        self.empate = empate


class MotorAnalise:
    def __init__(self):
        self.memoria_ciclos = deque(maxlen=3)

    # -----------------------------
    # BLOCOS REAIS
    # -----------------------------
    def _blocos(self, historico):
        blocos, atual, cont = [], None, 0
        for r in historico:
            if r == atual:
                cont += 1
            else:
                if atual is not None:
                    blocos.append(cont)
                atual, cont = r, 1
        if cont:
            blocos.append(cont)
        return blocos

    def _sem_empate(self, historico):
        return [h for h in historico if h != "E"]

    # -----------------------------
    # DETECÇÃO DE PADRÕES
    # -----------------------------
    def detectar(self, historico):
        padroes = []
        blocos = self._blocos(historico)
        h = self._sem_empate(historico)

        if len(h) < 6:
            return padroes, blocos

        # 1️⃣ STREAK
        if blocos and blocos[-1] >= 2:
            padroes.append(("STREAK", blocos[-1], blocos[-1]*10))

        # 2️⃣ DUPLO CURTO 2x2
        if len(blocos) >= 2 and blocos[-1] == 2 and blocos[-2] == 2:
            padroes.append(("DUPLO_CURTO_2x2", 2, 25))

        # 3️⃣ CURTO 1x1x1
        ult = h[-6:]
        if ult.count("R") == 3 and ult.count("B") == 3:
            if all(ult[i] != ult[i-1] for i in range(1,6)):
                padroes.append(("CURTO_1x1x1", 1, 20))

        # 4️⃣ ZIGZAG
        if all(ult[i] != ult[i-1] for i in range(1,len(ult))):
            padroes.append(("ZIGZAG", 1, 30))

        # 5️⃣ CLUSTER
        if len(blocos) >= 3:
            media = sum(blocos[-3:]) / 3
            if 2.5 <= media <= 4.5:
                padroes.append(("CLUSTER", int(media), 35))

        # 6️⃣ SEQUÊNCIA COMPLEXA
        if len(blocos) >= 8 and blocos[-8:] == [4,4,3,2,3,2,1,2]:
            padroes.append(("SEQUENCIA_COMPLEXA", 4, 60))

        # 7️⃣ REVERSÃO ESTATÍSTICA
        c = Counter(h[-50:])
        if abs(c["R"] - c["B"]) >= 15:
            padroes.append(("REVERSAO_MEDIA", abs(c["R"]-c["B"]), 40))

        return padroes, blocos

    # -----------------------------
    # EMPATE (CORRIGIDO)
    # -----------------------------
    def estado_empate(self, historico):
        sem = 0
        for r in reversed(historico):
            if r == "E":
                break
            sem += 1
        if sem >= 45:
            return "ANCORA"
        if sem >= 25:
            return "ATENCAO"
        return "NEUTRO"

    # -----------------------------
    # MEMÓRIA 3 CICLOS
    # -----------------------------
    def registrar_ciclo(self, padrao, bloco, empate):
        self.memoria_ciclos.append(Ciclo(padrao, bloco, empate))

    def memoria(self):
        return list(self.memoria_ciclos)


# =====================================================
# IA DE DECISÃO
# =====================================================

def decisao_ia(padroes, blocos, estado_empate, memoria):
    score = 0
    motivos = []

    if len(padroes) >= 2:
        score += 25
        motivos.append("Confluência de padrões")

    if blocos and blocos[-1] >= 4:
        score += 25
        motivos.append("Bloco forte")

    if estado_empate == "ANCORA":
        score += 10
        motivos.append("Empate âncora")

    if len(memoria) >= 2:
        score += 10
        motivos.append("Memória ativa")

    if score >= 60:
        return True, score, motivos

    return False, score, motivos


# =====================================================
# APP
# =====================================================

motor = MotorAnalise()

if "historico" not in st.session_state:
    st.session_state.historico = []

# -----------------------------
# BOTÕES (NOMES CORRIGIDOS)
# -----------------------------
c1, c2, c3 = st.columns(3)

if c1.button("CASA 🔴"):
    st.session_state.historico.insert(0, "R")

if c2.button("EMPATE ⚪"):
    st.session_state.historico.insert(0, "E")

if c3.button("VISITANTE 🔵"):
    st.session_state.historico.insert(0, "B")

# -----------------------------
# HISTÓRICO VISUAL
# -----------------------------
st.subheader("📊 Histórico (mais recente → mais antigo)")
st.write(" ".join({"R":"🔴","B":"🔵","E":"⚪"}[h] for h in st.session_state.historico))

# -----------------------------
# ANÁLISE
# -----------------------------
padroes, blocos = motor.detectar(st.session_state.historico)
estado_empate = motor.estado_empate(st.session_state.historico)

entrar, score, motivos = decisao_ia(
    padroes,
    blocos,
    estado_empate,
    motor.memoria()
)

st.subheader("🎯 SUGESTÃO DA IA")

if entrar:
    st.success(f"✅ ENTRAR | Score {score}")
else:
    st.warning(f"⏳ AGUARDAR | Score {score}")

st.write("Estado do empate:", estado_empate)

if padroes:
    st.write("📌 Padrões detectados:")
    for p in padroes:
        st.write(f"- {p[0]} | bloco {p[1]} | força {p[2]}")
    motor.registrar_ciclo(padroes[0][0], padroes[0][1], estado_empate)
else:
    st.write("Nenhum padrão válido no momento")

# -----------------------------
# MEMÓRIA
# -----------------------------
with st.expander("🧠 Memória de 3 ciclos"):
    for c in motor.memoria():
        st.write({
            "Padrão": c.padrao,
            "Bloco": c.bloco,
            "Empate": c.empate
        })
