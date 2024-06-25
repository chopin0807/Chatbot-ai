import streamlit as st
from streamlit_chat import message
from chatgpt_answer import retrieve
from chatgpt_answer import response
 
def generate_response():
    # open ai에서 발급받은 api key를 등록
    api_key = "<발급 api key>"
    retriever = retrieve(api_key)
    return retriever
 
 
st.header("🤖한양대학교 창업지원단 챗봇 AI")
st.markdown("ChatGPT와 RAG 이용")

db = generate_response()
 
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
 
if 'past' not in st.session_state:
    st.session_state['past'] = []
 
with st.form('form', clear_on_submit=True):
    user_input = st.text_input('질문: ', '', key='input')
    submitted = st.form_submit_button('보내기')
 
if submitted and user_input:
    output = response(db, user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)
 
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))