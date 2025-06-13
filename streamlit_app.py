# 1. IDŐVONAL
with tab1:
    st.header("Fuvarok idővonal nézete")
    df = st.session_state.fuvarok

    # Szűrés megrendelő szerint
    megr_szures = st.selectbox("Szűrés megrendelő szerint", ["Összes"] + st.session_state.megrendelok["Név"].tolist())
    if megr_szures != "Összes":
        df = df[df["Megrendelő"] == megr_szures]

    if not df.empty:
        import altair as alt

        # Altair-nek dátumos adat kell
        chart_data = df.copy()
        chart_data["Rendszám"] = chart_data["Rendszám"].astype(str)
        chart_data["Kezdete"] = pd.to_datetime(chart_data["Kezdete"])
        chart_data["Vége"] = pd.to_datetime(chart_data["Vége"])
        chart_data["időszak"] = chart_data["Vége"] - chart_data["Kezdete"]

        base = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Kezdete:T', title='Kezdési idő'),
            x2='Vége:T',
            y=alt.Y('Rendszám:N', title='Jármű'),
            color=alt.Color('Kategória:N'),
            tooltip=['Fuvar neve', 'Megrendelő', 'Kezdete', 'Vége']
        ).properties(
            height=600
        )

        st.altair_chart(base, use_container_width=True)
    else:
        st.info("Nincs megjeleníthető fuvar.")