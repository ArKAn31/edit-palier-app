import json
import streamlit as st

PALIERS_FILE = "paliers.json"

def charger_paliers():
    try:
        with open(PALIERS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def sauvegarder_paliers(paliers):
    with open(PALIERS_FILE, "w") as f:
        json.dump(paliers, f, indent=2, ensure_ascii=False)

paliers = charger_paliers()
cryptos = list(paliers.keys())

st.title("Gestion des paliers crypto (achat/vente)")

# Sélection de la crypto
crypto = st.selectbox("Sélectionne une crypto", cryptos)

# Liste achat/vente à modifier
col1, col2 = st.columns(2)
with col1:
    st.subheader("Paliers d'achat")
    achats = st.text_area("Liste (1 palier/ligne, format : prix $ - commentaire)",
        value="\n".join(paliers[crypto]['achat']), height=150, key="achat")
with col2:
    st.subheader("Paliers de vente")
    ventes = st.text_area("Liste (1 palier/ligne, format : prix $ - commentaire)",
        value="\n".join(paliers[crypto]['vente']), height=150, key="vente")

if st.button("Enregistrer les changements"):
    paliers[crypto]['achat'] = [a.strip() for a in achats.split("\n") if a.strip()]
    paliers[crypto]['vente'] = [v.strip() for v in ventes.split("\n") if v.strip()]
    sauvegarder_paliers(paliers)
    st.success("✅ Modifications enregistrées !")
