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

st.markdown("<h1 style='color:#3498db;'>🚦 Gestion des paliers crypto</h1>", unsafe_allow_html=True)
st.write("Modifie, ajoute ou supprime des paliers d'achat ou de vente pour chaque crypto facilement.")

if not cryptos:
    st.error("Aucune crypto trouvée dans paliers.json ! Ajoute au moins un crypto pour commencer.")
    st.stop()

# ---- Choix de la crypto
crypto = st.selectbox("Sélectionne une crypto à modifier :", cryptos)

st.markdown("---")

# ---- Edition des paliers
col1, col2 = st.columns(2)
with col1:
    st.subheader("Paliers d'**achat**")
    achats = st.text_area("1 palier par ligne (ex: 42000 $ - support)", 
        value="\n".join(paliers[crypto]['achat']), height=150, key="achat")
with col2:
    st.subheader("Paliers de **vente**")
    ventes = st.text_area("1 palier par ligne (ex: 69000 $ - prise de profit)",
        value="\n".join(paliers[crypto]['vente']), height=150, key="vente")

st.markdown(" ")

if st.button("💾 Enregistrer les changements", help="Sauvegarder dans paliers.json"):
    paliers[crypto]['achat'] = [a.strip() for a in achats.split("\n") if a.strip()]
    paliers[crypto]['vente'] = [v.strip() for v in ventes.split("\n") if v.strip()]
    sauvegarder_paliers(paliers)
    st.success("✅ Modifications enregistrées dans paliers.json !")

st.markdown("---")

# ---- Affichage & copier/coller du JSON
st.markdown("### 👀 Voir / Copier le contenu actuel de paliers.json")
if st.button("Afficher le JSON complet"):
    with open(PALIERS_FILE, "r") as f:
        contenu = f.read()
    st.code(contenu, language="json")
    st.info("👉 Sélectionne tout le texte ci-dessus avec ta souris puis fais **CTRL+C** pour copier !")

# ---- Téléchargement du fichier
with open(PALIERS_FILE, "rb") as f:
    st.download_button(
        label="⬇️ Télécharger paliers.json",
        data=f,
        file_name="paliers.json",
        mime="application/json"
    )

st.markdown("---")
st.markdown(
    """
    <div style='background:#F8F8F8; padding:10px; border-radius:10px; border:1px solid #eee;'>
    ⚡️ <b>Astuce</b> : <br>
    - Tu peux ajouter autant de paliers que tu veux, un par ligne.<br>
    - Après modification, <b>n'oublie pas d'utiliser ce fichier dans ton bot et de redeployer !</b><br>
    </div>
    """, unsafe_allow_html=True)
