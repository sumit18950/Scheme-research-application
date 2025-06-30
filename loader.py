# utils/loader.py

from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.docstore.document import Document
import logging

logging.basicConfig(level=logging.INFO)

def load_url_content(urls):
    """
    Loads content from a list of URLs using UnstructuredURLLoader.

    Args:
        urls (list): List of URLs.

    Returns:
        tuple: (docs, full_text) or ([], "") if loading fails
    """
    try:
        print("[INFO] Starting to load URLs...")
        loader = UnstructuredURLLoader(urls=urls)
        print("[INFO] Loader initialized. Fetching content...")
        docs = loader.load()
        print(f"[INFO] Loaded {len(docs)} documents.")

        full_text = " ".join([doc.page_content for doc in docs])
        return docs, full_text

    except Exception as e:
        print(f"[ERROR] Failed to load content from URLs: {e}")
        return [], ""


def load_text_file(uploaded_file):
    """
    Loads text content from an uploaded .txt file.

    Args:
        uploaded_file: Streamlit uploaded file object.

    Returns:
        tuple: (docs, full_text)
    """
    try:
        content = uploaded_file.read().decode("utf-8")
        doc = Document(page_content=content)
        print("[INFO] Text file loaded successfully.")
        return [doc], content
    except Exception as e:
        print(f"[ERROR] Failed to read uploaded text file: {e}")
        return [], ""
