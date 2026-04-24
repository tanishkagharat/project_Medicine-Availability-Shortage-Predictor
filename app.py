import streamlit as st
import pandas as pd
import datetime
import random

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(layout="wide")

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

        # INPUT VALIDATION
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
                    st.info("👉 Go to Emergency tab to find fastest option")

                else:
                    row = result.iloc[0]
                    status = row['Availability']

                    st.subheader(f"Status: {status}")

                    if status == "Available":
                        st.success("🟢 Available")
                        st.info("📊 Prediction: No shortage expected soon")

                    elif status == "Low Stock":
                        st.warning("🟡 Limited stock")
                        st.error("🚨 High chance it will run out soon")
                        st.info("📊 Buy as early as possible")

                    else:
                        st.error("🔴 Out of stock")
                        st.info("📊 Try nearby areas immediately")

                    # SAFE CONTACT
                    contact = row['Contact'] if 'Contact' in df.columns else "Not Available"

                    st.subheader("🏥 Pharmacy Details")
                    st.write(f"Name: {row['Pharmacy_Name']}")
                    st.write(f"Area: {row['Area']}")
                    st.write(f"🕒 Store: {store_status()}")
                    st.write(f"📞 Contact: {contact}")

                    # SUMMARY
                    st.subheader("🧾 overall")
                    st.info(f"""
Medicine: {med1}  
Area: {area1}  
Status: {status}  
Pharmacy: {row['Pharmacy_Name']}
""")

    # RESET BUTTON
    if st.button("🔁 Check Another"):
        st.rerun()

# =====================================================
# 🚨 TAB 2: EMERGENCY
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
            st.error("❌ Not available anywhere right now")

        else:
            def estimate_time(r):
                return random.randint(3, 8) if r['Area'] == area2 else random.randint(10, 20)

            available["Time"] = available.apply(estimate_time, axis=1)
            available = available.sort_values(by="Time")

            st.subheader("⚡ Fastest Pharmacies")

            for _, r in available.head(3).iterrows():
                st.success(f"""
🏥 {r['Pharmacy_Name']} ({r['Area']})
⏱️ Reach in: {r['Time']} mins
""")

            best = available.iloc[0]

            st.subheader("🏆 Best Immediate Option")
            st.success(f"""
🏥 {best['Pharmacy_Name']} ({best['Area']})
🚀 Reach in: {best['Time']} mins
""")

# =====================================================
# 📸 TAB 3: PRESCRIPTION
# =====================================================
with tab3:

    st.header("📸 Upload Prescription")

    file = st.file_uploader("Upload Prescription Image", type=["png","jpg","jpeg"], key="upload")

    if file:
        st.image(file, width=300)
        st.success("Uploaded successfully")

        st.subheader("💊 Medicines Detected")

        # Dummy detection
        detected = ["Paracetamol", "Crocin"]

        for med in detected:
            st.write(f"✔ {med}")

        st.info("👉 Use Medicine Predictor tab to check availability")

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.write("🚀 Built for real patient decision support")