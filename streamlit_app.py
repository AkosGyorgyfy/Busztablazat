import streamlit as st
import pandas as pd
import datetime
import uuid
import numpy as np

# Adatstruktúrák inicializálása
def init_data():
if 'megrendelok' not in st.session_state:
st.session_state.megrendelok = pd.DataFrame(columns=['id', 'nev', 'kapcsolattarto', 'telefon', 'email'])

if 'gepjarmuvek' not in st.session_state:
st.session_state.gepjarmuvek = pd.DataFrame(columns=['id', 'rendszam', 'tipus', 'evjarat', 'ferohely'])

if 'fuvar_kategoriak' not in st.session_state:
default_kategoriak = [
{'id': str(uuid.uuid4()), 'nev': 'Normál fuvar', 'szin': '#FFD700'},
{'id': str(uuid.uuid4()), 'nev': 'Speciális fuvar', 'szin': '#9932CC'},
{'id': str(uuid.uuid4()), 'nev': 'Karbantartás', 'szin': '#4169E1'},
{'id': str(uuid.uuid4()), 'nev': 'Szerviz', 'szin': '#FF8C00'},
{'id': str(uuid.uuid4()), 'nev': 'Pihenőnap', 'szin': '#808080'}
]
st.session_state.fuvar_kategoriak = pd.DataFrame(default_kategoriak)

if 'fuvarok' not in st.session_state:
st.session_state.fuvarok = pd.DataFrame(columns=[
'id', 'busz_id', 'kategoria_id', 'megrendelo_id',
'datum', 'kezdes', 'vege', 'cel', 'megjegyzes'
])

init_data()

# Segédfüggvények
def get_name_from_id(df, id_value, column='id', name_column='nev'):
if not df.empty and id_value in df[column].values:
return df[df[column] == id_value][name_column].values[0]
return 'Ismeretlen'

def format_time(time_obj):
if pd.isnull(time_obj):
return ''
if isinstance(time_obj, str):
return time_obj
return time_obj.strftime('%H:%M')

# Fő oldalfunkciók
def main_page():
st.subheader("Statisztikák")
col1, col2, col3 = st.columns(3)
with col1:
st.metric("Regisztrált buszok", len(st.session_state.gepjarmuvek))
with col2:
st.metric("Megrendelők", len(st.session_state.megrendelok))
with col3:
st.metric("Fuvarok", len(st.session_state.fuvarok))

def add_fuvar():
with st.form("Új fuvar", clear_on_submit=True):
busz_rendszam = st.selectbox("Busz", options=st.session_state.gepjarmuvek['rendszam'])
kategoria_nev = st.selectbox("Kategória", options=st.session_state.fuvar_kategoriak['nev'])
megrendelo_nev = st.selectbox("Megrendelő", options=[''] + st.session_state.megrendelok['nev'].tolist())
datum = st.date_input("Dátum", value=datetime.date.today())
col1, col2 = st.columns(2)
with col1:
kezdes = st.time_input("Kezdés időpontja")
with col2:
vege = st.time_input("Befejezés időpontja")
cel = st.text_input("Cél")
megjegyzes = st.text_area("Megjegyzés")

if st.form_submit_button("Mentés"):
busz_id = st.session_state.gepjarmuvek[
st.session_state.gepjarmuvek['rendszam'] == busz_rendszam]['id'].values[0]
kategoria_id = st.session_state.fuvar_kategoriak[
st.session_state.fuvar_kategoriak['nev'] == kategoria_nev]['id'].values[0]
megrendelo_id = st.session_state.megrendelok[
st.session_state.megrendelok['nev'] == megrendelo_nev]['id'].values[0] if megrendelo_nev else None

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
st.success("Fuvar sikeresen hozzáadva!")

def admin_panel():
tab1, tab2, tab3 = st.tabs(["Kategóriák", "Gépjárművek", "Megrendelők"])

with tab1:
st.subheader("Fuvar kategóriák kezelése")
for idx, row in st.session_state.fuvar_kategoriak.iterrows():
with st.expander(f"{row['nev']}"):
with st.form(f"kategoria_{row['id']}"):
new_name = st.text_input("Név", value=row['nev'], key=f"name_{row['id']}")
new_color = st.color_picker("Szín", value=row['szin'], key=f"color_{row['id']}")
if st.form_submit_button("Mentés"):
st.session_state.fuvar_kategoriak.at[idx, 'nev'] = new_name
st.session_state.fuvar_kategoriak.at[idx, 'szin'] = new_color
st.experimental_rerun()

with st.expander("Új kategória", expanded=False):
with st.form("Új kategória"):
new_cat_name = st.text_input("Kategória neve")
new_cat_color = st.color_picker("Szín")
if st.form_submit_button("Hozzáadás"):
new_category = pd.DataFrame([{
'id': str(uuid.uuid4()),
'nev': new_cat_name,
'szin': new_cat_color
}])
st.session_state.fuvar_kategoriak = pd.concat(
[st.session_state.fuvar_kategoriak, new_category],
ignore_index=True
)
st.experimental_rerun()

with tab2:
st.subheader("Gépjárművek kezelése")
for idx, row in st.session_state.gepjarmuvek.iterrows():
with st.expander(f"{row['rendszam']}"):
with st.form(f"gepjarmu_{row['id']}"):
new_rendszam = st.text_input("Rendszám", value=row['rendszam'])
new_tipus = st.text_input("Típus", value=row['tipus'])
new_evjarat = st.number_input("Évjárat", value=row['evjarat'])
new_ferohely = st.number_input("Férőhely", value=row['ferohely'])
if st.form_submit_button("Mentés"):
st.session_state.gepjarmuvek.at[idx, 'rendszam'] = new_rendszam
st.session_state.gepjarmuvek.at[idx, 'tipus'] = new_tipus
st.session_state.gepjarmuvek.at[idx, 'evjarat'] = new_evjarat
st.session_state.gepjarmuvek.at[idx, 'ferohely'] = new_ferohely
st.experimental_rerun()

with st.expander("Új gépjármű", expanded=False):
with st.form("Új gépjármű"):
new_rendszam = st.text_input("Rendszám")
new_tipus = st.text_input("Típus")
new_evjarat = st.number_input("Évjárat", min_value=1990, max_value=datetime.date.today().year)
new_ferohely = st.number_input("Férőhely", min_value=1)
if st.form_submit_button("Hozzáadás"):
new_vehicle = pd.DataFrame([{
