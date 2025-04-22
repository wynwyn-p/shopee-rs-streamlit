import streamlit as st
from streamlit_option_menu import option_menu

def show():
    with st.sidebar:
        st.image("https://seeklogo.com/images/S/shopee-logo-A3D65B6C50-seeklogo.com.png", width=120)
        st.markdown("""
        <h3 style='text-align:center; color:#1f77b4;'>Shopee Recommender</h3>
        <hr>
        👤 <b>Nguyễn Vũ Mai Phương</b><br>
        👤 <b>Nguyễn Nhật Tố Trân</b><br>
        👨‍🏫 <b>GVHD: Cô Khuất Thùy Phương</b><br>
        📅 <b>12/04/2025</b>
        """, unsafe_allow_html=True)
        selected = option_menu("Recommendation System",
            ["Introduction", "Data Exploration", "Data Visualization", "Link Code", "Demo App"],
            icons=["house", "search", "bar-chart", "link-45deg", "cpu"],
            default_index=0)
        st.session_state["selected_page"] = selected