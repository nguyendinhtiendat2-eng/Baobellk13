import streamlit as st
from google import genai

st.title("Chatbot Gemini với Streamlit")

# Khởi tạo client Gemini (sử dụng API key từ environment variable hoặc secrets)
client = genai.Client(api_key="API_KEY_CUA_BAN")

# Lưu lịch sử chat vào session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Nhận phản hồi từ người dùng
if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
    # Hiển thị câu hỏi của người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gọi API Gemini để tạo câu trả lời
    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        st.markdown(response.text)
        
    st.session_state.messages.append({"role": "assistant", "content": response.text})
  
