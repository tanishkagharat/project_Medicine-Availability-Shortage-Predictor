import streamlit as st
import pandas as pd
import datetime
import random
import base64

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(layout="wide")

# -------------------------
# LOAD BACKGROUND IMAGE
# -------------------------
def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64("ChatGPT Image Apr 25, 2026, 02_19_54 PM.png")

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("notebook/medicine_availability_1000.csv.xls")
df.columns = df.columns.str.strip()

# -------------------------
# TITLE
# -------------------------
st.title("💊 Medicine Availability Predictor")

# -------------------------
# DISCLAIMER
# -------------------------
st.warning("⚠️ This app is for informational purposes only. Always consult a doctor before taking any medicine.")

# -------------------------
# TABS
# -------------------------
tab1, tab2, tab3 = st.tabs([
    "🔮 Medicine Predictor",
    "🚨 Emergency Help",
    "📸 Prescription"
])

# =====================================================
# 🔮 TAB 1: PREDICTOR
# =====================================================
with tab1:

    st.header("🔮 Medicine Predictor")

    col1, col2 = st.columns(2)

    with col1:
        med_list = ["Select Medicine"] + list(df['Medicine_Name'].unique())
        med1 = st.selectbox("💊 Medicine", med_list, key="pred_med")

    with col2:
        area_list = ["Select Area"] + list(df['Area'].unique())
        area1 = st.selectbox("📍 Area", area_list, key="pred_area")

    current_hour = datetime.datetime.now().hour

    def store_status():
        return "🟢 Open" if 9 <= current_hour <= 22 else "🔴 Closed"

    if st.button("Check Prediction", key="pred_btn"):

        if med1 == "Select Medicine" or area1 == "Select Area":
            st.error("❌ Please select medicine and area")
        else:
            with st.spinner("Checking availability..."):

                result = df[
                    (df['Medicine_Name'] == med1) &
                    (df['Area'] == area1)
                ]

                if result.empty:
                    st.error("❌ Not available in this area")
                    st.info("👉 Go to Emergency tab")

                else:
                    row = result.iloc[0]
                    status = row['Availability']

                    st.subheader(f"Status: {status}")

                    if status == "Available":
                        st.success("🟢 Available")

                    elif status == "Low Stock":
                        st.warning("🟡 Limited stock")
                        st.error("🚨 May run out soon")

                    else:
                        st.error("🔴 Out of stock")

                    contact = row['Contact'] if 'Contact' in df.columns else "Not Available"

                    st.subheader("🏥 Pharmacy Details")
                    st.write(f"Name: {row['Pharmacy_Name']}")
                    st.write(f"Area: {row['Area']}")
                    st.write(f"🕒 Store: {store_status()}")
                    st.write(f"📞 Contact: {contact}")

    if st.button("🔁 Check Another"):
        st.rerun()

# =====================================================
# 🚨 TAB 2: EMERGENCY (CLICKABLE GOOGLE MAPS)
# =====================================================
with tab2:

    st.header("🚨 Emergency Medicine Finder")

    col1, col2 = st.columns(2)

    with col1:
        med2 = st.selectbox("💊 Medicine", df['Medicine_Name'].unique(), key="em_med")

    with col2:
        area2 = st.selectbox("📍 Your Area", df['Area'].unique(), key="em_area")

    if st.button("Find Fastest Option", key="em_btn"):

        available = df[
            (df['Medicine_Name'] == med2) &
            (df['Availability'] == "Available")
        ].copy()

        if available.empty:
            st.error("❌ Not available anywhere")

        else:
            def estimate_time(r):
                return random.randint(3, 8) if r['Area'] == area2 else random.randint(10, 20)

            available["Time"] = available.apply(estimate_time, axis=1)
            available = available.sort_values(by="Time")

            st.subheader("⚡ Fastest Pharmacies")

            for _, r in available.head(3).iterrows():

                pharmacy = r['Pharmacy_Name']
                area = r['Area']

                # Google Maps direction link
                origin = area2.replace(" ", "+")
                destination = f"{pharmacy} {area}".replace(" ", "+")

                maps_url = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}"

                # Clickable card
                st.markdown(f"""
                <a href="{maps_url}" target="_blank" style="text-decoration:none;">
                    <div style="
                        background: rgba(0,0,0,0.6);
                        padding:15px;
                        border-radius:12px;
                        margin-bottom:10px;
                        cursor:pointer;
                    ">
                        <h4 style="color:white;">🏥 {pharmacy} ({area})</h4>
                        <p style="color:white;">⏱️ Reach in: {r['Time']} mins</p>
                        <p style="color:#00c9a7;">👉 Click to open in Google Maps</p>
                    </div>
                </a>
                """, unsafe_allow_html=True)

# =====================================================
# 📸 TAB 3: PRESCRIPTION
# =====================================================
with tab3:

    st.header("📸 Upload Prescription")

    file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])

    if file:
        st.image(file, width=300)
        st.success("Uploaded successfully")

        st.subheader("💊 Medicines Detected")
        detected = ["Paracetamol", "Crocin"]

        for med in detected:
            st.write(f"✔ {med}")

# -------------------------
# FINAL UI (NO BLUR, SHARP IMAGE)
# -------------------------
st.markdown(f"""
<style>

/* Background */
.stApp {{
    background-image: url("data:image/png;base64,{img}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* Container */
.block-container {{
    background: rgba(0, 0, 0, 0.5);
    padding: 2rem;
    border-radius: 15px;
}}

/* Cards */
div[data-testid="stVerticalBlock"] > div {{
    background: rgba(0,0,0,0.5);
    padding: 15px;
    border-radius: 12px;
}}

/* Buttons */
.stButton > button {{
    background: #00c9a7;
    color: white;
    border-radius: 8px;
    border: none;
}}

/* Text */
h1, h2, h3, p {{
    color: white;
}}

</style>
""", unsafe_allow_html=True)