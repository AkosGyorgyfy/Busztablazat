import streamlit as st
import pandas as pd
import datetime
from datetime import timedelta
import uuid

# Adatstruktúrák inicializálása
if 'megrendelok' not in st.session_state:
st.session_state.megrendelok = pd.DataFrame(columns=['id', 'nev', 'kapcsolattarto', 'telefon', 'email'])
if 'gepjarmuvek' not in st.session_state:
st.session_state.gepjarmuvek = pd.DataFrame(columns=['id', 'rendszam', 'tipus', 'evjarat', 'ferohely'])
if 'fuvar_kategoriak' not in st.session_state:
st.session_state.fuvar_kategoriak = pd.DataFrame(columns=['id', 'nev', 'szin'])
if 'fuvarok' not in st.session_state:
st.session_state.fuvarok = pd.DataFrame(columns=['id', 'busz_id', 'kategoria_id', 'megrendelo_id', 'datum', 'kezdes', 'vege', 'cel', 'megjegyzes'])

# Alapértelmezett adatok
if st.session_state.fuvar_kategoriak.empty:
kategoria_adatok = [
{'id': str(uuid.uuid4()), 'nev': 'Normál fuvar', 'szin': '#FFD700'},
{'id': str(uuid.uuid4()), 'nev': 'Speciális fuvar', 'szin': '#9932CC'},
{'id': str(uuid.uuid4()), 'nev': 'Karbantartás', 'szin': '#4169E1'},
{'id': str(uuid.uuid4()), 'nev': 'Szerviz', 'szin': '#FF8C00'},
{'id': str(uuid.uuid4()), 'nev': 'Pihenőnap', 'szin': '#808080'}
]
st.session_state.fuvar_kategoriak = pd.DataFrame(kategoria_adatok)

if st.session_state.gepjarmuvek.empty:
gepjarmu_adatok = [
{'id': str(uuid.uuid4()), 'rendszam': 'ABC-123', 'tipus': 'Mercedes', 'evjarat': 2019, 'ferohely': 50},
{'id': str(uuid.uuid4()), 'rendszam': 'DEF-456', 'tipus': 'Volvo', 'evjarat': 2020, 'ferohely': 60}
]
st.session_state.gepjarmuvek = pd.DataFrame(gepjarmu_adatok)

if st.session_state.megrendelok.empty:
megrendelo_adatok = [
{'id': str(uuid.uuid4()), 'nev': 'Budapest Közlekedési Zrt.', 'kapcsolattarto': 'Kovács János', 'telefon': '+3611234567', 'email': 'kovacs@bkv.hu'},
{'id': str(uuid.uuid4()), 'nev': 'Volánbusz', 'kapcsolattarto': 'Nagy Erzsébet', 'telefon': '+3619876543', 'email': 'nagy@volanbusz.hu'}
]
st.session_state.megrendelok = pd.DataFrame(megrendelo_adatok)

# Függvények
def uj_fuvar_hozzaadasa():
busz_id = st.selectbox('Busz', st.session_state.gepjarmuvek['rendszam'])
kategoria_id = st.selectbox('Kategória', st.session_state.fuvar_kategoriak['nev'])
megrendelo_id = st.selectbox('Megrendelő', st.session_state.megrendelok['nev'])
datum = st.date_input('Dátum', value=datetime.date.today())
kezdes = st.time_input('Kezdés')
vege = st.time_input('Vége')
cel = st.text_input('Cél')
megjegyzes = st.text_area('Megjegyzés')
if st.button('Fuvar hozzáadása'):
busz_id = st.session_state.gepjarmuvek[st.session_state.gepjarmuvek['rendszam'] == busz_id]['id'].values[0]
kategoria_id = st.session_state.fuvar_kategoriak[st.session_state.fuvar_kategoriak['nev'] == kategoria_id]['id'].values[0]
megrendelo_id = st.session_state.megrendelok[st.session_state.megrendelok['nev'] == megrendelo_id]['id'].values[0]
fuvar = {
'id': str(uuid.uuid4()),
'busz_id': busz_id,
'kategoria_id': kategoria_id,
'megrendelo_id': megrendelo_id,
'datum': datum,
'kezdes': kezdes,
'vege': vege,
'cel': cel,
'megjegyzes': megjegyzes
}
st.session_state.fuvarok = st.session_state.fuvarok.append(fuvar, ignore_index=True)
st.success('Fuvar sikeresen hozzáadva!')

