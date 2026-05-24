import streamlit as st
import pickle
import numpy as np

st.set_page_config(
    page_title="Laptop Price Predictor",
    page_icon="💻",
    layout="wide",
)

pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

st.markdown("""
    <h1 style='text-align: center; color: #4F8BF9;'>💻 Laptop Price Predictor</h1>
    <p style='text-align: center; color: grey; font-size: 16px;'>
        Configure your dream laptop and get an instant price estimate powered by Machine Learning.
    </p>
    <hr/>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🏷️ Basic Info")
    company = st.selectbox('Brand', df['Company'].unique())
    type = st.selectbox('Type', df['TypeName'].unique())
    ram = st.selectbox('RAM (in GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])
    weight = st.number_input('Weight (in kg)', min_value=0.5, max_value=5.0, value=1.5, step=0.1)
    os = st.selectbox('Operating System', df['os'].unique())

with col2:
    st.subheader("🖥️ Display")
    screen_size = st.slider('Screen Size (inches)', 10.0, 18.0, 13.0)
    resolution = st.selectbox('Screen Resolution', [
        '1920x1080', '1366x768', '1600x900',
        '3840x2160', '3200x1800', '2880x1800',
        '2560x1600', '2560x1440', '2304x1440'
    ])
    touchscreen = st.radio('Touchscreen', ['No', 'Yes'], horizontal=True)
    ips = st.radio('IPS Display', ['No', 'Yes'], horizontal=True)

with col3:
    st.subheader("⚙️ Performance")
    cpu = st.selectbox('CPU Brand', df['Cpu brand'].unique())
    gpu = st.selectbox('GPU Brand', df['Gpu brand'].unique())
    hdd = st.selectbox('HDD (in GB)', [0, 128, 256, 512, 1024, 2048])
    ssd = st.selectbox('SSD (in GB)', [0, 8, 128, 256, 512, 1024])

st.markdown("<hr/>", unsafe_allow_html=True)

col_btn, col_summary = st.columns([1, 2])

with col_btn:
    predict_btn = st.button('🔍 Predict Price', use_container_width=True)

with col_summary:
    st.markdown(f"""
    **Selected Config:** {company} · {type} · {ram}GB RAM · {screen_size}" {resolution}
    CPU: {cpu} · GPU: {gpu} · HDD: {hdd}GB · SSD: {ssd}GB · OS: {os}
    """)

if predict_btn:
    touchscreen_val = 1 if touchscreen == 'Yes' else 0
    ips_val = 1 if ips == 'Yes' else 0

    X_res, Y_res = int(resolution.split('x')[0]), int(resolution.split('x')[1])
    ppi = ((X_res**2) + (Y_res**2))**0.5 / screen_size

    query = np.array([company, type, ram, weight, touchscreen_val, ips_val, ppi, cpu, hdd, ssd, gpu, os])
    query = query.reshape(1, 12)

    with st.spinner('Calculating best price...'):
        predicted_log_price = pipe.predict(query)[0]
        predicted_price = int(np.exp(predicted_log_price))

    low = int(predicted_price * 0.90)
    high = int(predicted_price * 1.10)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.success("Prediction Complete!")

    r1, r2, r3 = st.columns(3)
    r1.metric("💰 Estimated Price", f"₹{predicted_price:,}")
    r2.metric("📉 Lower Bound (~10%)", f"₹{low:,}")
    r3.metric("📈 Upper Bound (~10%)", f"₹{high:,}")

    st.balloons()
