import streamlit as st
from google import genai
from google.genai import types

st.title("Chatbot Gemini")

# 1. Khởi tạo client Gemini (sử dụng API key từ Streamlit Secrets hoặc biến môi trường)
# Nếu dùng Secrets: st.secrets["GEMINI_API_KEY"]
client = genai.Client()

# 2. Khởi tạo lịch sử hội thoại cho Streamlit UI và Lịch sử API
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Hiển thị lại các tin nhắn cũ trong phiên làm việc
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Xử lý khi người dùng gửi tin nhắn mới
if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
    # Hiển thị tin nhắn người dùng lên giao diện
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Chuyển đổi lịch sử chat sang định dạng API Gemini yêu cầu
    contents = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=msg["content"])]
            )
        )

    # Hiển thị phản hồi từ Gemini dạng Streaming
    with st.chat_message("assistant"):
        # Gọi API với phản hồi stream
        response_stream = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=contents,
        )
        
        # Đọc dữ liệu stream và hiển thị từng từ lên màn hình
        full_response = st.write_stream(chunk.text for chunk in response_stream)

    # Lưu phản hồi của trợ lý vào lịch sử trò chuyện
    st.session_state.messages.append({"role": "assistant", "content": full_response})
  
