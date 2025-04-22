import re
import streamlit as st
import pandas as pd
from gensim import corpora, models, similarities
from underthesea import word_tokenize
from .preprocessing import clean_and_tokenize

# ==================== Gợi ý sản phẩm theo user_id với mô hình BaselineOnly ====================
def recommend_baseline(user_id, top_k, df_final, baseline_model):
    rated_products = df_final[df_final['user_id'] == user_id]['product_id'].tolist()
    all_products = df_final['product_id'].unique()
    products_to_predict = [pid for pid in all_products if pid not in rated_products]

    predictions = []
    for pid in products_to_predict:
        try:
            pred = baseline_model.predict(uid=str(user_id), iid=str(pid))
            predictions.append((pid, pred.est))
        except:
            continue

    top_predictions = sorted(predictions, key=lambda x: x[1], reverse=True)[:top_k]
    top_product_ids = [pid for pid, _ in top_predictions]

    result_df = df_final[df_final['product_id'].isin(top_product_ids)].copy()
    result_df['predicted_rating'] = result_df['product_id'].map(dict(top_predictions))
    result_df = result_df.drop_duplicates(subset='product_id')
    result_df = result_df.sort_values(by='predicted_rating', ascending=False)

    return result_df[['product_id', 'product_name', 'image', 'price', 'link', 'rating', 'description', 'predicted_rating']]

# ==================== Gợi ý theo mô tả ====================
def recommend_similar_products_by_content(content, df_final, dictionary, tfidf_model, similarity_index, stop_words, top_k=5):
    try:
        tokens = clean_and_tokenize(content, stop_words)
        if not tokens:
            return pd.DataFrame()

        content_bow = dictionary.doc2bow(tokens)
        content_tfidf = tfidf_model[content_bow]
        sims = similarity_index[content_tfidf]
        top_matches = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)

        results = []
        seen_ids = set()
        for i, score in top_matches:
            if len(results) >= top_k:
                break
            product = df_final.iloc[i]
            pid = product.get('product_id')
            if not pid or pid in seen_ids:
                continue
            seen_ids.add(pid)

            results.append({
                "product_id": pid,
                "product_name": product.get("product_name"),
                "price": product.get("price", 0),
                "image": product.get("image"),
                "rating": product.get("rating"),
                "description": product.get("description"),
                "link": product.get("link"),
                "score": score
            })

        return pd.DataFrame(results)

    except Exception as e:
        print("Lỗi khi gợi ý sản phẩm theo content:", e)
        return pd.DataFrame()

# ==================== Gợi ý theo product_id hoặc product_name ====================
def recommend_similar_products_by_options(input_text, dictionary, tfidf_model, similarity_index, df_final, stop_words, top_k=5):
    row = None

    # Nếu input là số → tìm theo product_id
    if input_text.isdigit():
        row = df_final[df_final['product_id'].astype(str) == input_text]

    # Nếu không tìm được theo ID → tìm theo tên (không dùng regex để tránh lỗi)
    if row is None or row.empty:
        row = df_final[df_final['product_name'].str.lower().str.contains(input_text.lower(), regex=False)]

    # Nếu không tìm thấy gì
    if row.empty:
        return f"Không tìm thấy sản phẩm với thông tin: `{input_text}`", pd.DataFrame()

    # Lấy thông tin mô tả từ sản phẩm đầu tiên tìm được
    product = row.iloc[0]
    description = product.get('description', '')

    if pd.isna(description) or not isinstance(description, str) or not description.strip():
        return f"Mô tả sản phẩm không hợp lệ hoặc bị thiếu cho **{product['product_name']}**", pd.DataFrame()

    # Làm sạch và tokenize mô tả
    tokens = clean_and_tokenize(description, stop_words)
    if not tokens:
        return f"Mô tả sau khi xử lý không còn từ khóa hợp lệ.", pd.DataFrame()

    # Tính TF-IDF và độ tương đồng
    bow = dictionary.doc2bow(tokens)
    tfidf_vec = tfidf_model[bow]
    sims = similarity_index[tfidf_vec]
    top_indices = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)

    # Lọc kết quả
    results = []
    seen_ids = set()
    for i, score in top_indices:
        if len(results) >= top_k:
            break
        similar_product = df_final.iloc[i]
        pid = similar_product.get('product_id')
        if pid == product['product_id'] or pid in seen_ids:
            continue
        seen_ids.add(pid)
        results.append({
            "product_id": pid,
            "product_name": similar_product.get("product_name"),
            "price": similar_product.get("price"),
            "image": similar_product.get("image"),
            "rating": similar_product.get("rating"),
            "description": similar_product.get("description"),
            "link": similar_product.get("link"),
            "score": score
        })

    result_df = pd.DataFrame(results)
    return product['product_name'], result_df

# ==================== Hiển thị kết quả ====================
def display_results(
    results,
    method="cf",
    dictionary=None,
    tfidf_model=None,
    similarity_index=None,
    stop_words=None,
    df_final=None,
    top_k=5
):
    st.markdown("### 🎯 Các sản phẩm gợi ý:")

    if results.empty:
        st.info("⚠️ Không có sản phẩm nào phù hợp.")
        return

    for idx, row in results.iterrows():
        # Xử lý ảnh (ảnh mặc định nếu thiếu)
        image_url = row.get("image", "")
        if not isinstance(image_url, str) or image_url.strip() == "":
            image_url = "https://via.placeholder.com/100x100.png?text=No+Image"

        # Mô tả ngắn
        description = row.get("description", "")
        short_desc = description[:200] + "..." if description and isinstance(description, str) and len(description) > 200 else description

        # Layout chia 2 cột
        with st.container():
            cols = st.columns([1, 4])
            with cols[0]:
                st.image(image_url, width=120)
            with cols[1]:
                st.markdown(f"### 🛍️ {row.get('product_name', 'Không có tên')}")
                if "price" in row:
                    st.markdown(f"💰 **Giá**: `{int(row['price']):,}₫`")
                if "rating" in row:
                    st.markdown(f"⭐ **Đánh giá**: `{row['rating']}`")
                if short_desc:
                    with st.expander("📄 Xem mô tả chi tiết"):
                        st.markdown(description)
                    st.markdown(f"📝 *{short_desc}*")

                if row.get("link"):
                    st.markdown(f"🔗 [Xem chi tiết tại đây]({row['link']})")

            st.markdown("---")