def admin_panel():
st.subheader('Adminisztráció')
tab1, tab2, tab3 = st.tabs(['Kategóriák', 'Gépjárművek', 'Megrendelők'])
with tab1:
st.subheader('Fuvar kategóriák')
for idx, row in st.session_state.fuvar_kategoriak.iterrows():
with st.expander(f"{row['nev']} (Szin: {row['szin']})"):
nev = st.text_input('Név', value=row['nev'], key=f"kategorianev_{idx}")
szin = st.text_input('Szín', value=row['szin'], key=f"kategoriaszin_{idx}")
if st.button('Mentés', key=f"kategoriasave_{idx}"):
st.session_state.fuvar_kategoriak.at[idx, 'nev'] = nev
st.session_state.fuvar_kategoriak.at[idx, 'szin'] = szin
st.success('Kategória frissítve!')
if st.button('Új kategória hozzáadása'):
nev = st.text_input('Új kategória neve', key='uj_kategoria_nev')
szin = st.text_input('Színkód', key='uj_kategoria_szin')
if nev and szin:
st.session_state.fuvar_kategoriak = st.session_state.fuvar_kategoriak.append({
'id': str(uuid.uuid4()),
'nev': nev,
'szin': szin
}, ignore_index=True)
st.success('Kategória hozzáadva!')
with tab2:
st.subheader('Gépjárművek')
for idx, row in st.session_state.gepjarmuvek.iterrows():
with st.expander(f"{row['rendszam']}"):
rendszam = st.text_input('Rendszám', value=row['rendszam'], key=f"rendszam_{idx}")
tipus = st.text_input('Típus', value=row['tipus'], key=f"tipus_{idx}")
evjarat = st.number_input('Évjárat', value=row['evjarat'], key=f"evjarat_{idx}")
ferohely = st.number_input('Férőhely', value=row['ferohely'], key=f"ferohely_{idx}")
if st.button('Mentés', key=f"gepjarmu_save_{idx}"):
st.session_state.gepjarmuvek.at[idx, 'rendszam'] = rendszam
st.session_state.gepjarmuvek.at[idx, 'tipus'] = tipus
st.session_state.gepjarmuvek.at[idx, 'evjarat'] = evjarat
st.session_state.gepjarmuvek.at[idx, 'ferohely'] = ferohely
st.success('Gépjármű frissítve!')
if st.button('Új gépjármű hozzáadása'):
rendszam = st.text_input('Rendszám', key='uj_rendszam')
tipus = st.text_input('Típus', key='uj_tipus')
evjarat = st.number_input('Évjárat', key='uj_evjarat')
ferohely = st.number_input('Férőhely', key='uj_ferohely')
if rendszam:
st.session_state.gepjarmuvek = st.session_state.gepjarmuvek.append({
'id': str(uuid.uuid4()),
'rendszam': rendszam,
'tipus': tipus,
'evjarat': evjarat,
'ferohely': ferohely
}, ignore_index=True)
st.success('Gépjármű hozzáadva!')
with tab3:
st.subheader('Megrendelők')
for idx, row in st.session_state.megrendelok.iterrows():
with st.expander(f"{row['nev']}"):
nev = st.text_input('Megrendelő', value=row['nev'], key=f"megrendelo_nev_{idx}")
kapcsolattarto = st.text_input('Kapcsolattartó', value=row['kapcsolattarto'], key=f"kapcsolattarto_{idx}")
telefon = st.text_input('Telefon', value=row['telefon'], key=f"telefon_{idx}")
email = st.text_input('E-mail', value=row['email'], key=f"email_{idx}")
if st.button('Mentés', key=f"megrendelo_save_{idx}"):
st.session_state.megrendelok.at[idx, 'nev'] = nev
st.session_state.megrendelok.at[idx, 'kapcsolattarto'] = kapcsolattarto
st.session_state.megrendelok.at[idx, 'telefon'] = telefon
st.session_state.megrendelok.at[idx, 'email'] = email
st.success('Megrendelő frissítve!')
if st.button('Új megrendelő hozzáadása'):
nev = st.text_input('Megrendelő', key='uj_megrendelo_nev')
kapcsolattarto = st.text_input('Kapcsolattartó', key='uj_kapcsolattarto')
telefon = st.text_input('Telefon', key='uj_telefon')
email = st.text_input('E-mail', key='uj_email')
if nev:
st.session_state.megrendelok = st.session_state.megrendelok.append({
'id': str(uuid.uuid4()),
'nev': nev,
'kapcsolattarto': kapcsolattarto,
'telefon': telefon,
'email': email
}, ignore_index=True)
st.success('Megrendelő hozzáadva!')

