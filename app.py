from __future__ import annotations

import streamlit as st

from src.rag import answer_question


st.set_page_config(page_title="Winnipeg RAG", layout="wide")
st.title("Winnipeg RAG")

question = st.text_area("Question", height=110)

if st.button("Ask", type="primary") and question.strip():
    with st.spinner("Searching Winnipeg documentation..."):
        answer, sources = answer_question(question.strip())

    st.subheader("Answer")
    st.write(answer)

    st.subheader("Retrieved Sources")
    for source in sources:
        meta = source["metadata"]
        with st.expander(f"{meta['file_name']} | score {source['score']:.3f}"):
            st.caption(meta["path"])
            st.write(source["text"])

