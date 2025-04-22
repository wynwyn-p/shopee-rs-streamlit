import re
from underthesea import word_tokenize

def clean_and_tokenize(text, stop_words=[]):
    # Chuẩn hóa văn bản
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)  # Xóa ký tự đặc biệt
    text = re.sub(r'\s+', ' ', text).strip()

    # Tách từ tiếng Việt
    tokens = word_tokenize(text, format="text").split()

    # Loại bỏ stopword nếu có
    if stop_words:
        tokens = [token for token in tokens if token not in stop_words]

    return tokens
