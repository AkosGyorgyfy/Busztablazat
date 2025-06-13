import streamlit as st
import pandas as pd
import datetime
import uuid

# AlkalmazÃ¡s konfigurÃ¡ciÃ³
st.set_page_config(
    page_title="Busz Fuvar KezelÅ‘", 
    page_icon="ðŸšŒ"
)

# AdatinicializÃ¡lÃ¡s
def init_data():
    """AlapÃ©rtelmezett adatok betÃ¶ltÃ©se"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        
        # Fuvar kategÃ³riÃ¡k
        st.session_state.kategoriak = pd.DataFrame([
            {'id': str(uuid.uuid4()), 'nev': 'NormÃ¡l fuvar', 'szin': '#FFD700'},
            {'id': str(uuid.uuid4()), 'nev': 'SpeciÃ¡lis fuvar', 'szin': '#9932CC'},
            {'id': str(uuid.uuid4()), 'nev': 'KarbantartÃ¡s', 'szin': '#4169E1'},
            {'id': str(uuid.uuid4()), 'nev': 'Szerviz', 'szin': '#FF8C00'},
            {'id': str(uuid.uuid4()), 'nev': 'PihenÅ‘nap', 'szin': '#808080'}
        ])
        
        # GÃ©pjÃ¡rmÅ±vek
        st.session_state.buszok = pd.DataFrame([
            {'id': str(uuid.uuid4()), 'rendszam': 'ABC-123', 'tipus': 'Mercedes Benz Citaro', 'evjarat': 2019, 'ferohely': 50},
            {'id': str(uuid.uuid4()), 'rendszam': 'DEF-456', 'tipus': 'Volvo 7900', 'evjarat': 2020, 'ferohely': 60},
            {'id': str(uuid.uuid4()), 'rendszam': 'GHI-789', 'tipus': 'Scania Citywide', 'evjarat': 2021, 'ferohely': 45}
        ])
        
        # MegrendelÅ‘k
        st.session_state.megrendelok = pd.DataFrame([
            {'id': str(uuid.uuid4()), 'nev': 'Budapest KÃ¶zlekedÃ©si KÃ¶zpont', 'kapcsolattarto': 'KovÃ¡cs JÃ¡nos', 'telefon': '+36-1-123-4567', 'email': 'kovacs@bkk.hu'},
            {'id': str(uuid.uuid4()), 'nev': 'VolÃ¡nbusz Zrt.', 'kapcsolattarto': 'Nagy Anna', 'telefon': '+36-1-987-6543', 'email': 'nagy@volanbusz.hu'},
            {'id': str(uuid.uuid4()), 'nev': 'Flixbus MagyarorszÃ¡g', 'kapcsolattarto': 'Schmidt PÃ©ter', 'telefon': '+36-30-555-0123', 'email': 'schmidt@flixbus.hu'}
        ])
        
        # Fuvarok
        st.session_state.fuvarok = pd.DataFrame(columns=[
            'id', 'busz_id', 'kategoria_id', 'megrendelo_id', 
            'datum', 'kezdes', 'vege', 'cel', 'megjegyzes'
        ])

init_data()

# SegÃ©dfÃ¼ggvÃ©nyek
def get_name_by_id(dataframe, target_id, name_column='nev'):
    """ID alapjÃ¡n nÃ©v keresÃ©se"""
    try:
        if not dataframe.empty and target_id in dataframe['id'].values:
            return dataframe[dataframe['id'] == target_id][name_column].iloc[0]
        return 'Ismeretlen'
    except (KeyError, IndexError):
        return 'Ismeretlen'

def get_id_by_name(dataframe, name, name_column='nev'):
    """NÃ©v alapjÃ¡n ID keresÃ©se"""
    try:
        if not dataframe.empty and name in dataframe[name_column].values:
            return dataframe[dataframe[name_column] == name]['id'].iloc[0]
        return None
    except (KeyError, IndexError):
        return None

# FÅ‘oldal
def fooldal():
    st.title("ðŸšŒ Busz Fuvar KezelÅ‘ Rendszer")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Buszok szÃ¡ma", len(st.session_state.buszok))
    with col2:
        st.metric("KategÃ³riÃ¡k", len(st.session_state.kategoriak))
    with col3:
        st.metric("MegrendelÅ‘k", len(st.session_state.megrendelok))
    with col4:
        st.metric("Fuvarok", len(st.session_state.fuvarok))
    
    st.subheader("UtolsÃ³ fuvarok")
    if not st.session_state.fuvarok.empty:
        display_df = st.session_state.fuvarok.copy()
        display_df['Busz'] = display_df['busz_id'].apply(lambda x: get_name_by_id(st.session_state.buszok, x, 'rendszam'))
        display_df['KategÃ³ria'] = display_df['kategoria_id'].apply(lambda x: get_name_by_id(st.session_state.kategoriak, x))
        
        st.dataframe(
            display_df[['Busz', 'KategÃ³ria', 'datum', 'kezdes', 'vege', 'cel']].tail(),
            use_container_width=True
        )
    else:
        st.info("MÃ©g nincsenek fuvarok rÃ¶gzÃ­tve.")

# Ãšj fuvar hozzÃ¡adÃ¡sa
def uj_fuvar():
    st.header("Ãšj fuvar hozzÃ¡adÃ¡sa")
    
    with st.form("uj_fuvar_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            busz = st.selectbox(
                "Busz kivÃ¡lasztÃ¡sa", 
                options=st.session_state.buszok['rendszam'].tolist()
            )
            kategoria = st.selectbox(
                "Fuvar tÃ­pusa", 
                options=st.session_state.kategoriak['nev'].tolist()
            )
            megrendelo = st.selectbox(
                "MegrendelÅ‘", 
                options=[''] + st.session_state.megrendelok['nev'].tolist()
            )
        
        with col2:
            datum = st.date_input("DÃ¡tum", value=datetime.date.today())
            kezdes = st.time_input("KezdÃ©s")
            vege = st.time_input("BefejezÃ©s")
        
        cel = st.text_input("ÃšticÃ©l")
        megjegyzes = st.text_area("MegjegyzÃ©s")
        
        submit = st.form_submit_button("Fuvar mentÃ©se")
        
        if submit:
            try:
                busz_id = get_id_by_name(st.session_state.buszok, busz, 'rendszam')
                kategoria_id = get_id_by_name(st.session_state.kategoriak, kategoria)
                megrendelo_id = get_id_by_name(st.session_state.megrendelok, megrendelo) if megrendelo else None
                
                new_fuvar = pd.DataFrame([{
                    'id': str(uuid.uuid4()),
                    'busz_id': busz_id,
                    'kategoria_id': kategoria_id,
                    'megrendelo_id': megrendelo_id,
                    'datum': datum,
                    'kezdes': kezdes,
                    'vege': vege,
                    'cel': cel,
                    'megjegyzes': megjegyzes
                }])
                
                st.session_state.fuvarok = pd.concat(
                    [st.session_state.fuvarok, new_fuvar], 
                    ignore_index=True
                )
                st.success("Fuvar sikeresen hozzÃ¡adva!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Hiba tÃ¶rtÃ©nt: {str(e)}")

# IdÅ‘vonalas nÃ©zet egyszerÅ± HTML alapÃº megoldÃ¡ssal
def idovonal():
    st.header("IdÅ‘vonalas megjelenÃ­tÃ©s")
    
    if st.session_state.fuvarok.empty:
        st.warning("Nincs megjelenÃ­thetÅ‘ fuvar. Adjon hozzÃ¡ fuvarokat a 'Ãšj fuvar' menÃ¼pontban!")
        return
    
    try:
        # HTML megjelenÃ­tÃ©s
        timeline_html = """
        <style>
        .timeline-container {
            font-family: Arial, sans-serif;
            padding: 20px;
            background: #f7f7f7;
            border-radius: 10px;
        }
        .bus-row {
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #ddd;
        }
        .bus-name {
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 5px;
        }
        .event {
            display: inline-block;
            padding: 8px 10px;
            margin: 3px;
            border-radius: 4px;
            color: white;
            font-size: 14px;
        }
        </style>
        <div class="timeline-container">
        """
        
        # Adatok rendezÃ©se buszok szerint
        df = st.session_state.fuvarok.copy()
        df['busz_nev'] = df['busz_id'].apply(lambda x: get_name_by_id(st.session_state.buszok, x, 'rendszam'))
        df['kategoria_nev'] = df['kategoria_id'].apply(lambda x: get_name_by_id(st.session_state.kategoriak, x))
        df['kategoria_szin'] = df['kategoria_id'].apply(
            lambda x: st.session_state.kategoriak[st.session_state.kategoriak['id'] == x]['szin'].iloc[0] 
            if x in st.session_state.kategoriak['id'].values else '#999999'
        )
        df['megrendelo_nev'] = df['megrendelo_id'].apply(
            lambda x: get_name_by_id(st.session_state.megrendelok, x) if pd.notnull(x) else ""
        )
        
        # RendezÃ©s busz Ã©s dÃ¡tum szerint
        df = df.sort_values(['busz_nev', 'datum', 'kezdes'])
        
        # HTML generÃ¡lÃ¡sa buszonkÃ©nt
        for busz in df['busz_nev'].unique():
            timeline_html += f'<div class="bus-row"><div class="bus-name">{busz}</div>'
            busz_events = df[df['busz_nev'] == busz]
            
            for _, event in busz_events.iterrows():
                tooltip = f"{event['datum']} {event['kezdes']}-{event['vege']}: {event['cel']}"
                if event['megrendelo_nev']:
                    tooltip += f" ({event['megrendelo_nev']})"
                
                timeline_html += f"""
                <div class="event" style="background-color: {event['kategoria_szin']};" 
                     title="{tooltip}">
                    {event['kategoria_nev']}: {event['cel']}
                </div>
                """
            
            timeline_html += '</div>'
        
        timeline_html += '</div>'
        
        # MegjelenÃ­tÃ©s
        st.markdown(timeline_html, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Hiba az idÅ‘vonal megjelenÃ­tÃ©sekor: {str(e)}")

# SzÅ±rÃ©s
def szures():
    st.header("Fuvarok szÅ±rÃ©se")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_busz = st.selectbox(
            "Busz", 
            options=["Mind"] + st.session_state.buszok['rendszam'].tolist()
        )
    
    with col2:
        selected_kategoria = st.selectbox(
            "KategÃ³ria", 
            options=["Mind"] + st.session_state.kategoriak['nev'].tolist()
        )
    
    with col3:
        selected_megrendelo = st.selectbox(
            "MegrendelÅ‘", 
            options=["Mind"] + st.session_state.megrendelok['nev'].tolist()
        )
    
    datum_szures = st.date_input("DÃ¡tum szÅ±rÃ©s (opcionÃ¡lis)")
    
    # SzÅ±rÃ©s
    filtered_df = st.session_state.fuvarok.copy()
    
    if not filtered_df.empty:
        if selected_busz != "Mind":
            busz_id = get_id_by_name(st.session_state.buszok, selected_busz, 'rendszam')
            filtered_df = filtered_df[filtered_df['busz_id'] == busz_id]
        
        if selected_kategoria != "Mind":
            kategoria_id = get_id_by_name(st.session_state.kategoriak, selected_kategoria)
            filtered_df = filtered_df[filtered_df['kategoria_id'] == kategoria_id]
        
        if selected_megrendelo != "Mind":
            megrendelo_id = get_id_by_name(st.session_state.megrendelok, selected_megrendelo)
            filtered_df = filtered_df[filtered_df['megrendelo_id'] == megrendelo_id]
        
        if datum_szures:
            filtered_df = filtered_df[filtered_df['datum'] == datum_szures]
    
    # EredmÃ©nyek megjelenÃ­tÃ©se
    if not filtered_df.empty:
        display_df = filtered_df.copy()
        display_df['Busz'] = display_df['busz_id'].apply(lambda x: get_name_by_id(st.session_state.buszok, x, 'rendszam'))
        display_df['KategÃ³ria'] = display_df['kategoria_id'].apply(lambda x: get_name_by_id(st.session_state.kategoriak, x))
        display_df['MegrendelÅ‘'] = display_df['megrendelo_id'].apply(
            lambda x: get_name_by_id(st.session_state.megrendelok, x) if pd.notnull(x) else ""
        )
        
        st.subheader(f"TalÃ¡lt fuvarok: {len(display_df)}")
        st.dataframe(
            display_df[['Busz', 'KategÃ³ria', 'MegrendelÅ‘', 'datum', 'kezdes', 'vege', 'cel', 'megjegyzes']],
            use_container_width=True
        )
    else:
        st.warning("Nincs a szÅ±rÃ©si feltÃ©teleknek megfelelÅ‘ fuvar.")

# Admin panel
def admin():
    st.header("AdminisztrÃ¡ciÃ³")
    
    tab1, tab2, tab3 = st.tabs(["KategÃ³riÃ¡k", "GÃ©pjÃ¡rmÅ±vek", "MegrendelÅ‘k"])
    
    with tab1:
        st.subheader("Fuvar kategÃ³riÃ¡k")
        
        # MeglÃ©vÅ‘ kategÃ³riÃ¡k
        for idx, row in st.session_state.kategoriak.iterrows():
            with st.expander(f"{row['nev']}"):
                with st.form(f"kategoria_{row['id']}"):
                    new_name = st.text_input("NÃ©v", value=row['nev'])
                    new_color = st.color_picker("SzÃ­n", value=row['szin'])
                    
                    if st.form_submit_button("MentÃ©s"):
                        st.session_state.kategoriak.at[idx, 'nev'] = new_name
                        st.session_state.kategoriak.at[idx, 'szin'] = new_color
                        st.success("KategÃ³ria frissÃ­tve!")
                        st.experimental_rerun()
        
        # Ãšj kategÃ³ria
        with st.expander("Ãšj kategÃ³ria hozzÃ¡adÃ¡sa"):
            with st.form("uj_kategoria"):
                new_name = st.text_input("KategÃ³ria neve")
                new_color = st.color_picker("SzÃ­n", value="#FF0000")
                
                if st.form_submit_button("HozzÃ¡adÃ¡s"):
                    if new_name:
                        new_kategoria = pd.DataFrame([{
                            'id': str(uuid.uuid4()),
                            'nev': new_name,
                            'szin': new_color
                        }])
                        st.session_state.kategoriak = pd.concat(
                            [st.session_state.kategoriak, new_kategoria], 
                            ignore_index=True
                        )
                        st.success("KategÃ³ria hozzÃ¡adva!")
                        st.experimental_rerun()
                    else:
                        st.error("A kategÃ³ria neve kÃ¶telezÅ‘!")
    
    with tab2:
        st.subheader("GÃ©pjÃ¡rmÅ±vek")
        
        # MeglÃ©vÅ‘ buszok
        for idx, row in st.session_state.buszok.iterrows():
            with st.expander(f"{row['rendszam']} - {row['tipus']}"):
                with st.form(f"busz_{row['id']}"):
                    new_rendszam = st.text_input("RendszÃ¡m", value=row['rendszam'])
                    new_tipus = st.text_input("TÃ­pus", value=row['tipus'])
                    new_evjarat = st.number_input("Ã‰vjÃ¡rat", value=int(row['evjarat']), min_value=1990, max_value=2030)
                    new_ferohely = st.number_input("FÃ©rÅ‘hely", value=int(row['ferohely']), min_value=1, max_value=200)
                    
                    if st.form_submit_button("MentÃ©s"):
                        st.session_state.buszok.at[idx, 'rendszam'] = new_rendszam
                        st.session_state.buszok.at[idx, 'tipus'] = new_tipus
                        st.session_state.buszok.at[idx, 'evjarat'] = new_evjarat
                        st.session_state.buszok.at[idx, 'ferohely'] = new_ferohely
                        st.success("Busz adatai frissÃ­tve!")
                        st.experimental_rerun()
        
        # Ãšj busz
        with st.expander("Ãšj gÃ©pjÃ¡rmÅ± hozzÃ¡adÃ¡sa"):
            with st.form("uj_busz"):
                new_rendszam = st.text_input("RendszÃ¡m")
                new_tipus = st.text_input("TÃ­pus")
                new_evjarat = st.number_input("Ã‰vjÃ¡rat", min_value=1990, max_value=2030, value=2020)
                new_ferohely = st.number_input("FÃ©rÅ‘hely", min_value=1, max_value=200, value=50)
                
                if st.form_submit_button("HozzÃ¡adÃ¡s"):
                    if new_rendszam and new_tipus:
                        new_busz = pd.DataFrame([{
                            'id': str(uuid.uuid4()),
                            'rendszam': new_rendszam,
                            'tipus': new_tipus,
                            'evjarat': new_evjarat,
                            'ferohely': new_ferohely
                        }])
                        st.session_state.buszok = pd.concat(
                            [st.session_state.buszok, new_busz], 
                            ignore_index=True
                        )
                        st.success("Ãšj busz hozzÃ¡adva!")
                        st.experimental_rerun()
                    else:
                        st.error("A rendszÃ¡m Ã©s tÃ­pus megadÃ¡sa kÃ¶telezÅ‘!")
    
    with tab3:
        st.subheader("MegrendelÅ‘k")
        
        # MeglÃ©vÅ‘ megrendelÅ‘k
        for idx, row in st.session_state.megrendelok.iterrows():
            with st.expander(f"{row['nev']}"):
                with st.form(f"megrendelo_{row['id']}"):
                    new_name = st.text_input("NÃ©v", value=row['nev'])
                    new_contact = st.text_input("KapcsolattartÃ³", value=row['kapcsolattarto'])
                    new_phone = st.text_input("Telefon", value=row['telefon'])
                    new_email = st.text_input("E-mail", value=row['email'])
                    
                    if st.form_submit_button("MentÃ©s"):
                        st.session_state.megrendelok.at[idx, 'nev'] = new_name
                        st.session_state.megrendelok.at[idx, 'kapcsolattarto'] = new_contact
                        st.session_state.megrendelok.at[idx, 'telefon'] = new_phone
                        st.session_state.megrendelok.at[idx, 'email'] = new_email
                        st.success("MegrendelÅ‘ adatai frissÃ­tve!")
                        st.experimental_rerun()
        
        # Ãšj megrendelÅ‘
        with st.expander("Ãšj megrendelÅ‘ hozzÃ¡adÃ¡sa"):
            with st.form("uj_megrendelo"):
                new_name = st.text_input("NÃ©v")
                new_contact = st.text_input("KapcsolattartÃ³")
                new_phone = st.text_input("Telefon")
                new_email = st.text_input("E-mail")
                
                if st.form_submit_button("HozzÃ¡adÃ¡s"):
                    if new_name:
                        new_megrendelo = pd.DataFrame([{
                            'id': str(uuid.uuid4()),
                            'nev': new_name,
                            'kapcsolattarto': new_contact,
                            'telefon': new_phone,
                            'email': new_email
                        }])
                        st.session_state.megrendelok = pd.concat(
                            [st.session_state.megrendelok, new_megrendelo], 
                            ignore_index=True
                        )
                        st.success("Ãšj megrendelÅ‘ hozzÃ¡adva!")
                        st.experimental_rerun()
                    else:
                        st.error("A megrendelÅ‘ neve kÃ¶telezÅ‘!")

# FÅ‘menÃ¼ navigÃ¡ciÃ³
def main():
    st.sidebar.title("NavigÃ¡ciÃ³")
    menu = st.sidebar.radio(
        "VÃ¡lasszon menÃ¼pontot:",
        ["FÅ‘oldal", "Ãšj fuvar", "IdÅ‘vonal", "SzÅ±rÃ©s", "AdminisztrÃ¡ciÃ³"]
    )
    
    if menu == "FÅ‘oldal":
        fooldal()
    elif menu == "Ãšj fuvar":
        uj_fuvar()
    elif menu == "IdÅ‘vonal":
        idovonal()
    elif menu == "SzÅ±rÃ©s":
        szures()
    elif menu == "AdminisztrÃ¡ciÃ³":
        admin()

if __name__ == "__main__":
    main()