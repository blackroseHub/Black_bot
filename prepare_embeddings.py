from loader_splitter import load_and_split
from embedder_store import create_vector_store
import os

# 📜 SETTINGS
FOLDER_PATH = "./data"  # Your documents folder

if __name__ == "__main__":
    if not os.path.exists(FOLDER_PATH):
        raise Exception(f"❌ Folder {FOLDER_PATH} does not exist!")

    print(f"🔎 Loading and splitting documents from {FOLDER_PATH}...")
    chunks = load_and_split(FOLDER_PATH)

    print(f"🧠 Creating embeddings and saving to ChromaDB...")
    create_vector_store(chunks)

    print("✅ Embeddings successfully created and stored!")
