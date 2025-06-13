import streamlit as st
import pandas as pd
import datetime
import uuid

# ======= ALAP ADATSTRUKTÚRÁK =======
# Session state inicializálása, ha még nem létezik
if 'fuvarok' not in st.session_state:
    st.session_state.fuvarok = []

if 'gepjarmuvek' not in st.session_state:
    st.session_state.gepjarmuvek = [
        {"id": "1", "rendszam": "ABC-123", "tipus": "Mercedes", "evjarat": 2019, "ferohely": 50},
        {"id": "2", "rendszam": "DEF-456", "tipus": "Volvo", "evjarat": 2020, "ferohely": 60}
    ]

if 'kategoriak' not in st.session_state:
    st.session_state.kategoriak = [
        {"id": "1", "nev": "Normál fuvar", "szin": "#FFD700"},
        {"id": "2", "nev": "Speciális fuvar", "szin": "#9932CC"},
        {"id": "3", "nev": "Karbantartás", "szin": "#4169E1"},
        {"id": "4", "nev": "Szerviz", "szin": "#FF8C00"},
        {"id": "5", "nev": "Pihenőnap", "szin": "#808080"}
    ]

if 'megrendelok' not in st.session_state:
    st.session_state.megrendelok = [
        {"id": "1", "nev": "Budapest Közlekedési Zrt.", "kapcsolattarto": "Kovács János", "telefon": "+3611234567", "email": "kovacs@bkv.hu"},
        {"id": "2", "nev": "Volánbusz", "kapcsolattarto": "Nagy Erzsébet", "telefon": "+3619876543", "email": "nagy@volanbusz.hu"}
    ]

# ======= SEGÉDFÜGGVÉNYEK =======
def get_object_by_id(array, id_value):
    """Visszaadja az objektumot az ID alapján"""
    for item in array:
        if item["id"] == id_value:
            return item
    return None

def get_name_by_id(array, id_value):
    """Visszaadja a nevet az ID alapján"""
    item = get_object_by_id(array, id_value)
    return item["nev"] if item else "Ismeretlen"

# ======= ALKALMAZÁS FUNKCIÓK =======
def fooldal():
    """Főoldal nézet"""
    st.markdown("## Üdvözöljük a Busz Fuvar Kezelő alkalmazásban!")
    
    # Egyszerű statisztikák
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Buszok száma", len(st.session_state.gepjarmuvek))
    with col2:
        st.metric("Megrendelők száma", len(st.session_state.megrendelok))
    with col3:
        st.metric("Fuvarok száma", len(st.session_state.fuvarok))

def uj_fuvar():
    """Új fuvar felvétele űrlap"""
    st.markdown("## Új fuvar felvétele")
    
    with st.form("uj_fuvar_form"):
        # Gépjármű kiválasztása
        busz_options = [f"{b['rendszam']} ({b['tipus']})" for b in st.session_state.gepjarmuvek]
        busz_index = st.selectbox("Busz", options=range(len(busz_options)), format_func=lambda x: busz_options[x])
        
        # Kategória kiválasztása
        kategoria_options = [k["nev"] for k in st.session_state.kategoriak]
        kategoria_index = st.selectbox("Kategória", options=range(len(kategoria_options)), format_func=lambda x: kategoria_options[x])
        
        # Megrendelő kiválasztása
        megrendelo_options = ["Nincs megrendelő"] + [m["nev"] for m in st.session_state.megrendelok]
        megrendelo_index = st.selectbox("Megrendelő", options=range(len(megrendelo_options)), format_func=lambda x: megrendelo_options[x])
        
        # Dátum és idő
        datum = st.date_input("Dátum", value=datetime.datetime.now())
        col1, col2 = st.columns(2)
        with col1:
            kezdes = st.time_input("Kezdés")
        with col2:
            vege = st.time_input("Vége")
        
        # Cél és megjegyzés
        cel = st.text_input("Úticél")
        megjegyzes = st.text_area("Megjegyzés")
        
        submitted = st.form_submit_button("Mentés")
        if submitted:
            # Fuvar létrehozása
            uj_fuvar_obj = {
                "id": str(uuid.uuid4()),
                "busz_id": st.session_state.gepjarmuvek[busz_index]["id"],
                "kategoria_id": st.session_state.kategoriak[kategoria_index]["id"],
                "megrendelo_id": None if megrendelo_index == 0 else st.session_state.megrendelok[megrendelo_index-1]["id"],
                "datum": datum.isoformat(),
                "kezdes": kezdes.strftime("%H:%M"),
                "vege": vege.strftime("%H:%M"),
                "cel": cel,
                "megjegyzes": megjegyzes
            }
            
            # Fuvar hozzáadása a listához
            st.session_state.fuvarok.append(uj_fuvar_obj)
            st.success("Fuvar sikeresen hozzáadva!")

