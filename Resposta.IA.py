import streamlit as st
from collections import Counter

# ======================================================
# CONFIG
# ======================================================
st.set_page_config(page_title="Football Studio Trader IA PRO", layout="wide")

# ======================================================
# ESTADO GLOBAL
# ======================================================
if "historico" not in st.session_state:
    st.session_state.historico = []  # mais recente -> antigo

# ======================================================
# MOTOR COMPLETO – TRADER IA
# ======================================================
class TraderIA:
    def __init__(self, historico):
        self.h = historico
        self.padroes = []
        self.score = 0
        self.contexto = {}
        self.brecha = False

    # ==========================
    # EXECUÇÃO PRINCIPAL
    # ==========================
    def executar(self):
        if len(self.h) < 3:
            return self._saida("SEGURAR", "Histórico insuficiente")

        self._leitura_contexto()
        self._padroes_simples()
        self._padroes_compostos()
        self._memoria_ciclos()
        self._avaliar_brecha()

        return self._decisao_final()

    # ==========================
    # CONTEXTO DE MESA
    # ==========================
    def _leitura_contexto(self):
        ultimos = self.h[:20]
        cont = Counter(ultimos)

        total = len(ultimos)
        if total == 0:
            return

        vr = cont.get("R", 0) / total
        vb = cont.get("B", 0) / total

        if abs(vr - vb) >= 0.25:
            self.contexto["mesa"] = "DOMINANTE"
            self.score += 20
        elif abs(vr - vb) <= 0.1:
            self.contexto["mesa"] = "EQUILIBRADA"
        else:
            self.contexto["mesa"] = "INSTÁVEL"

        # ritmo
        alternancias = sum(1 for i in range(len(ultimos)-1) if ultimos[i] != ultimos[i+1])
        if alternancias >= total * 0.6:
            self.contexto["ritmo"] = "RÁPIDO"
            self.score += 10
        else:
            self.contexto["ritmo"] = "LENTO"

    # ==========================
    # PADRÕES SIMPLES
    # ==========================
    def _padroes_simples(self):
        h = self.h

        # STREAK
        streak = 1
        for i in range(1, len(h)):
            if h[i] == h[0] and h[i] != "E":
                streak += 1
            else:
                break

        if streak >= 3:
            self._add(f"STREAK_{streak}", 25 + streak * 3)

        # 2x2
        if len(h) >= 4 and h[0] == h[1] and h[2] == h[3] and h[0] != h[2]:
            self._add("PADRAO_2x2", 30)

        # 1x1x1
        if len(h) >= 3 and h[0] != h[1] != h[2]:
            self._add("PADRAO_1x1x1", 20)

        # empate âncora
        if "E" in h[:6]:
            self._add("EMPATE_ANCORA", 10)

    # ==========================
    # PADRÕES COMPOSTOS
    # ==========================
    def _padroes_compostos(self):
        h = self.h

        def blocos(seq):
            res, atual, count = [], seq[0], 1
            for x in seq[1:]:
                if x == atual:
                    count += 1
                else:
                    res.append(count)
                    atual = x
                    count = 1
            res.append(count)
            return res

        b = blocos(h[:30])

        # exemplos estruturais reais
        estruturas = [
            ([4,4,3,2], 60),
            ([3,2,3], 45),
            ([2,1,2,1], 40),
            ([4,3,2,1], 55),
            ([4,4,3,2,3,2,1,2], 75)
        ]

        for estrutura, peso in estruturas:
            if b[:len(estrutura)] == estrutura:
                self._add(f"PADRAO_ESTRUTURAL_{estrutura}", peso)

        # degeneração (encurtando)
        if len(b) >= 4 and b[0] < b[1] < b[2]:
            self._add("DEGENERACAO_PADRAO", 35)

        # inflação (alongando)
        if len(b) >= 4 and b[0] > b[1] > b[2]:
            self._add("INFLACAO_PADRAO", 35)

    # ==========================
    # MEMÓRIA DE CICLOS
    # ==========================
    def _memoria_ciclos(self):
        h = self.h
        if len(h) < 9:
            return

        c1 = h[0:3]
        c2 = h[3:6]
        c3 = h[6:9]

        if c1 == c2 == c3:
            self._add("MEMORIA_3_CICLOS", 50)

        # memória parcial (similaridade)
        if c1 == c2:
            self._add("MEMORIA_PARCIAL", 30)

    # ==========================
    # BRECHA
    # ==========================
    def _avaliar_brecha(self):
        if self.contexto.get("mesa") == "DOMINANTE" and self.contexto.get("ritmo") == "RÁPIDO":
            self.brecha = True
            self.score += 15

    # ==========================
    # DECISÃO FINAL (TRADER)
    # ==========================
    def _decisao_final(self):
        direcao = self._direcao()

        if self.score >= 70:
            return self._saida("ENTRAR", direcao)
        elif self.score >= 35:
            return self._saida("ENTRAR COM ALERTA", direcao)
        else:
            return self._saida("SEGURAR", "Mesa sem edge")

    def _direcao(self):
        ultimo = self.h[0]
        if ultimo == "R":
            return "AZUL"
        if ultimo == "B":
            return "VERMELHO"
        return "SEM COR"

    def _add(self, nome, peso):
        self.padroes.append(f"{nome} (+{peso})")
        self.score += peso

    def _saida(self, acao, direcao):
        return {
            "acao": acao,
            "direcao": direcao,
            "score": self.score,
            "padroes": self.padroes,
            "contexto": self.contexto
        }

# ======================================================
# INTERFACE
# ======================================================
st.title("🎯 Football Studio – Trader IA PROFISSIONAL")

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🔴 VERMELHO"):
        st.session_state.historico.insert(0, "R")
with c2:
    if st.button("🔵 AZUL"):
        st.session_state.historico.insert(0, "B")
with c3:
    if st.button("🟡 EMPATE"):
        st.session_state.historico.insert(0, "E")

st.divider()

# HISTÓRICO
st.subheader("📊 Histórico (mais recente → antigo)")
mapa = {"R":"🔴","B":"🔵","E":"🟡"}
st.write(" ".join(mapa[x] for x in st.session_state.historico[:30]))

# ANÁLISE
ia = TraderIA(st.session_state.historico)
res = ia.executar()

st.divider()
st.subheader("🧠 DECISÃO DO TRADER IA")

if res["acao"] == "ENTRAR":
    st.success(f"✅ ENTRAR → {res['direcao']} | SCORE {res['score']}")
elif res["acao"] == "ENTRAR COM ALERTA":
    st.warning(f"⚠️ ENTRAR COM ALERTA → {res['direcao']} | SCORE {res['score']}")
else:
    st.info("⏳ SEGURAR")

st.write("**Contexto da Mesa:**", res["contexto"])

st.subheader("📌 Padrões Detectados")
if res["padroes"]:
    for p in res["padroes"]:
        st.write("•", p)
else:
    st.write("Nenhum padrão ativo")

if st.button("♻️ RESETAR HISTÓRICO"):
    st.session_state.historico = []
