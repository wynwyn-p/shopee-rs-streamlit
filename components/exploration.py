import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from components import exploration

def render_exploration(file_1):
    # Giao diện tổng thể
    st.markdown("""
        <style>
            .main .block-container {
                max-width: 95%;
                padding-left: 3rem;
                padding-right: 3rem;
                background-color: #0e1117;
            }
            h1, h3, .metric-label {
                color: #1f77b4;
            }
            table td, table th {
                text-align: center !important;
            }
            .highlight-table thead tr {
                background-color: #1f77b4 !important;
                color: white !important;
            }
            .highlight-table tbody tr:nth-child(even) {
                background-color: #1a1d23;
            }
            .highlight-table tbody tr:nth-child(odd) {
                background-color: #111417;
            }
            .highlight-table tbody tr:hover {
                background-color: #2c3e50;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

    # Tiêu đề
    st.markdown("<h1 style='text-align: center;'>📊 KHÁM PHÁ DỮ LIỆU</h1>", unsafe_allow_html=True)

    # Xem trước dữ liệu
    st.markdown("📁 **Xem trước dữ liệu gốc:**")
    st.dataframe(file_1.head(), use_container_width=True)

    # Thống kê tổng quan nhanh
    st.markdown("### 📌 Tổng quan nhanh")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔢 Số sản phẩm", f"{file_1['product_id'].nunique():,}")
    with col2:
        st.metric("🧩 Nhóm sản phẩm", f"{file_1['sub_category'].nunique():,}")
    with col3:
        st.metric("💵 Giá trung bình", f"{file_1['price'].mean():,.0f}₫")
    with col4:
        avg_rating = file_1['rating'].mean() if 'rating' in file_1.columns else None
        st.metric("⭐ Điểm đánh giá TB", f"{avg_rating:.2f}" if avg_rating else "N/A")

    # Thống kê số lượng giá trị duy nhất
    st.markdown("### 📌 Thống kê số lượng giá trị duy nhất")
    unique_counts = {col: file_1[col].nunique() for col in file_1.columns}
    stats_df = pd.DataFrame(list(unique_counts.items()), columns=["Tên Cột", "Số Giá Trị Khác Nhau"])
    st.dataframe(stats_df.style.set_table_attributes('class="highlight-table"'), use_container_width=True)

    # Biểu đồ phân phối giá
    st.markdown("### 💰 Phân phối giá sản phẩm")
    fig_price = px.histogram(file_1, x="price", nbins=50, title="Phân phối giá sản phẩm",
                             template="plotly_dark", color_discrete_sequence=["#1f77b4"])
    st.plotly_chart(fig_price, use_container_width=True)

    # Biểu đồ rating nếu có
    if 'rating' in file_1.columns and file_1['rating'].notna().sum() > 0:
        st.markdown("### ⭐ Phân phối điểm đánh giá")
        fig_rating = px.histogram(file_1, x="rating", nbins=50, title="Phân phối điểm đánh giá",
                                  template="plotly_dark", color_discrete_sequence=["#FF7F0E"])
        st.plotly_chart(fig_rating, use_container_width=True)

    # Biểu đồ cột số lượng theo nhóm sản phẩm
    st.markdown("### 🧩 Số lượng sản phẩm theo nhóm")
    count_by_cat = file_1['sub_category'].value_counts().reset_index()
    count_by_cat.columns = ['sub_category', 'Số lượng']
    fig_bar = px.bar(count_by_cat, x='sub_category', y='Số lượng',
                     template="plotly_dark", color='sub_category',
                     color_discrete_sequence=px.colors.qualitative.Safe)
    fig_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)