def fuvarok_listaja():
    """Fuvarok listázása és szűrése"""
    st.markdown("## Fuvarok listája")
    
    # Szűrők
    st.markdown("### Szűrési lehetőségek")
    col1, col2, col3 = st.columns(3)
    with col1:
        # Busz szűrő
        busz_filter = st.selectbox(
            "Busz", 
            options=["Mind"] + [b["rendszam"] for b in st.session_state.gepjarmuvek]
        )
    with col2:
        # Kategória szűrő
        kategoria_filter = st.selectbox(
            "Kategória", 
            options=["Mind"] + [k["nev"] for k in st.session_state.kategoriak]
        )
    with col3:
        # Megrendelő szűrő
        megrendelo_filter = st.selectbox(
            "Megrendelő", 
            options=["Mind"] + [m["nev"] for m in st.session_state.megrendelok]
        )
    
    # Lista megjelenítése
    st.markdown("### Találatok")
    if not st.session_state.fuvarok:
        st.info("Nincsenek rögzített fuvarok.")
    else:
        # Szűrés
        filtered_fuvarok = st.session_state.fuvarok.copy()
        
        # Busz szűrés
        if busz_filter != "Mind":
            busz_id = next((b["id"] for b in st.session_state.gepjarmuvek if b["rendszam"] == busz_filter), None)
            filtered_fuvarok = [f for f in filtered_fuvarok if f["busz_id"] == busz_id]
        
        # Kategória szűrés
        if kategoria_filter != "Mind":
            kategoria_id = next((k["id"] for k in st.session_state.kategoriak if k["nev"] == kategoria_filter), None)
            filtered_fuvarok = [f for f in filtered_fuvarok if f["kategoria_id"] == kategoria_id]
        
        # Megrendelő szűrés
        if megrendelo_filter != "Mind":
            megrendelo_id = next((m["id"] for m in st.session_state.megrendelok if m["nev"] == megrendelo_filter), None)
            filtered_fuvarok = [f for f in filtered_fuvarok if f["megrendelo_id"] == megrendelo_id]
        
        # Megjelenítés táblázatban
        if not filtered_fuvarok:
            st.warning("Nincs a szűrési feltételeknek megfelelő fuvar.")
        else:
            # Táblázat adatok előkészítése
            table_data = []
            for f in filtered_fuvarok:
                busz = get_object_by_id(st.session_state.gepjarmuvek, f["busz_id"])
                kategoria = get_object_by_id(st.session_state.kategoriak, f["kategoria_id"])
                megrendelo = get_object_by_id(st.session_state.megrendelok, f["megrendelo_id"]) if f["megrendelo_id"] else {"nev": "-"}
                
                table_data.append({
                    "Rendszám": busz["rendszam"] if busz else "Ismeretlen",
                    "Kategória": kategoria["nev"] if kategoria else "Ismeretlen",
                    "Megrendelő": megrendelo["nev"],
                    "Dátum": f["datum"],
                    "Kezdés": f["kezdes"],
                    "Vége": f["vege"],
                    "Cél": f["cel"],
                    "Megjegyzés": f["megjegyzes"]
                })
            
            # Táblázat megjelenítése
            st.dataframe(table_data, use_container_width=True)

