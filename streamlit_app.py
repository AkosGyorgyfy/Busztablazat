import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, time

# Kezdeti adatok
if "fuvarok" not in st.session_state:
    st.session_state.fuvarok = pd.DataFrame(columns=["Rendszám", "Fuvar neve", "Kategória", "Megrendelő", "Kezdete", "Vége"])

if "jarmuvek" not in st.session_state:
    st.session_state.jarmuvek = ["AO-BK-447", "RXD-624"]

if "kategoriak" not in st.session_state:
    st.session_state.kategoriak = ["Belföldi", "Külföldi", "Diákcsoport", "Szerviz"]

if "megrendelok" not in st.session_state:
    st.session_state.megrendelok = pd.DataFrame(columns=["Név", "Telefonszám", "Email"])

st.title("🚌 Fuvarszervező Idővonal Alkalmazás")

tab1, tab2, tab3, tab4 = st.tabs(["📅 Idővonal", "➕ Új fuvar", "⚙️ Beállítások", "🧾 Megrendelők"])

# 1. IDŐVONAL
with tab1:
    st.header("Fuvarok idővonal nézete")
    df = st.session_state.fuvarok

    # Szűrés megrendelő szerint
    megr_szures = st.selectbox("Szűrés megrendelő szerint", ["Összes"] + st.session_state.megrendelok["Név"].tolist())
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
        )
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(height=800, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nincs megjeleníthető fuvar.")

# 2. ÚJ FUVAR
with tab2:
    st.header("Új fuvar rögzítése")
    with st.form("fuvar_form"):
        rendszam = st.selectbox("Rendszám", st.session_state.jarmuvek)
        nev = st.text_input("Fuvar neve")
        kategoria = st.selectbox("Kategória", st.session_state.kategoriak)
        megrendelo = st.selectbox("Megrendelő", [""] + st.session_state.megrendelok["Név"].tolist())

        kezd_datum = st.date_input("Kezdő dátum")
        kezd_ido = st.time_input("Kezdés időpontja", value=time(8, 0))
        vege_datum = st.date_input("Záró dátum")
        vege_ido = st.time_input("Befejezés időpontja", value=time(17, 0))

        submitted = st.form_submit_button("Fuvar mentése")
        if submitted:
            kezdet = datetime.combine(kezd_datum, kezd_ido)
            vege = datetime.combine(vege_datum, vege_ido)
            uj_sor = pd.DataFrame([{
                "Rendszám": rendszam,
                "Fuvar neve": nev,
                "Kategória": kategoria,
                "Megrendelő": megrendelo,
                "Kezdete": kezdet,
                "Vége": vege
            }])
            st.session_state.fuvarok = pd.concat([st.session_state.fuvarok, uj_sor], ignore_index=True)
            st.success("Fuvar sikeresen hozzáadva!")

# 3. BEÁLLÍTÁSOK
with tab3:
    st.header("Beállítások")

    # Járművek kezelése
    with st.expander("🚍 Járművek kezelése"):
        st.write("**Aktív járművek:**")
        st.write(st.session_state.jarmuvek)
        col1, col2 = st.columns(2)
        with col1:
            uj_jarmu = st.text_input("Új rendszám")
        with col2:
            if st.button("➕ Hozzáadás", key="jarmu_hozza"):
                if uj_jarmu and uj_jarmu not in st.session_state.jarmuvek:
                    st.session_state.jarmuvek.append(uj_jarmu)
                    st.success(f"{uj_jarmu} hozzáadva")
        rendszam_torol = st.selectbox("Rendszám törlése", [""] + st.session_state.jarmuvek)
        if st.button("❌ Törlés", key="jarmu_torol") and rendszam_torol:
            st.session_state.jarmuvek.remove(rendszam_torol)
            st.success(f"{rendszam_torol} törölve")

    # Kategóriák kezelése
    with st.expander("🏷️ Kategóriák kezelése"):
        st.write("**Aktív kategóriák:**")
        st.write(st.session_state.kategoriak)
        uj_kategoria = st.text_input("Új kategória")
        if st.button("➕ Kategória hozzáadása"):
            if uj_kategoria and uj_kategoria not in st.session_state.kategoriak:
                st.session_state.kategoriak.append(uj_kategoria)
                st.success(f"{uj_kategoria} kategória hozzáadva")
        torlendo_kategoria = st.selectbox("Kategória törlése", [""] + st.session_state.kategoriak)
        if st.button("❌ Kategória törlése") and torlendo_kategoria:
            st.session_state.kategoriak.remove(torlendo_kategoria)
            st.success(f"{torlendo_kategoria} törölve")

# 4. MEGRENDELŐK
with tab4:
    st.header("Megrendelők kezelése")

    with st.form("megrendelo_form"):
        nev = st.text_input("Név")
        telefon = st.text_input("Telefonszám")
        email = st.text_input("Email cím")
        hozzaad = st.form_submit_button("➕ Megrendelő hozzáadása")

        if hozzaad:
            if nev and nev not in st.session_state.megrendelok["Név"].values:
                uj = pd.DataFrame([{"Név": nev, "Telefonszám": telefon, "Email": email}])
                st.session_state.megrendelok = pd.concat([st.session_state.megrendelok, uj], ignore_index=True)
                st.success(f"{nev} hozzáadva")

    st.subheader("Megrendelők listája")
    st.dataframe(st.session_state.megrendelok, use_container_width=True)

    torol_megr = st.selectbox("Törlendő megrendelő", [""] + st.session_state.megrendelok["Név"].tolist())
    if st.button("❌ Megrendelő törlése") and torol_megr:
        st.session_state.megrendelok = st.session_state.megrendelok[st.session_state.megrendelok["Név"] != torol_megr]
        st.success(f"{torol_megr} törölve")