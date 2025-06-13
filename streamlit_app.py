import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, time

# Kezdeti állapot
if "fuvarok" not in st.session_state:
    st.session_state.fuvarok = pd.DataFrame(columns=["Rendszám", "Fuvar neve", "Kategória", "Megrendelő", "Kezdete", "Vége"])

if "jarmuvek" not in st.session_state:
    st.session_state.jarmuvek = ["AO-BK-447", "RXD-624"]

if "kategoriak" not in st.session_state:
    st.session_state.kategoriak = ["Belföldi", "Külföldi", "Diákcsoport", "Szerviz"]

if "megrendelok" not in st.session_state:
    st.session_state.megrendelok = pd.DataFrame(columns=["Név", "Telefonszám", "Email"])

# Főcím
st.title("🚌 Fuvarszervező Idővonal Alkalmazás")

# Menüpontok
tab1, tab2, tab3, tab4 = st.tabs(["📅 Idővonal", "➕ Új fuvar", "⚙️ Beállítások", "🧾 Megrendelők"])

# 1. IDŐVONAL nézet
with tab1:
    st.header("Fuvarok idővonal nézete")
    df = st.session_state.fuvarok

    megr_szures = st.selectbox("Szűrés megrendelő szerint", ["Összes"] + st.session_state.megrendelok["Név"].tolist())
    if megr_szures != "Összes":
        df = df[df["Megrendelő"] == megr_szures]

    if not df.empty:
        chart_data = df.copy()
        chart_data["Kezdete"] = pd.to_datetime(chart_data["Kezdete"])
        chart_data["Vége"] = pd.to_datetime(chart_data["Vége"])

        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Kezdete:T', title='Kezdés'),
            x2='Vége:T',
            y=alt.Y('Rendszám:N', title='Jármű'),
            color=alt.Color('Kategória:N', legend=alt.Legend(title="Kategória")),
            tooltip=['Fuvar neve', 'Megrendelő', 'Kezdete', 'Vége']
        ).properties(
            height=600,
            title="🕒 Fuvar idővonal"
        )

        st.altair_chart(chart, use_container_width=True)
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

        kezd_datum = st.date_input("Kezdés dátuma")
        kezd_ido = st.time_input("Kezdés időpontja", value=time(8, 0))
        vege_datum = st.date_input("Befejezés dátuma")
        vege_ido = st.time_input("Befejezés időpontja", value=time(17, 0))

        submitted = st.form_submit_button("✅ Fuvar mentése")
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
            st.success("🚍 Fuvar sikeresen rögzítve!")

# 3. BEÁLLÍTÁSOK
with tab3:
    st.header("Beállítások")

    with st.expander("🚐 Járművek"):
        st.write(st.session_state.jarmuvek)
        uj = st.text_input("Új rendszám")
        if st.button("➕ Hozzáadás"):
            if uj and uj not in st.session_state.jarmuvek:
                st.session_state.jarmuvek.append(uj)
                st.success(f"{uj} hozzáadva")
        torol = st.selectbox("Törlés", [""] + st.session_state.jarmuvek)
        if st.button("❌ Törlés") and torol:
            st.session_state.jarmuvek.remove(torol)
            st.success(f"{torol} törölve")

    with st.expander("🏷️ Kategóriák"):
        st.write(st.session_state.kategoriak)
        ujk = st.text_input("Új kategória")
        if st.button("➕ Kategória"):
            if ujk and ujk not in st.session_state.kategoriak:
                st.session_state.kategoriak.append(ujk)
                st.success(f"{ujk} kategória hozzáadva")
        torolk = st.selectbox("Kategória törlése", [""] + st.session_state.kategoriak)
        if st.button("❌ Kategória törlése") and torolk:
            st.session_state.kategoriak.remove(torolk)
            st.success(f"{torolk} törölve")

# 4. MEGRENDELŐK
with tab4:
    st.header("Megrendelők kezelése")

    with st.form("megrendelo_form"):
        nev = st.text_input("Név")
        tel = st.text_input("Telefonszám")
        email = st.text_input("Email")
        if st.form_submit_button("➕ Megrendelő hozzáadása"):
            if nev and nev not in st.session_state.megrendelok["Név"].values:
                uj = pd.DataFrame([{"Név": nev, "Telefonszám": tel, "Email": email}])
                st.session_state.megrendelok = pd.concat([st.session_state.megrendelok, uj], ignore_index=True)
                st.success(f"{nev} hozzáadva")

    st.subheader("📋 Megrendelők listája")
    st.dataframe(st.session_state.megrendelok, use_container_width=True)

    torolnev = st.selectbox("Törlendő megrendelő", [""] + st.session_state.megrendelok["Név"].tolist())
    if st.button("❌ Megrendelő törlése") and torolnev:
        st.session_state.megrendelok = st.session_state.megrendelok[st.session_state.megrendelok["Név"] != torolnev]
        st.success(f"{torolnev} törölve")