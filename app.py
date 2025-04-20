import streamlit as st
import pandas as pd

st.set_page_config(page_title="Earned Media Value Estimator", layout="centered")
st.title("💰 Earned Media Value Estimator")

media_type = st.selectbox("Select Media Type", ["Online", "Print", "Podcast"])

def calculate_emv_online(uvm, cpm, quality_multiplier):
    return (uvm / 1000) * cpm * quality_multiplier

def calculate_emv_print(circulation, ad_size_multiplier, prominence_multiplier, base_rate):
    return circulation * ad_size_multiplier * prominence_multiplier * base_rate / 1000

def calculate_emv_podcast(listeners, cpm, segment_quality_multiplier):
    return (listeners / 1000) * cpm * segment_quality_multiplier

data = {}

if media_type == "Online":
    uvm = st.number_input("Estimated Unique Monthly Visitors (UVM)", min_value=0)
    cpm = st.number_input("Industry CPM ($)", value=25.0)
    quality = st.selectbox("Coverage Quality", ["Mention", "Quote", "Feature"])
    quality_multiplier = {"Mention": 0.5, "Quote": 1.0, "Feature": 1.5}[quality]

    if st.button("Estimate EMV"):
        emv = calculate_emv_online(uvm, cpm, quality_multiplier)
        data = {
            "Type": "Online",
            "UVM": uvm,
            "CPM": cpm,
            "Quality": quality,
            "Estimated EMV ($)": round(emv, 2)
        }
        st.success(f"Estimated EMV: ${round(emv, 2)}")

elif media_type == "Print":
    circulation = st.number_input("Estimated Circulation", min_value=0)
    ad_size = st.selectbox("Ad Size", ["Mention", "Quarter Page", "Half Page", "Full Page"])
    prominence = st.selectbox("Prominence", ["Low", "Medium", "High"])
    base_rate = st.number_input("Base Print Rate (per 1K circ)", value=50.0)

    ad_size_multiplier = {"Mention": 0.3, "Quarter Page": 0.5, "Half Page": 0.75, "Full Page": 1.0}[ad_size]
    prominence_multiplier = {"Low": 0.75, "Medium": 1.0, "High": 1.25}[prominence]

    if st.button("Estimate EMV"):
        emv = calculate_emv_print(circulation, ad_size_multiplier, prominence_multiplier, base_rate)
        data = {
            "Type": "Print",
            "Circulation": circulation,
            "Ad Size": ad_size,
            "Prominence": prominence,
            "Estimated EMV ($)": round(emv, 2)
        }
        st.success(f"Estimated EMV: ${round(emv, 2)}")

elif media_type == "Podcast":
    listeners = st.number_input("Estimated Listeners", min_value=0)
    cpm = st.number_input("Industry CPM ($)", value=30.0)
    segment_type = st.selectbox("Segment Type", ["Brief Mention", "Mid-Roll Mention", "Dedicated Segment"])
    segment_quality_multiplier = {"Brief Mention": 0.5, "Mid-Roll Mention": 1.0, "Dedicated Segment": 1.5}[segment_type]

    if st.button("Estimate EMV"):
        emv = calculate_emv_podcast(listeners, cpm, segment_quality_multiplier)
        data = {
            "Type": "Podcast",
            "Listeners": listeners,
            "Segment": segment_type,
            "Estimated EMV ($)": round(emv, 2)
        }
        st.success(f"Estimated EMV: ${round(emv, 2)}")

# Show and export results
if data:
    df = pd.DataFrame([data])
    st.dataframe(df)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", data=csv, file_name="emv_estimate.csv")
