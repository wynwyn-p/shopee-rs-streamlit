import os
import gdown

def download_models(folder_url="https://drive.google.com/drive/u/0/folders/1mB2wQqf1OspB8_wulXMaoxd_2W0fRpdj", model_dir="models"):
    """
    Tải toàn bộ mô hình từ Google Drive folder về thư mục models/
    """
    if os.path.exists(os.path.join(model_dir, "baseline_only_model.pkl")):
        print("Models already exist. Skip downloading.")
        return

    print("Downloading models from Google Drive...")
    os.makedirs(model_dir, exist_ok=True)
    gdown.download_folder(url=folder_url, output=model_dir, quiet=False, use_cookies=False)
    print("All models downloaded.")

if __name__ == "__main__":
    download_models()
