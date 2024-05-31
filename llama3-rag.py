import streamlit as st
import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
st.title("한양대학교 챗봇 AI 🌐")
st.caption("local Llama-3와 RAG 이용")

# 1. 수집된 웹 데이터 txt파일 불러오기
loader = TextLoader("keyword.txt", encoding = 'utf-8')
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20, length_function = len)
splits = text_splitter.split_documents(docs)
# 2. Ollama 임베딩 진행
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
# 3. Call Ollama Llama3 model
def ollama_llm(question, context):
    formatted_prompt = f"Question: {question}\n\nContext: {context}"
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': formatted_prompt}])
    return response['message']['content']
# 4. RAG Setup
retriever = vectorstore.as_retriever()

def combine_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def rag_chain(question):
    retrieved_docs = retriever.invoke(question)
    formatted_context = combine_docs(retrieved_docs)
    return ollama_llm(question, formatted_context)

# Ask a question about the webpage
prompt = st.text_input("질문")

# Chat with the webpage
if prompt:
    result = rag_chain(prompt)
    st.write(result)