def admin_panel():
    """Admin panel a beállításokhoz"""
    st.markdown("## Admin beállítások")
    
    tab1, tab2, tab3 = st.tabs(["Kategóriák", "Gépjárművek", "Megrendelők"])
    
    # Kategóriák kezelése
    with tab1:
        st.markdown("### Kategóriák kezelése")
        
        # Meglévő kategóriák
        for i, kategoria in enumerate(st.session_state.kategoriak):
            with st.expander(f"{kategoria['nev']} - {kategoria['szin']}"):
                with st.form(f"kategoria_form_{i}"):
                    nev = st.text_input("Kategória neve", value=kategoria["nev"])
                    szin = st.color_picker("Színkód", value=kategoria["szin"])
                    submit = st.form_submit_button("Módosítás")
                    
                    if submit:
                        st.session_state.kategoriak[i]["nev"] = nev
                        st.session_state.kategoriak[i]["szin"] = szin
                        st.success("Kategória módosítva!")
        
        # Új kategória
        with st.expander("+ Új kategória hozzáadása"):
            with st.form("uj_kategoria_form"):
                uj_nev = st.text_input("Kategória neve")
                uj_szin = st.color_picker("Színkód", value="#3498db")
                submit = st.form_submit_button("Hozzáadás")
                
                if submit and uj_nev:
                    uj_kategoria = {
                        "id": str(uuid.uuid4()),
                        "nev": uj_nev,
                        "szin": uj_szin
                    }
                    st.session_state.kategoriak.append(uj_kategoria)
                    st.success("Új kategória hozzáadva!")
                    st.experimental_rerun()
    
    # Gépjárművek kezelése
    with tab2:
        st.markdown("### Gépjárművek kezelése")
        
        # Meglévő gépjárművek
        for i, gepjarmu in enumerate(st.session_state.gepjarmuvek):
            with st.expander(f"{gepjarmu['rendszam']} - {gepjarmu['tipus']}"):
                with st.form(f"gepjarmu_form_{i}"):
                    rendszam = st.text_input("Rendszám", value=gepjarmu["rendszam"])
                    tipus = st.text_input("Típus", value=gepjarmu["tipus"])
                    evjarat = st.number_input("Évjárat", value=gepjarmu["evjarat"], min_value=1990, max_value=2030)
                    ferohely = st.number_input("Férőhelyek száma", value=gepjarmu["ferohely"], min_value=1, max_value=100)
                    submit = st.form_submit_button("Módosítás")
                    
                    if submit:
                        st.session_state.gepjarmuvek[i]["rendszam"] = rendszam
                        st.session_state.gepjarmuvek[i]["tipus"] = tipus
                        st.session_state.gepjarmuvek[i]["evjarat"] = evjarat
                        st.session_state.gepjarmuvek[i]["ferohely"] = ferohely
                        st.success("Gépjármű módosítva!")
        
        # Új gépjármű
        with st.expander("+ Új gépjármű hozzáadása"):
            with st.form("uj_gepjarmu_form"):
                uj_rendszam = st.text_input("Rendszám")
                uj_tipus = st.text_input("Típus")
                uj_evjarat = st.number_input("Évjárat", min_value=1990, max_value=2030, value=2023)
                uj_ferohely = st.number_input("Férőhelyek száma", min_value=1, max_value=100, value=50)
                submit = st.form_submit_button("Hozzáadás")
                
                if submit and uj_rendszam and uj_tipus:
                    uj_gepjarmu = {
                        "id": str(uuid.uuid4()),
                        "rendszam": uj_rendszam,
                        "tipus": uj_tipus,
                        "evjarat": uj_evjarat,
                        "ferohely": uj_ferohely
                    }
                    st.session_state.gepjarmuvek.append(uj_gepjarmu)
                    st.success("Új gépjármű hozzáadva!")
                    st.experimental_rerun()
    
    # Megrendelők kezelése
    with tab3:
        st.markdown("### Megrendelők kezelése")
        
        # Meglévő megrendelők
        for i, megrendelo in enumerate(st.session_state.megrendelok):
            with st.expander(f"{megrendelo['nev']} - {megrendelo['kapcsolattarto']}"):
                with st.form(f"megrendelo_form_{i}"):
                    nev = st.text_input("Megrendelő neve", value=megrendelo["nev"])
                    kapcsolattarto = st.text_input("Kapcsolattartó", value=megrendelo["kapcsolattarto"])
                    telefon = st.text_input("Telefonszám", value=megrendelo["telefon"])
                    email = st.text_input("E-mail cím", value=megrendelo["email"])
                    submit = st.form_submit_button("Módosítás")
                    
                    if submit:
                        st.session_state.megrendelok[i]["nev"] = nev
                        st.session_state.megrendelok[i]["kapcsolattarto"] = kapcsolattarto
                        st.session_state.megrendelok[i]["telefon"] = telefon
                        st.session_state.megrendelok[i]["email"] = email
                        st.success("Megrendelő módosítva!")
        
        # Új megrendelő
        with st.expander("+ Új megrendelő hozzáadása"):
            with st.form("uj_megrendelo_form"):
                uj_nev = st.text_input("Megrendelő neve")
                uj_kapcsolattarto = st.text_input("Kapcsolattartó")
                uj_telefon = st.text_input("Telefonszám")
                uj_email = st.text_input("E-mail cím")
                submit = st.form_submit_button("Hozzáadás")
                
                if submit and uj_nev:
                    uj_megrendelo = {
                        "id": str(uuid.uuid4()),
                        "nev": uj_nev,
                        "kapcsolattarto": uj_kapcsolattarto,
                        "telefon": uj_telefon,
                        "email": uj_email
                    }
                    st.session_state.megrendelok.append(uj_megrendelo)
                    st.success("Új megrendelő hozzáadva!")
                    st.experimental_rerun()

