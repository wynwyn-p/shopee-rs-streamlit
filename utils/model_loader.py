import os
import joblib
import pandas as pd
from gensim import corpora, models, similarities
from gensim.corpora import MmCorpus
import streamlit as st

@st.cache_resource(show_spinner="Đang tải mô hình...")
def load_all_models(base_path="models"):
    df_final = pd.read_parquet(os.path.join(base_path, 'df_final_new.parquet'))

    dictionary = corpora.Dictionary.load(os.path.join(base_path, 'dictionary_tokenized.dict'))
    tfidf_model = models.TfidfModel.load(os.path.join(base_path, 'tfidf_model_gensim.pkl'))

    similarity_index_path = os.path.join(base_path, 'gensim_index_merged')
    similarity_index = similarities.Similarity.load(similarity_index_path)

    baseline_model = joblib.load(os.path.join(base_path, 'baseline_only_model.pkl'))

    return dictionary, tfidf_model, similarity_index, df_final, baseline_model
