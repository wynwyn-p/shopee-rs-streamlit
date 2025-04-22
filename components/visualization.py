import streamlit as st
import plotly.express as px

def show(df):
    st.title("📈 TRỰC QUAN HÓA & INSIGHTS VỀ DỮ LIỆU")

    st.markdown("""
        <div style='font-size: 20px; line-height: 1.7; text-align: justify; margin-bottom: 30px;'>
            Biểu đồ giúp chúng ta biết được sản phẩm nào được ưa chuộng, hành vi người tiêu dùng cũng như xu hướng tiêu dùng trên nền tảng Shopee.
        </div>
    """, unsafe_allow_html=True)

    # --- Tổng quan nhanh ---
    st.markdown("### 📌 **Tổng quan nhanh**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Số lượng sản phẩm", len(df['product_id'].unique()))
    with col2:
        st.metric("Số người dùng", len(df['user_id'].unique()))
    with col3:
        st.metric("Tổng số lượt đánh giá", len(df))

    # --- Xem bảng dữ liệu ---
    st.markdown("### 🗂️ **Xem trước dữ liệu**")
    st.dataframe(df.head(10), use_container_width=True)

    # --- Biểu đồ 1 ---
    st.markdown("### ⭐ **Top 5 sản phẩm có nhiều lượt đánh giá nhất**")
    top_5_reviews = df.groupby('product_name').size().sort_values(ascending=False).head(5).reset_index(name='count')
    fig1 = px.bar(top_5_reviews, x='product_name', y='count', color='count',
                  labels={'product_name': 'Tên sản phẩm', 'count': 'Số lượt đánh giá'},
                  title='TOP 5 SẢN PHẨM CÓ LƯỢT ĐÁNH GIÁ NHIỀU NHẤT')
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

    # --- Biểu đồ 2 ---
    st.markdown("### 🌟 **Top 5 sản phẩm được đánh giá 5 sao nhiều nhất**")
    top_5_stars = df[df['rating'] == 5]['product_name'].value_counts().head(5).reset_index()
    top_5_stars.columns = ['product_name', 'count']
    fig2 = px.bar(top_5_stars, x='product_name', y='count', color='count',
                  labels={'product_name': 'Tên sản phẩm', 'count': 'Số đánh giá 5 sao'},
                  title='TOP 5 SẢN PHẨM ĐƯỢC ĐÁNH GIÁ 5 SAO NHIỀU NHẤT')
    fig2.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig2, use_container_width=True)

    # --- Biểu đồ 3 ---
    st.markdown("### 📊 **Lượt mua và doanh thu theo nhóm sản phẩm**")
    product_group = df.groupby('sub_category').agg(
        purchases=('rating', 'count'),
        total_revenue=('price', 'sum')
    ).reset_index().sort_values(by='total_revenue', ascending=False)

    col_a, col_b = st.columns(2)
    with col_a:
        fig3a = px.bar(product_group, x='sub_category', y='purchases', color='purchases',
                       labels={'sub_category': 'Nhóm sản phẩm', 'purchases': 'Lượt mua'},
                       title='LƯỢT MUA THEO NHÓM SẢN PHẨM')
        fig3a.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig3a, use_container_width=True)
    with col_b:
        fig3b = px.bar(product_group, x='sub_category', y='total_revenue', color='total_revenue',
                       labels={'sub_category': 'Nhóm sản phẩm', 'total_revenue': 'Doanh thu'},
                       title='DOANH THU THEO NHÓM SẢN PHẨM')
        fig3b.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig3b, use_container_width=True)

    # --- Biểu đồ 4 ---
    st.markdown("### 👤 **Top 10 khách hàng có lượt mua nhiều nhất**")
    top_users = df.groupby('user_id').agg(
        purchases=('rating', 'count'),
        purchase_amount=('price', 'sum')
    ).sort_values(by='purchases', ascending=False).head(10).reset_index()
    fig4 = px.bar(top_users, x='user_id', y='purchases', color='purchases',
                  labels={'user_id': 'User ID', 'purchases': 'Lượt mua'},
                  title='TOP 10 NGƯỜI DÙNG CÓ LƯỢT MUA NHIỀU NHẤT')
    fig4.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig4, use_container_width=True)

    # --- Biểu đồ 5 ---
    st.markdown("### 💰 **Top 10 khách hàng chi tiêu nhiều nhất**")
    top_spenders = df.groupby('user_id').agg(
        purchases=('rating', 'count'),
        purchase_amount=('price', 'sum')
    ).sort_values(by='purchase_amount', ascending=False).head(10).reset_index()
    fig5 = px.bar(top_spenders, x='user_id', y='purchase_amount', color='purchase_amount',
                  labels={'user_id': 'User ID', 'purchase_amount': 'Tổng chi tiêu'},
                  title='TOP 10 NGƯỜI DÙNG CHI TIÊU NHIỀU NHẤT')
    fig5.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig5, use_container_width=True)
