import streamlit as st
from PIL import Image

def show():
    st.markdown('<h1 style="color:#f0f0f0;">📌 GIỚI THIỆU PROJECT</h1>', unsafe_allow_html=True)
    st.markdown(
    """
    <div style="
        background-color: #1e1e1e;
        border: 1px solid #444;
        border-radius: 12px;
        padding: 30px;
        box-shadow: 2px 2px 10px rgba(255,255,255,0.05);
        font-size: 18px;
        line-height: 1.8;
        text-align: justify;
        margin: 20px 40px;
        color: #f0f0f0;
    ">

    Trong thời đại thương mại điện tử phát triển bùng nổ, việc cá nhân hóa trải nghiệm mua sắm ngày càng trở nên quan trọng.

    Giả sử <b>Shopee</b> – một trong những nền tảng mua sắm trực tuyến hàng đầu – vẫn chưa triển khai <b>hệ thống gợi ý sản phẩm (Recommendation System)</b>.<br>
    Điều này đặt ra bài toán: <i>Làm thế nào để Shopee có thể tối ưu hóa doanh thu và nâng cao sự hài lòng của khách hàng</i> thông qua các chiến dịch quảng cáo và truyền thông hiệu quả?

    <br><br>
    🔍 <b>Giải pháp:</b> Xây dựng hệ thống đề xuất sản phẩm thông minh, nhằm:
    <ul>
        <li>Gợi ý các sản phẩm phù hợp với từng người dùng.</li>
        <li>Tăng tỷ lệ chuyển đổi và thời gian tương tác của khách hàng.</li>
        <li>Thiết kế chương trình khuyến mãi nhắm đúng đối tượng mục tiêu.</li>
    </ul>

    Thông qua việc áp dụng các kỹ thuật phân tích dữ liệu và học máy (<i>Machine Learning</i>), hệ thống đề xuất không chỉ hỗ trợ bán hàng hiệu quả mà còn mang lại trải nghiệm cá nhân hóa tối ưu cho từng khách hàng.

    <br><br>
    💡 <b>Trong project này, chúng em sử dụng bộ dataset được "cào" từ Shopee với hơn 1 triệu dòng. Hệ thống gợi ý sản phẩm sử dụng:</b>
    <ul>
        <li><b>Collaborative Filtering</b> (Surprise - BaselineOnly)</li>
        <li><b>Content-based Filtering</b> (Gensim TF-IDF)</li>
    </ul>

    </div>
    """,
    unsafe_allow_html=True
    )

    try:
        image = Image.open("assets/shopee_1.jpg")
        st.image(image, caption="Shopee - nền tảng mua sắm trực tuyến hàng đầu Việt Nam", use_container_width=True)
    except Exception as e:
        st.error(f"Lỗi khi mở ảnh: {e}")