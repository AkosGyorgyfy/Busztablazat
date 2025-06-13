import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Alap adatok
if "fuvarok" not in st.session_state:
    st.session_state.fuvarok = pd.DataFrame(columns=["Rendszám", "Fuvar neve", "Kategória", "Megrendelő", "Kezdete", "Vége"])

if "jarmuvek" not in st.session_state:
    st.session_state.jarmuvek = ["AO-BK-447", "RXD-624"]

if "kategoriak" not in st.session_state:
    st.session_state.kategoriak = ["Belföldi", "Külföldi", "Diákcsoport", "Szerviz"]

if "megrendelok" not in st.session_state:
    st.session_state.megrendelok = []

st.title("🚌 Busz Fuvar Idővonal")

tab1, tab2, tab3, tab4 = st.tabs(["📅 Fuvarok", "➕ Új fuvar", "⚙️ Beállítások", "🧾 Megrendelők"])

# 1. IDŐVONAL NÉZET
with tab1:
    st.header("Fuvarok idővonal nézete")
    df = st.session_state.fuvarok

    megr_szures = st.selectbox("Szűrés megrendelő szerint", ["Összes"] + st.session_state.megrendelok)
    if megr_szures != "Összes":
        df = df[df["Megrendelő"] == megr_szures]

    if not df.empty:
        fig = px.timeline(
            df,
            x_start="Kezdete",
            x_end="Vége",
            y="Rendszám",
            color="Kategória",
            text="Fuvar neve",
            title="Busz Fuvar Idővonal"
        )
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nincs megjeleníthető fuvar.")

# 2. FUVAR HOZZÁADÁS
with tab2:
    st.header("Új fuvar rögzítése")
    with st.form("fuvar_form"):
        rendszam = st.selectbox("Rendszám", st.session_state.jarmuvek)
        nev = st.text_input("Fuvar neve")
        kategoria = st.selectbox("Kategória", st.session_state.kategoriak)
        megrendelo = st.selectbox("Megrendelő", [""] + st.session_state.megrendelok)
        kezdete = st.date_input("Kezdő dátum")
        vege = st.date_input("Vége dátum")

        submitted = st.form_submit_button("Fuvar mentése")
        if submitted:
            uj_sor = pd.DataFrame([{
                "Rendszám": rendszam,
                "Fuvar neve": nev,
                "Kategória": kategoria,
                "Megrendelő": megrendelo,
                "Kezdete": datetime.combine(kezdete, datetime.min.time()),
                "Vége": datetime.combine(vege, datetime.min.time())
            }])
            st.session_state.fuvarok = pd.concat([st.session_state.fuvarok, uj_sor], ignore_index=True)
            st.success("Fuvar sikeresen hozzáadva!")

# 3. BEÁLLÍTÁSOK
with tab3:
    st.header("Beállítások")

    with st.expander("🚍 Járművek"):
        uj_jarmu = st.text_input("Új rendszám hozzáadása")
        if st.button("Hozzáadás"):
            if uj_jarmu and uj_jarmu not in st.session_state.jarmuvek:
                st.session_state.jarmuvek.append(uj_jarmu)
                st.success(f"{uj_jarmu} hozzáadva")

    with st.expander("🏷️ Kategóriák"):
        uj_kategoria = st.text_input("Új kategória hozzáadása")
        if st.button("Kategória hozzáadása"):
            if uj_kategoria and uj_kategoria not in st.session_state.kategoriak:
                st.session_state.kategoriak.append(uj_kategoria)
                st.success(f"{uj_kategoria} kategória hozzáadva")

# 4. MEGRENDELŐK
with tab4:
    st.header("Megrendelők kezelése")
    uj_megrendelo = st.text_input("Új megrendelő neve")
    if st.button("Megrendelő hozzáadása"):
        if uj_megrendelo and uj_megrendelo not in st.session_state.megrendelok:
            st.session_state.megrendelok.append(uj_megrendelo)
            st.success(f"{uj_megrendelo} megrendelő hozzáadva")