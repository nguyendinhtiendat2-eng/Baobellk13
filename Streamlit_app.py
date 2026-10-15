import streamlit as st

# Cấu hình giao diện trang
st.set_page_config(
    page_title="Thám Tử Hóa Học - Chinh Phục Khoa Học",
    page_icon="🧪",
    layout="centered"
)

# Danh sách câu hỏi từ lớp 6 đến lớp 9
QUESTIONS = [
    {
        "level": "Lớp 6 - Khoa học Tự nhiên",
        "question": "Khí nào chiếm thể tích lớn nhất trong không khí (khoảng 78%)?",
        "options": ["Khí Ô-xi", "Khí Nitơ", "Khí Cac-bon-đích", "Hơi nước"],
        "answer": 1,
        "explanation": "Không khí chứa khoảng 78% khí Nitơ, 21% khí Ô-xi và 1% các khí khác."
    },
    {
        "level": "Lớp 6 - Khoa học Tự nhiên",
        "question": "Hiện tượng nào sau đây là hiện tượng hóa học?",
        "options": [
            "Đường hòa tan vào nước",
            "Nước lỏng bay hơi thành hơi nước",
            "Dây sắt bị đốt nóng đỏ chảy lỏng",
            "Đinh sắt để ngoài không khí bị gỉ sét"
        ],
        "answer": 3,
        "explanation": "Đinh sắt bị gỉ sét tạo ra chất mới (sắt oxit), đây là hiện tượng hóa học. Các câu khác là hiện tượng vật lý."
    },
    {
        "level": "Lớp 7 - Khoa học Tự nhiên",
        "question": "Ký hiệu hóa học của nguyên tố Natri là gì?",
        "options": ["Na", "N", "K", "Cu"],
        "answer": 0,
        "explanation": "Natri có ký hiệu hóa học là Na (tên tiếng Latinh: Natrium)."
    },
    {
        "level": "Lớp 7 - Khoa học Tự nhiên",
        "question": "Công thức hóa học của nước là gì?",
        "options": ["H2O2", "H2O", "HO2", "OH2"],
        "answer": 1,
        "explanation": "Nước là hợp chất tạo bởi 2 nguyên tố Hydro (H) và Oxi (O) với công thức hóa học là H2O."
    },
    {
        "level": "Lớp 8 - Hóa học",
        "question": "Tính khối lượng mol phân tử của khí Cac-bon-đích (CO2). Biết C=12, O=16.",
        "options": ["28 g/mol", "32 g/mol", "44 g/mol", "58 g/mol"],
        "answer": 2,
        "explanation": "Khối lượng mol của CO2 = 12 + (16 * 2) = 44 g/mol."
    },
    {
        "level": "Lớp 8 - Hóa học",
        "question": "Dãy chất nào sau đây chỉ gồm các Oxit bazơ?",
        "options": ["CaO, Na2O, CuO", "SO2, CO2, P2O5", "HCl, H2SO4, HNO3", "NaOH, KOH, Ca(OH)2"],
        "answer": 0,
        "explanation": "CaO, Na2O, CuO là các oxit bazơ (oxit của kim loại tương ứng với bazơ)."
    },
    {
        "level": "Lớp 9 - Hóa học",
        "question": "Chất nào sau đây làm quỳ tím hóa đỏ?",
        "options": ["Dung dịch NaOH", "Dung dịch NaCl", "Dung dịch HCl", "Nước cất"],
        "answer": 2,
        "explanation": "Dung dịch axit như HCl làm quỳ tím chuyển sang màu đỏ."
    },
    {
        "level": "Lớp 9 - Hóa học",
        "question": "Cho thanh sắt vào dung dịch muối nào sau đây sẽ xảy ra phản ứng hóa học (Sắt đẩy kim loại ra khỏi muối)?",
        "options": ["Dung dịch MgSO4", "Dung dịch ZnSO4", "Dung dịch CuSO4", "Dung dịch NaCl"],
        "answer": 2,
        "explanation": "Sắt đứng trước đồng (Cu) trong dãy hoạt động hóa học nên sắt đẩy được Cu ra khỏi dung dịch CuSO4."
    }
]

