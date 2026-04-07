import streamlit as st
from predict import predict_sms


st.set_page_config(page_title="SMS Fraud Detector", page_icon="🔍")

# ===== ENHANCEMENTS ADDED HERE =====
st.markdown("""
<style>
.main {background-color: #f0f2f6;}
.stButton > button {background-color: #ff4b4b; color: white; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# Replace st.title line
st.markdown("# 🔍 *SMS Fraud Detector*")
st.markdown("---")
st.info("🏆 Trained on 5,500+ real SMS. Detects fraud signals instantly.")
# ===== END ENHANCEMENTS =====

message = st.text_area("SMS Message", height=150,
                        placeholder="Paste the full SMS here...")

if st.button("Analyse"):
    if message.strip():
        result = predict_sms(message)

        # ===== ENHANCEMENT ADDED HERE =====
        col1, col2 = st.columns([3,1])
        with col1:
            color = "red" if "SPAM" in result["verdict"] else "green"
            st.markdown(f"### *Verdict: :{color}[{result['verdict']}]*", 
                       unsafe_allow_html=True)
        with col2:
            st.metric("Confidence", result["confidence"])
        # ===== END ENHANCEMENT =====

        st.markdown("*Signals detected:*")
        for s in result["signals"]:
            st.markdown(f"- {s}")
    else:
        st.warning("Please paste a message first.")

st.set_page_config(page_title="SMS Fraud Detector", page_icon="🔍")
st.title("SMS Fraud Detector")
st.caption("Paste any SMS message below to check if it is fraudulent.")

message = st.text_area("SMS Message", height=150,
                        placeholder="Paste the full SMS here...")

if st.button("Analyse"):
    if message.strip():
        result = predict_sms(message)

        color = "red" if "SPAM" in result["verdict"] else "green"
        st.markdown(f"### Verdict: :{color}[{result['verdict']}]")
        st.metric("Confidence", result["confidence"])

        st.markdown("**Signals detected:**")
        for s in result["signals"]:
            st.markdown(f"- {s}")
    else:
        st.warning("Please paste a message first.")