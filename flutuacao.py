import streamlit as st
from math import radians, tan

# Funções
def F_solicitante(a_caixa, b_caixa, h_fundo, esp_parede, L_aba, prof_na):
    area_fundo = (a_caixa + 2 * esp_parede + 2 * L_aba) * (b_caixa + 2 * esp_parede + 2 * L_aba)
    return area_fundo * (prof_na + h_fundo) * 10

def F_resistente(a_caixa, b_caixa, h_caixa, esp_parede, h_fundo, L_aba, peso_esp_solo, cunha=0, peso_esp_concreto=25):
    peso_paredes = (2 * a_caixa + 2 * b_caixa) * esp_parede * h_caixa * peso_esp_concreto
    peso_laje = (a_caixa + 2 * esp_parede + 2 * L_aba) * (b_caixa + 2 * esp_parede + 2 * L_aba) * h_fundo * peso_esp_concreto
    peso_solo = ((a_caixa + 2 * esp_parede + 2 * L_aba)**2 - (a_caixa + 2*esp_parede)**2) * h_caixa * peso_esp_solo
    peso_cunha = h_caixa**2 * tan(radians(cunha)) * (2 * a_caixa + 2 * b_caixa + 8 * esp_parede) * peso_esp_solo / 2
    return peso_paredes + peso_laje + peso_solo + peso_cunha, peso_paredes, peso_laje, peso_solo, peso_cunha

# Interface
st.set_page_config(page_title="Verificação de Flutuação", layout="centered")
st.title("Verificação de Flutuação da Caixa")
st.header("Eng. Guilherme Vick")
st.header("Parâmetros de Entrada")
st.image("caixa.png", caption="Esquema ilustrativo da geometria", use_column_width=True)
a = st.number_input("a_caixa (largura interna) [m]", value=36.0)
b = st.number_input("b_caixa (comprimento interno) [m]", value=25.0)
h_caixa = st.number_input("Altura da caixa [m]", value=15.0)
prof_na = st.number_input("Profundidade do nível d'água (NA) [m]", value=15.0)
L_aba = st.number_input("Largura da aba [m]", value=5.0)
e_par = st.number_input("Espessura da parede [m]", value=1.5)
h_fundo = st.number_input("Espessura da laje de fundo [m]", value=2.0)
peso_solo = st.number_input("Peso específico do solo [kN/m³]", value=17.0)
cunha = st.number_input("Ângulo da cunha (º)", value=0.0)

if st.button("Calcular"):
    solicitantes = F_solicitante(a, b, h_fundo, e_par, L_aba, prof_na)
    resistentes, p_paredes, p_laje, p_solo, p_cunha = F_resistente(
        a, b, h_caixa, e_par, h_fundo, L_aba, peso_solo, cunha
    )
    fs = resistentes / solicitantes if solicitantes > 0 else float('inf')

    st.header("Resultados")
    st.write(f"Forças solicitantes: **{solicitantes:.2f} kN**")
    st.write(f"Forças resistentes: **{resistentes:.2f} kN**")
    st.metric("Fator de segurança à flutuação", f"{fs:.2f}")

    with st.expander("Detalhamento dos pesos resistentes"):
        st.write(f"Peso das paredes: **{p_paredes:.2f} kN**")
        st.write(f"Peso da laje de fundo: **{p_laje:.2f} kN**")
        st.write(f"Peso do solo sobre aba: **{p_solo:.2f} kN**")
        st.write(f"Peso da cunha: **{p_cunha:.2f} kN**")
