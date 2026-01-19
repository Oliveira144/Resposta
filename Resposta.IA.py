import streamlit as st
from motor import MotorAnalise

# ===============================
# CONFIG
# ===============================
st.set_page_config(layout="wide")
st.title("⚽ Football Studio – PRO (IA + Motor Central)")

motor = MotorAnalise()

# ===============================
# ESTADO
# ===============================
if "historico" not in st.session_state:
    st.session_state.historico = []

if "ultima_sugestao" not in st.session_state:
    st.session_state.ultima_sugestao = "AGUARDAR"

# ===============================
# FUNÇÕES
# ===============================
def registrar(resultado):
    st.session_state.historico.append(resultado)

def decidir_ia(padroes, blocos, empate_estado):
    score = 0
    motivo = []

    if len(padroes) >= 2:
        score += 25
        motivo.append("Confluência de padrões")

    if blocos and blocos[0] >= 4:
        score += 25
        motivo.append("Bloco forte")

    if empate_estado == "ANCORA":
        score += 10
        motivo.append("Empate âncora")

    if len(motor.memoria()) >= 2:
        score += 10
        motivo.append("Memória ativa")

    if score >= 60:
        return True, score, motivo

    return False, score, motivo

# ===============================
# BOTÕES (CORRIGIDOS)
# ===============================
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("CASA 🔴"):
        registrar("R")

with c2:
    if st.button("EMPATE ⚪"):
        registrar("E")

with c3:
    if st.button("VISITANTE 🔵"):
        registrar("B")

# ===============================
# HISTÓRICO VISUAL
# ===============================
st.subheader("📊 Histórico (recente → antigo)")
cores = {"R":"🔴","B":"🔵","E":"⚪"}
st.write(" ".join(cores[r] for r in st.session_state.historico))

# ===============================
# ANÁLISE PELO MOTOR
# ===============================
padroes, blocos = motor.detectar(st.session_state.historico)
estado_empate = motor.estado_empate(st.session_state.historico)

# ===============================
# IA DECISÃO
# ===============================
entrar, score, motivos = decidir_ia(padroes, blocos, estado_empate)

st.subheader("🎯 DECISÃO DA IA")

if entrar:
    st.success(
        f"ENTRAR ✅\n\n"
        f"Score: {score}\n"
        f"Estado do Empate: {estado_empate}\n\n"
        f"Padrões Detectados:\n" +
        "\n".join([f"- {p['padrao']} | Janela {p['janela']}" for p in padroes])
    )
else:
    st.warning(
        f"AGUARDAR ⏳\n\n"
        f"Score: {score}\n"
        f"Estado do Empate: {estado_empate}\n\n"
        f"Padrões Detectados:\n" +
        ("\n".join([f"- {p['padrao']} | Janela {p['janela']}" for p in padroes]) if padroes else "Nenhum padrão válido")
    )

# ===============================
# MEMÓRIA DE CICLOS
# ===============================
if padroes:
    motor.registrar_ciclo(
        padrao=padroes[0]["padrao"],
        bloco=padroes[0]["bloco"],
        lado="INDEFINIDO",
        empate=estado_empate
    )

with st.expander("🧠 Memória de 3 ciclos"):
    for c in motor.memoria():
        st.write({
            "Padrão": c.padrao,
            "Bloco": c.bloco,
            "Empate": c.empate
        })

# ===============================
# DEBUG (OPCIONAL)
# ===============================
with st.expander("🔍 Debug técnico"):
    st.write("Blocos reais:", blocos)
    st.write("Padrões brutos:", padroes)
    # motor.py

from collections import deque

# ===============================
# MODELOS
# ===============================

class Padrao:
    def __init__(self, nome, sequencia):
        self.nome = nome
        self.sequencia = sequencia

class Ciclo:
    def __init__(self, padrao, bloco, lado, empate):
        self.padrao = padrao
        self.bloco = bloco
        self.lado = lado
        self.empate = empate

# ===============================
# MOTOR CENTRAL
# ===============================

class MotorAnalise:
    def __init__(self):
        self.ciclos = deque(maxlen=3)
        self.padroes = self._carregar_padroes()

    # ---------------------------
    # PADRÕES (CATÁLOGO TOTAL)
    # ---------------------------
    def _carregar_padroes(self):
        return [
            Padrao("CURTO 1x1", [1,1]),
            Padrao("CURTO 1x1x1", [1,1,1]),
            Padrao("DUPLO 2x2", [2,2]),
            Padrao("DUPLO 2x1x2", [2,1,2]),
            Padrao("TRIPLO 3", [3]),
            Padrao("COMPOSTO 3x1x3", [3,1,3]),
            Padrao("DUPLO LONGO 4x4", [4,4]),
            Padrao("PADRÃO ATUALIZADO", [4,4,3,2,3,2,1,2]),
        ]

    # ---------------------------
    # BLOCOS REAIS
    # ---------------------------
    def extrair_blocos(self, historico):
        blocos = []
        atual = None
        cont = 0

        for r in reversed(historico):
            if r == "E":
                if cont > 0:
                    blocos.append(cont)
                atual = None
                cont = 0
                continue

            if r == atual:
                cont += 1
            else:
                if cont > 0:
                    blocos.append(cont)
                atual = r
                cont = 1

        if cont > 0:
            blocos.append(cont)

        return blocos

    # ---------------------------
    # JANELAS DESLIZANTES
    # ---------------------------
    def gerar_janelas(self, blocos):
        janelas = []
        for tamanho in [3,5,7,9,12]:
            for i in range(len(blocos) - tamanho + 1):
                janelas.append(blocos[i:i+tamanho])
        return janelas

    # ---------------------------
    # EMPATE (ESTADO)
    # ---------------------------
    def estado_empate(self, historico):
        if not historico:
            return "NEUTRO"

        if historico[-1] == "E":
            if historico[-2] == "E":
                return "QUEBRA"
            return "ANCORA"

        return "NEUTRO"

    # ---------------------------
    # DETECÇÃO DE PADRÕES
    # ---------------------------
    def detectar(self, historico):
        blocos = self.extrair_blocos(historico)
        janelas = self.gerar_janelas(blocos)
        encontrados = []

        for janela in janelas:
            for p in self.padroes:
                if janela[:len(p.sequencia)] == p.sequencia:
                    encontrados.append({
                        "padrao": p.nome,
                        "janela": janela,
                        "bloco": janela[0]
                    })

        return encontrados, blocos

    # ---------------------------
    # MEMÓRIA DE 3 CICLOS
    # ---------------------------
    def registrar_ciclo(self, padrao, bloco, lado, empate):
        self.ciclos.append(Ciclo(padrao, bloco, lado, empate))

    def memoria(self):
        return list(self.ciclos)
