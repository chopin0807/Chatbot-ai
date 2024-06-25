from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import create_qa_with_sources_chain
from langchain.chains import ConversationalRetrievalChain

# open ai에서 발급받은 api key를 등록
api_key = "<발급 api key>"

def retrieve(api_key):
    # 키워드 문서 로딩
    loader = TextLoader('keyword.txt', encoding = 'utf-8')
    data = loader.load()

    # 키워드 분할
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 300, chunk_overlap = 50, length_function = len)
    document = text_splitter.split_documents(data)

    # 저장
    embedding_model = OpenAIEmbeddings(api_key=api_key)
    db = Chroma.from_documents(document, embedding_model)

    # 지식 검색
    retriever = db.as_retriever()
    # 응답 생성
    llm_src = ChatOpenAI(temperature = 0, model = "gpt-3.5-turbo", api_key = api_key)
    retrieval_qa = ConversationalRetrievalChain.from_llm(llm_src, retriever)
    return retrieval_qa

def response(retrieval_qa, question):
    # 질의응답 출력
    output = retrieval_qa({
        "question": question,
        "chat_history": []
    })

    return f"{output['answer']}"