# Khởi tạo trạng thái game trong session_state của Streamlit
if "started" not in st.session_state:
    st.session_state.started = False
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected_choice" not in st.session_state:
    st.session_state.selected_choice = None

# Tiêu đề game
st.title("🧪 Thám Tử Hóa Học - THCS")
st.markdown("---")

# Màn hình bắt đầu
if not st.session_state.started:
    st.subheader("Chào mừng bạn đến với thử thách giải đố Hóa học từ Lớp 6 đến Lớp 9!")
    st.write("Hãy kiểm tra lại kiến thức nguyên tố, phản ứng và hiện tượng tự nhiên của bạn qua các câu hỏi thú vị.")
    if st.button("🚀 Bắt Đầu Khám Phá", type="primary"):
        st.session_state.started = True
        st.rerun()

else:
    # Kiểm tra nếu đã hoàn thành tất cả câu hỏi
    if st.session_state.current_q >= len(QUESTIONS):
        st.success("🎉 Chúc mừng bạn đã hoàn thành xuất sắc chuyến hành trình Thám Tử Hóa Học!")
        
        # Đánh giá kết quả
        final_score = st.session_state.score
        total_q = len(QUESTIONS)
        st.metric(label="Điểm số của bạn", value=f"{final_score} / {total_q}")
        
        if final_score == total_q:
            st.balloons()
            st.write("🌟 Xuất sắc! Bạn đích thực là một Chuyên gia Hóa học nhí tài ba!")
        elif final_score >= total_q / 2:
            st.write("👍 Khá lắm! Bạn nắm vững kiến thức cơ bản rất tốt.")
        else:
            st.write("💡 Cần cố gắng ôn tập thêm một chút về các hiện tượng và công thức hóa học nhé!")

        if st.button("🔄 Chơi Lại Từ Đầu"):
            st.session_state.started = False
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.selected_choice = None
            st.rerun()

    else:
        # Hiển thị câu hỏi hiện tại
        q_data = QUESTIONS[st.session_state.current_q]
        
        st.caption(f"Câu hỏi {st.session_state.current_q + 1} / {len(QUESTIONS)} | *{q_data['level']}*")
        st.subheader(q_data["question"])

        # Hiển thị các lựa chọn dạng Radio button
        choice = st.radio(
            "Chọn đáp án đúng nhất của bạn:",
            q_data["options"],
            key=f"q_{st.session_state.current_q}",
            index=st.session_state.selected_choice
        )

        col1, col2 = st.columns([1, 4])
        
        with col1:
            if not st.session_state.answered:
                if st.button("Xác Nhận", type="primary"):
                    # Lưu lại đáp án người dùng chọn
                    selected_index = q_data["options"].index(choice)
                    st.session_state.selected_choice = selected_index
                    st.session_state.answered = True
                    if selected_index == q_data["answer"]:
                        st.session_state.score += 1
                    st.rerun()
            else:
                if st.button("Câu Tiếp Theo"):
                    st.session_state.current_q += 1
                    st.session_state.answered = False
                    st.session_state.selected_choice = None
                    st.rerun()

        # Hiển thị kết quả đúng/sai và giải thích sau khi bấm xác nhận
        if st.session_state.answered:
            selected_index = q_data["options"].index(choice)
            correct_index = q_data["answer"]
            
            st.markdown("---")
            if selected_index == correct_index:
                st.success("✅ Chính xác! Làm rất tốt!")
            else:
                st.error(f"❌ Chưa chính xác. Đáp án đúng là: **{q_data['options'][correct_index]}**")
            
            st.info(f"💡 **Giải thích:** {q_data['explanation']}")
