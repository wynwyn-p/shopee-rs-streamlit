import streamlit as st
import pandas as pd
from utils.recommenders import (
    recommend_baseline,
    recommend_similar_products_by_content,
    recommend_similar_products_by_options,
    display_results
)

def show(file_2, file_1, df, df_final, dictionary, tfidf_model, similarity_index, stop_words, baseline_model):
    st.markdown("## 🧠 Demo Recommendation")

    top_k = st.slider("📦 Số lượng sản phẩm muốn gợi ý:", 1, 20, 5)

    tab_cf, tab_content = st.tabs(["👤 Theo tài khoản Shopee", "🛍️ Theo sản phẩm"])

    # ============================== TAB 1: Collaborative Filtering ==============================
    with tab_cf:
        st.markdown("#### 🧑 Nhập hoặc chọn tài khoản Shopee")

        top_users = df['user_id'].value_counts().head(20).index.tolist() if 'user_id' in df.columns else []

        col1, col2 = st.columns([2, 3])
        with col1:
            selected_user = st.selectbox("🔽 Chọn user_id phổ biến:", options=top_users, index=0 if top_users else None)
        with col2:
            user_input = st.text_input("✍️ Hoặc nhập user_id:", key="user_input_cf")

        final_user_input = user_input.strip() if user_input.strip() else str(selected_user)

        if st.button("🚀 Gợi ý sản phẩm (CF)", key="submit_user_cf"):
            if final_user_input.isdigit():
                user_id = int(final_user_input)
                results = recommend_baseline(user_id, top_k, df_final, baseline_model)
                if results is not None and not results.empty:
                    display_results(results, method="cf")
                else:
                    st.warning("❌ Không có gợi ý cho user_id này.")
            else:
                st.warning("⚠️ Vui lòng nhập hoặc chọn user_id hợp lệ.")

    # ============================== TAB 2: Content-Based Filtering ==============================
    with tab_content:
        st.markdown("#### 📋 Chọn cách nhập thông tin sản phẩm")

        method = st.radio(
            "🔍 Chọn phương thức nhập sản phẩm:",
            ["Mô tả sản phẩm", "ID sản phẩm", "Tên sản phẩm"],
            horizontal=True,
            key="method_selector"
        )

        query = ""
        if method == "Mô tả sản phẩm":
            query = st.text_area("📝 Nhập mô tả sản phẩm:", key="desc_input")

        elif method == "ID sản phẩm":
            top_product_ids = df_final['product_id'].astype(str).value_counts().head(30).index.tolist()
            col1, col2 = st.columns([2, 3])
            with col1:
                selected_id = st.selectbox("🔽 Chọn mã sản phẩm:", options=top_product_ids, key="product_id_dropdown")
            with col2:
                input_id = st.text_input("✍️ Hoặc nhập ID sản phẩm:", key="product_id_input")
            query = input_id.strip() if input_id.strip() else selected_id

        elif method == "Tên sản phẩm":
            top_product_names = df_final['product_name'].value_counts().head(30).index.tolist()
            col1, col2 = st.columns([2, 3])
            with col1:
                selected_name = st.selectbox("🔽 Chọn tên sản phẩm:", options=top_product_names, key="product_name_dropdown")
            with col2:
                input_name = st.text_input("✍️ Hoặc nhập tên sản phẩm:", key="product_name_input")
            query = input_name.strip() if input_name.strip() else selected_name

        if st.button("🚀 Gợi ý sản phẩm (Content-Based)", key="recommend_content_button"):
            if query:
                with st.spinner("🔍 Đang tìm sản phẩm tương tự..."):
                    msg, results = recommend_similar_products_by_options(
                        input_text=query,
                        dictionary=dictionary,
                        tfidf_model=tfidf_model,
                        similarity_index=similarity_index,
                        df_final=df_final,
                        stop_words=stop_words,
                        top_k=top_k
                    )

                if isinstance(results, pd.DataFrame) and not results.empty:
                    display_results(results, method="content")
                else:
                    st.warning(msg)
            else:
                st.warning("⚠️ Vui lòng nhập thông tin sản phẩm hợp lệ.")
