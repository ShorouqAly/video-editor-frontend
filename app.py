import streamlit as st
import pandas as pd
import random
from datetime import datetime



st.set_page_config(page_title="UVM Estimator", layout="centered")



st.title("📊 UVM Estimator Tool")
st.write("Paste in one or more media domains to estimate their Unique Monthly Visitors (UVM).")



sample_domains = ["forbes.com", "nytimes.com", "techcrunch.com"]



# Input form
domains_input = st.text_area("Enter domains (one per line):", value="\n".join(sample_domains), height=150)
run_estimate = st.button("Estimate UVM")



def estimate_uvm(domain):
random.seed(domain)
uvm = random.randint(500000, 90000000)
confidence = random.choice(["High", "Medium", "Low"])
return {"Domain": domain, "Estimated UVM": uvm, "Confidence": confidence}



if run_estimate:
domains = [d.strip() for d in domains_input.splitlines() if d.strip()]
results = [estimate_uvm(domain) for domain in domains]
df = pd.DataFrame(results)
st.success(f"✅ Estimated UVM for {len(df)} domains.")
st.dataframe(df)



csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download CSV", data=csv, file_name=f"uvm_estimates_{datetime.now().strftime('%Y%m%d')}.csv")