def fuvarok_listazasa():
st.subheader('Fuvarok listája')
df = st.session_state.fuvarok.copy()
if not df.empty:
# ID-k helyett nevek beillesztése
df['busz_id'] = df['busz_id'].map(lambda x: st.session_state.gepjarmuvek[st.session_state.gepjarmuvek['id']==x]['rendszam'].values[0] if not st.session_state.gepjarmuvek[st.session_state.gepjarmuvek['id']==x].empty else 'Ismeretlen')
df['kategoria_id'] = df['kategoria_id'].map(lambda x: st.session_state.fuvar_kategoriak[st.session_state.fuvar_kategoriak['id']==x]['nev'].values[0] if not st.session_state.fuvar_kategoriak[st.session_state.fuvar_kategoriak['id']==x].empty else 'Ismeretlen')
df['megrendelo_id'] = df['megrendelo_id'].map(lambda x: st.session_state.megrendelok[st.session_state.megrendelok['id']==x]['nev'].values[0] if not st.session_state.megrendelok[st.session_state.megrendelok['id']==x].empty else 'Ismeretlen')
st.dataframe(df[['busz_id', 'kategoria_id', 'megrendelo_id', 'datum', 'kezdes', 'vege', 'cel', 'megjegyzes']])
else:
st.write('Még nincsenek fuvarok rögzítve.')

def fuvar_szures():
st.subheader('Fuvar szűrése')
busz = st.selectbox('Busz', ['Mind'] + st.session_state.gepjarmuvek['rendszam'].tolist())
kategoria = st.selectbox('Kategória', ['Mind'] + st.session_state.fuvar_kategoriak['nev'].tolist())
megrendelo = st.selectbox('Megrendelő', ['Mind'] + st.session_state.megrendelok['nev'].tolist())
datum = st.date_input('Dátum', value=None)
df = st.session_state.fuvarok.copy()
if not df.empty:
df['busz_id'] = df['busz_id'].map(lambda x: st.session_state.gepjarmuvek[st.session_state.gepjarmuvek['id']==x]['rendszam'].values[0] if not st.session_state.gepjarmuvek[st.session_state.gepjarmuvek['id']==x].empty else 'Ismeretlen')
df['kategoria_id'] = df['kategoria_id'].map(lambda x: st.session_state.fuvar_kategoriak[st.session_state.fuvar_kategoriak['id']==x]['nev'].values[0] if not st.session_state.fuvar_kategoriak[st.session_state.fuvar_kategoriak['id']==x].empty else 'Ismeretlen')
df['megrendelo_id'] = df['megrendelo_id'].map(lambda x: st.session_state.megrendelok[st.session_state.megrendelok['id']==x]['nev'].values[0] if not st.session_state.megrendelok[st.session_state.megrendelok['id']==x].empty else 'Ismeretlen')
if busz != 'Mind':
df = df[df['busz_id'] == busz]
if kategoria != 'Mind':
df = df[df['kategoria_id'] == kategoria]
if megrendelo != 'Mind':
df = df[df['megrendelo_id'] == megrendelo]
if datum:
df = df[df['datum'] == datum]
st.dataframe(df[['busz_id', 'kategoria_id', 'megrendelo_id', 'datum', 'kezdes', 'vege', 'cel', 'megjegyzes']])
else:
st.write('Még nincsenek fuvarok rögzítve.')

# Főmenü
st.title('Busz Fuvar Kezelő')
menu = st.sidebar.radio('Menü', ['Főoldal', 'Fuvar hozzáadása', 'Adminisztráció', 'Fuvarok listája', 'Fuvar szűrése'])

if menu == 'Főoldal':
st.write('Üdvözöljük a Busz Fuvar Kezelő alkalmazásban!')
elif menu == 'Fuvar hozzáadása':
uj_fuvar_hozzaadasa()
elif menu == 'Adminisztráció':
admin_panel()
elif menu == 'Fuvarok listája':
fuvarok_listazasa()
elif menu == 'Fuvar szűrése':
fuvar_szures()