def idovonal_nezet():
    """Idővonalas megjelenítés"""
    st.markdown("## Idővonalas nézet")
    
    if not st.session_state.fuvarok:
        st.info("Nincsenek megjeleníthető fuvarok.")
        return
    
    # Egyszerű idővonalas megjelenítés
    st.markdown("### Buszok fuvarjai")
    
    # Fuvarok rendezése
    sorted_fuvarok = sorted(st.session_state.fuvarok, key=lambda x: x["datum"])
    
    # Buszok szerint csoportosítás
    for gepjarmu in st.session_state.gepjarmuvek:
        bus_fuvarok = [f for f in sorted_fuvarok if f["busz_id"] == gepjarmu["id"]]
        
        if bus_fuvarok:
            st.markdown(f"#### {gepjarmu['rendszam']} ({gepjarmu['tipus']})")
            
            for fuvar in bus_fuvarok:
                kategoria = get_object_by_id(st.session_state.kategoriak, fuvar["kategoria_id"])
                megrendelo = get_object_by_id(st.session_state.megrendelok, fuvar["megrendelo_id"]) if fuvar["megrendelo_id"] else {"nev": "Nincs megrendelő"}
                
                # Színes doboz HTML-lel
                szin = kategoria["szin"] if kategoria else "#999999"
                
                # HTML kártya az idővonalon
                html = f"""
                <div style="margin: 10px 0; padding: 10px; border-radius: 5px; background-color: {szin}; color: white;">
                    <div style="font-weight: bold;">{kategoria['nev'] if kategoria else 'Ismeretlen kategória'}</div>
                    <div>Dátum: {fuvar['datum']}</div>
                    <div>Idő: {fuvar['kezdes']} - {fuvar['vege']}</div>
                    <div>Cél: {fuvar['cel']}</div>
                    <div>Megrendelő: {megrendelo['nev']}</div>
                    <div>Megjegyzés: {fuvar['megjegyzes']}</div>
                </div>
                """
                st.markdown(html, unsafe_allow_html=True)

# ======= FŐPROGRAM =======
def main():
    st.set_page_config(
        page_title="Busz Fuvar Kezelő",
        page_icon="🚌",
        layout="wide"
    )
    
    st.title("🚌 Busz Fuvar Kezelő")
    
    # Menü
    menu = st.sidebar.radio(
        "Navigáció",
        ["Főoldal", "Új fuvar", "Fuvarok listája", "Idővonalas nézet", "Admin beállítások"]
    )
    
    # Oldal betöltése a menü alapján
    if menu == "Főoldal":
        fooldal()
    elif menu == "Új fuvar":
        uj_fuvar()
    elif menu == "Fuvarok listája":
        fuvarok_listaja()
    elif menu == "Idővonalas nézet":
        idovonal_nezet()
    elif menu == "Admin beállítások":
        admin_panel()

if __name__ == "__main__":
    main()