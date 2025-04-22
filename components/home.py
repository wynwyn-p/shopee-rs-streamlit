import streamlit as st

def show():
    st.markdown("""
        <h1 style='text-align:center; color:#f0f0f0;'>🎓 ĐỒ ÁN CUỐI KHÓA</h1>
        <div style='background-color:#1e1e1e; padding: 30px; border-radius: 10px; color: #ccc; margin: 30px;'>
            <p style='font-size: 18px; line-height: 1.7;'>
                Chào mừng bạn đến với hệ thống gợi ý sản phẩm Shopee! 🎉<br><br>
                Đây là đồ án tốt nghiệp nhằm xây dựng hệ thống gợi ý sản phẩm thông minh dựa trên kỹ thuật Collaborative và Content-based Filtering.
                <br><br>
                🔍 Ứng dụng sử dụng dữ liệu thực tế từ Shopee với hơn 1 triệu dòng sản phẩm và đánh giá.<br>
                🚀 Được phát triển với Python, Streamlit, Surprise, Gensim và nhiều thư viện khác.
                <br><br>
                👉 Hãy khám phá các mục bên trái để tìm hiểu thêm!
            </p>
        </div>
    """, unsafe_allow_html=True)