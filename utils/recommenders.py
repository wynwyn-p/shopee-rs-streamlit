import os
import re
import joblib
import pandas as pd
from gensim import corpora, models, similarities
from .preprocessing import clean_and_tokenize

# ==================== Load models, corpus, index ====================

def load_all_models(base_path="models"):
    df_final = pd.read_parquet(os.path.join(base_path, 'df_final_new.parquet'))
    dictionary = corpora.Dictionary.load(os.path.join(base_path, 'dictionary_tokenized.dict'))
    tfidf_model = models.TfidfModel.load(os.path.join(base_path, 'tfidf_model_gensim.pkl'))
    similarity_index = similarities.Similarity.load(os.path.join(base_path, 'similarity_index_gensim.pkl'))
    baseline_model = joblib.load(os.path.join(base_path, 'baseline_only_model.pkl'))

    return dictionary, tfidf_model, similarity_index, df_final, baseline_model


# ==================== Gợi ý theo user_id (CF) ====================

def recommend_baseline(user_id, top_k, df, model=None):
    if model is None:
        return pd.DataFrame()

    all_items = df['product_id'].unique()
    predictions = []

    for item_id in all_items:
        pred = model.predict(user_id, item_id)
        predictions.append((item_id, pred.est))

    top_items = sorted(predictions, key=lambda x: x[1], reverse=True)[:top_k]
    top_df = df[df['product_id'].isin([item[0] for item in top_items])].drop_duplicates('product_id')

    return top_df


# ==================== Gợi ý theo nội dung mô tả ====================

def recommend_similar_products_by_content(content, df_final, dictionary, tfidf_model, similarity_index, stop_words, top_k=5):
    try:
        tokens = clean_and_tokenize(content, stop_words)
        content_bow = dictionary.doc2bow(tokens)
        content_tfidf = tfidf_model[content_bow]
        sims = similarity_index[content_tfidf]

        top_matches = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[1:]

        results = []
        seen_ids = set()

        for i, score in top_matches:
            product = df_final.iloc[i]
            pid = product.get('product_id')
            if not pid or pid in seen_ids:
                continue
            seen_ids.add(pid)

            results.append({
                "product_id": pid,
                "product_name": product.get('product_name'),
                "image": product.get('image'),
                "link": product.get('link'),
                "rating": product.get('rating'),
                "description": product.get('description'),
                "similarity": round(score, 3)
            })

            if len(results) >= top_k:
                break

        return pd.DataFrame(results)

    except Exception as e:
        return pd.DataFrame()


# ==================== Gợi ý theo mô tả / product_id / tên ====================

def recommend_similar_products_by_options(input_text, top_k=5):
    dictionary, tfidf_model, similarity_index, df_final, _ = load_all_models()

    row = None
    if input_text.isdigit():
        row = df_final[df_final['product_id'] == int(input_text)]

    if row is None or row.empty:
        row = df_final[df_final['product_name'].str.lower().str.contains(input_text.lower())]

    if row.empty:
        return f"Không tìm thấy sản phẩm với thông tin: {input_text}", pd.DataFrame()

    product = row.iloc[0]
    description = product.get('description', '')

    if pd.isna(description) or not isinstance(description, str) or not description.strip():
        return f"Mô tả sản phẩm không hợp lệ hoặc bị thiếu cho '{product['product_name']}'", pd.DataFrame()

    cleaned = re.sub(r'[^\w\s]', ' ', description.lower())
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    bow = dictionary.doc2bow(cleaned.split())
    tfidf_vec = tfidf_model[bow]
    sims = similarity_index[tfidf_vec]

    top_matches = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[1:]

    results = []
    seen_ids = set()

    for i, score in top_matches:
        item = df_final.iloc[i]
        pid = item.get('product_id')
        if not pid or pid in seen_ids:
            continue
        seen_ids.add(pid)

        results.append({
            "product_id": pid,
            "product_name": item.get('product_name'),
            "image": item.get('image'),
            "link": item.get('link'),
            "rating": item.get('rating'),
            "description": item.get('description'),
            "similarity": round(score, 3)
        })

        if len(results) >= top_k:
            break

    return "", pd.DataFrame(results)
    
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
