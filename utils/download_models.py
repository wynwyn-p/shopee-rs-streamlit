import os
import gdown

def download_models(folder_url="https://drive.google.com/drive/u/0/folders/1mB2wQqf1OspB8_wulXMaoxd_2W0fRpdj", model_dir="models"):
    """
    Tải toàn bộ mô hình từ Google Drive folder về thư mục models/
    """
    model_check_file = os.path.join(model_dir, "baseline_only_model.pkl")

    if os.path.exists(model_check_file):
        print("✅ Models already exist. Skip downloading.")
        return

    print("📥 Downloading models from Google Drive...")
    os.makedirs(model_dir, exist_ok=True)
    
    try:
        gdown.download_folder(
            url=folder_url,
            output=model_dir,
            quiet=False,
            use_cookies=False
        )
        print("✅ All models downloaded.")
    except Exception as e:
        print(f"❌ Error downloading models: {e}")

if __name__ == "__main__":
    download_models()
