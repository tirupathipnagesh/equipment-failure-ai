import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000/api/v1"

st.set_page_config(
    page_title="Equipment Failure Prediction Platform",
    layout="wide"
)

st.title("Equipment Failure Prediction Platform")
st.caption("Predictive Maintenance Intelligence System")

# Sidebar machine input
st.sidebar.header("Machine Input")

machine_type = st.sidebar.selectbox("Machine Type", ["H", "M", "L"])
air_temp = st.sidebar.number_input("Air Temperature (K)", value=300.5)
process_temp = st.sidebar.number_input("Process Temperature (K)", value=309.8)
rot_speed = st.sidebar.number_input("Rotational Speed (rpm)", value=1345)
torque = st.sidebar.number_input("Torque (Nm)", value=62.7)
tool_wear = st.sidebar.number_input("Tool Wear (min)", value=153)

machine_data = {
    "Type": machine_type,
    "Air_temperature_K": air_temp,
    "Process_temperature_K": process_temp,
    "Rotational_speed_rpm": rot_speed,
    "Torque_Nm": torque,
    "Tool_wear_min": tool_wear
}

# Health status
st.subheader("System Status")

try:
    health = requests.get(f"{API_BASE}/health").json()
    st.success(f"Backend Status: {health['status']}")
except:
    st.error("Backend not reachable")

st.divider()

# Prediction section
st.header("Failure Prediction")

if st.button("Predict Failure Risk"):

    response = requests.post(
        f"{API_BASE}/predict/failure",
        json=machine_data
    )

    if response.status_code == 200:
        result = response.json()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Failure Probability",
                f"{result['failure_probability']*100:.2f}%"
            )

        with col2:
            pred = "Risk Detected" if result["failure_prediction"] == 1 else "Low Risk"
            st.metric("Prediction", pred)

        with col3:
            st.metric("Alert Level", result["alert_level"])

        st.subheader("Explanation")
        st.write(result["explanation"])

        st.subheader("Recommendation")
        st.info(result["recommendation"])

        st.subheader("Top Influencing Factors")
        st.write(result["top_features"])

    else:
        st.error("Prediction failed")

st.divider()

# Chatbot section
st.header("Machine Assistant")

question = st.text_input("Ask a question about the machine")

if st.button("Ask Assistant") and question:

    payload = machine_data.copy()
    payload["question"] = question

    response = requests.post(
        f"{API_BASE}/chat/query",
        json=payload
    )

    if response.status_code == 200:
        result = response.json()

        st.subheader("Assistant Response")
        st.write(result["chatbot_response"])

    else:
        st.error("Chat request failed")