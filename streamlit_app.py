import streamlit as st
import pandas as pd
import datetime
import uuid
import plotly.express as px

# Adatinicializálás
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

def get_color_from_id(df, id_value):
if not df.empty and id_value in df['id'].values:
return df[df['id'] == id_value]['szin'].values[0]
return '#FFFFFF'

# Idővonalas nézet
def show_timeline():
st.subheader("Idővonalas Gantt-diagram")

if st.session_state.fuvarok.empty:
st.warning("Nincs megjeleníthető fuvar")
return

# Adatok előkészítése
df = st.session_state.fuvarok.copy()

# Dátum-idő kombinációk létrehozása
df['Kezdés'] = pd.to_datetime(df['datum'].astype(str) + ' ' + df['kezdes'].astype(str))
df['Befejezés'] = pd.to_datetime(df['datum'].astype(str) + ' ' + df['vege'].astype(str))

# Adatok transzformációja
df['Busz'] = df['busz_id'].apply(lambda x: get_name_from_id(st.session_state.gepjarmuvek, x))
df['Kategória'] = df['kategoria_id'].apply(lambda x: get_name_from_id(st.session_state.fuvar_kategoriak, x))
df['Szín'] = df['kategoria_id'].apply(get_color_from_id, df=st.session_state.fuvar_kategoriak)
df['Megrendelő'] = df['megrendelo_id'].apply(
lambda x: get_name_from_id(st.session_state.megrendelok, x) if pd.notnull(x) else ""
)

# Plotly Gantt-diagram
fig = px.timeline(
df,
x_start="Kezdés",
x_end="Befejezés",
y="Busz",
color="Kategória",
color_discrete_map=dict(zip(
st.session_state.fuvar_kategoriak['nev'],
st.session_state.fuvar_kategoriak['szin']
)),
hover_name="cel",
hover_data={
"Megrendelő": True,
"Kezdés": "|%Y-%m-%d %H:%M",
"Befejezés": "|%Y-%m-%d %H:%M",
"Kategória": False,
"Busz": False
},
title="Fuvarok idővonala"
)

# Diagram testreszabása
fig.update_yaxes(autorange="reversed", title_text='Buszok')
fig.update_xaxes(title_text='Időszak')
fig.update_layout(
height=600,
showlegend=True,
hovermode="closest",
plot_bgcolor='rgba(240,240,240,0.9)'
)

# Diagram megjelenítése
st.plotly_chart(fig, use_container_width=True)

# Fő alkalmazás
st.title("🚌 Busz Fuvar Kezelő Rendszer")
menu = st.sidebar.selectbox("Menü", [
"Főoldal",
"Új fuvar",
"Idővonal",
"Szűrés",
"Adminisztráció"
])

# További függvények és menükezelés itt folytatódik...
# (Az előző válaszban szereplő add_fuvar, admin_panel, filter_fuvarok függvények maradnak változatlanok)

if menu == "Főoldal":
st.subheader("Statisztikák")
col1, col2, col3 = st.columns(3)
with col1:
st.metric("Regisztrált buszok", len(st.session_state.gepjarmuvek))
with col2:
st.metric("Megrendelők", len(st.session_state.megrendelok))
with col3:
st.metric("Fuvarok", len(st.session_state.fuvarok))
elif menu == "Idővonal":
show_timeline()
elif menu == "Adminisztráció":
# Admin panel implementációja
pass
elif menu == "Új fuvar":
# Új fuvar hozzáadása
pass
elif menu == "Szűrés":
# Szűrési funkciók
pass