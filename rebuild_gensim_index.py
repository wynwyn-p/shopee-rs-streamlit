from gensim import corpora, models, similarities
import os

# Đường dẫn
BASE_PATH = "models"
DICT_PATH = os.path.join(BASE_PATH, "dictionary_tokenized.dict")
TFIDF_PATH = os.path.join(BASE_PATH, "tfidf_model_gensim.pkl")
CORPUS_PATH = os.path.join(BASE_PATH, "corpus_tokenized.mm")
OUTPUT_INDEX = os.path.join(BASE_PATH, "gensim_index_merged")

# Load dictionary & TF-IDF model
print("Đang load dictionary & mô hình TF-IDF...")
dictionary = corpora.Dictionary.load(DICT_PATH)
tfidf_model = models.TfidfModel.load(TFIDF_PATH)

# Load corpus BoW
print("Đang load corpus BoW...")
corpus_bow = corpora.MmCorpus(CORPUS_PATH)

# Biến corpus sang TF-IDF vector
print("Chuyển BoW → TF-IDF...")
corpus_tfidf = tfidf_model[corpus_bow]

# Tạo index mới
print("Đang tạo Gensim Similarity index...")
index = similarities.Similarity(
    output_prefix=OUTPUT_INDEX,
    corpus=corpus_tfidf,
    num_features=len(dictionary),
    chunksize=256  # có thể điều chỉnh nếu RAM thấp
)

# Lưu index
index.save(OUTPUT_INDEX)
print(f"Đã lưu index tại: {OUTPUT_INDEX}")
