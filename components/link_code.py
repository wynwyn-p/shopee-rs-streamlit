import streamlit as st

def show():
    st.title("LIÊN KẾT MÃ NGUỒN")

    st.markdown("""
    <div style='font-size: 18px; line-height: 1.8; text-align: justify; background-color: #111111; padding: 20px; border-radius: 10px; color: white;'>
        📂 <b>Xem toàn bộ mã nguồn của đồ án tại:</b><br>
        👉 <a href="https://drive.google.com/drive/u/0/folders/1LWkvBy4MUGA08mJMVxFwQs8gKP6VbO-a" target="_blank" style="color:#1faee9; font-weight:bold;">
            Google Drive - Source Code (Click vào đây)
        </a>
    </div>
    """, unsafe_allow_html=True)
