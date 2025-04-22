import re

def clean_and_tokenize(text, stop_words=None):
    """
    Làm sạch và tách từ đơn giản bằng regex, không cần underthesea.
    """
    # Loại bỏ ký tự đặc biệt, chuyển về thường
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    text = re.sub(r'\s+', ' ', text).strip()

    # Tách từ đơn giản
    tokens = text.split()

    # Loại bỏ stopwords nếu có
    if stop_words:
        tokens = [t for t in tokens if t not in stop_words]

    return tokens
