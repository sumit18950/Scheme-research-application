import streamlit as st
import os
import pickle
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Import your custom utility functions
from utils.loader import load_url_content
from utils.processor import process_text_and_create_faiss
from utils.qa_engine import answer_query

# Streamlit page config
st.set_page_config(page_title="Scheme Research Tool", layout="wide")
st.title("📑 Scheme Research Application")

# Sidebar: Input section
st.sidebar.header("Enter Scheme Article URLs")
urls = st.sidebar.text_area("Paste one or more scheme URLs (one per line)").splitlines()

# Process Button
if st.sidebar.button("Process URLs"):
    if not urls or all(url.strip() == "" for url in urls):
        st.error("⚠️ Please enter at least one valid URL.")
    else:
        with st.spinner("🔄 Loading and processing articles..."):
            try:
                docs, full_text = load_url_content(urls)

                if not docs or len(docs) == 0:
                    st.error("❌ Failed to load content from the provided URLs.")
                else:
                    # Create FAISS index
                    st.session_state['index'] = process_text_and_create_faiss(docs)

                    # Save FAISS index to file
                    with open("faiss_store_openai.pkl", "wb") as f:
                        pickle.dump(st.session_state['index'], f)

                    st.success("✅ Articles processed and indexed successfully!")
            except Exception as e:
                st.error(f"🚫 Error occurred during processing: {e}")

# Query Section
st.markdown("### Ask a question based on the processed scheme articles")
query = st.text_input("🔍 Type your question (e.g., What are the eligibility criteria?)")

if query and 'index' in st.session_state:
    with st.spinner("💬 Getting answer from AI..."):
        try:
            answer, sources = answer_query(query, st.session_state['index'])

            st.markdown("### ✅ Answer")
            st.write(answer)

            st.markdown("### 🔗 Sources")
            for src in sources:
                st.markdown(f"- {src}")
        except Exception as e:
            st.error(f"❌ Could not retrieve answer: {e}")
elif query and 'index' not in st.session_state:
    st.warning("⚠️ Please process URLs first before asking questions.")
