import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Thám Tử Hóa Học",
    page_icon="🧪",
    layout="centered"
)

# Thêm CSS tùy chỉnh giao diện giống Duolingo
st.markdown("""
<style>
    /* Nền tổng thể và font chữ */
    .stApp {
        background-color: #f7f7f7;
        font-family: 'Avenir', 'Feather', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    /* Container chính bo góc kiểu ứng dụng di động */
    .main-card {
        background-color: white;
        border-radius: 20px;
        padding: 30px 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        max-width: 480px;
        margin: 0 auto;
    }

    /* Nút chọn kiểu Duolingo */
    div.stButton > button {
        width: 100%;
        border-radius: 16px !important;
        border: 2px solid #e5e5e5 !important;
        border-bottom: 5px solid #e5e5e5 !important;
        background-color: #ffffff !important;
        color: #4b4b4b !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        padding: 14px 20px !important;
        text-align: left !important;
        margin-bottom: 8px !important;
        transition: all 0.1s ease !important;
    }

    div.stButton > button:hover {
        background-color: #f7f7f7 !important;
        border-color: #cecece !important;
        border-bottom-color: #cecece !important;
    }

    div.stButton > button:active {
        border-bottom-width: 2px !important;
        transform: translateY(3px);
    }

    /* Tiêu đề nhóm (ví dụ: For Students / Cấp học) */
    .group-label {
        color: #afafaf;
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        margin-top: 20px;
        margin-bottom: 10px;
        letter-spacing: 0.8px;
    }

    /* Header câu hỏi */
    .question-title {
        color: #3c3c3c;
        font-size: 24px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 24px;
    }
</style>
""", unsafe_allow_html=True)

# Bộ câu hỏi chia theo Lớp (6, 7, 8, 9)
QUESTIONS_BY_GRADE = {
    "6": [
        {
            "q": "Khí nào chiếm thể tích lớn nhất trong không khí (khoảng 78%)?",
            "options": ["Khí Ô-xi", "Khí Nitơ", "Khí Cac-bon-đích", "Hơi nước"],
            "ans": 1,
            "exp": "Không khí chứa khoảng 78% khí Nitơ, 21% khí Ô-xi và 1% các khí khác."
        },
        {
            "q": "Hiện tượng nào sau đây là hiện tượng hóa học?",
            "options": ["Đường hòa tan vào nước", "Đinh sắt bị gỉ sét", "Nước đá tan chảy", "Dây sắt bị uốn cong"],
            "ans": 1,
            "exp": "Đinh sắt bị gỉ sét biến đổi thành chất mới (sắt oxit), đây là hiện tượng hóa học."
        }
    ],
    "7": [
        {
            "q": "Ký hiệu hóa học của nguyên tố Natri là gì?",
            "options": ["Na", "N", "K", "Cu"],
            "ans": 0,
            "exp": "Natri có ký hiệu hóa học là Na."
        },
        {
            "q": "Công thức hóa học của nước là gì?",
            "options": ["H2O2", "H2O", "HO2", "OH2"],
            "ans": 1,
            "exp": "Phân tử nước gồm 2 nguyên tử Hydro và 1 nguyên tử Oxi kết hợp lại."
        }
    ],
    "8": [
        {
            "q": "Khối lượng mol của khí CO2 (C=12, O=16) là bao nhiêu?",
            "options": ["28 g/mol", "32 g/mol", "44 g/mol", "58 g/mol"],
            "ans": 2,
            "exp": "Khối lượng mol CO2 = 12 + (16 * 2) = 44 g/mol."
        },
        {
            "q": "Dãy chất nào sau đây chỉ gồm các Oxit bazơ?",
            "options": ["CaO, Na2O, CuO", "SO2, CO2, P2O5", "HCl, H2SO4, HNO3", "NaOH, KOH"],
            "ans": 0,
            "exp": "CaO, Na2O, CuO là các oxit bazơ cấu tạo từ kim loại và oxi."
        }
    ],
    "9": [
        {
            "q": "Dung dịch nào sau đây làm quỳ tím hóa đỏ?",
            "options": ["Dung dịch NaOH", "Dung dịch NaCl", "Dung dịch HCl", "Nước cất"],
            "ans": 2,
            "exp": "Dung dịch axit như HCl làm quỳ tím hóa đỏ."
        },
        {
            "q": "Cho thanh sắt vào dung dịch nào sau đây sẽ xảy ra phản ứng?",
            "options": ["MgSO4", "ZnSO4", "CuSO4", "NaCl"],
            "ans": 2,
            "exp": "Sắt đứng trước Đồng (Cu) trong dãy hoạt động hóa học nên đẩy được Cu ra khỏi CuSO4."
        }
    ]
}

# Khởi tạo trạng thái ứng dụng
if "grade" not in st.session_state:
    st.session_state.grade = None
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "user_choice" not in st.session_state:
    st.session_state.user_choice = None

# MAN HINH 1: CHỌN LỚP HỌC (Giao diện giống ảnh thiết kế)
if st.session_state.grade is None:
    st.markdown('<div class="question-title">Bạn muốn thử sức kiến thức lớp mấy?</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="group-label">Tổng hợp THCS</div>', unsafe_allow_html=True)
    if st.button("🔴  Tất cả các lớp (6 - 9)"):
        st.session_state.grade = "ALL"
        st.rerun()

    st.markdown('<div class="group-label">Chọn theo từng lớp</div>', unsafe_allow_html=True)
    
    if st.button("🟣  Lớp 6 - Khoa học Tự nhiên"):
        st.session_state.grade = "6"
        st.rerun()
        
    if st.button("🔵  Lớp 7 - Khoa học Tự nhiên"):
        st.session_state.grade = "7"
        st.rerun()
        
    if st.button("🟢  Lớp 8 - Hóa học cơ bản"):
        st.session_state.grade = "8"
        st.rerun()
        
    if st.button("🟡  Lớp 9 - Hóa học nâng cao"):
        st.session_state.grade = "9"
        st.rerun()

# MÀN HÌNH 2: CHƠI GAME & GIẢI ĐỐ
else:
    # Lấy danh sách câu hỏi dựa theo lớp chọn
    if st.session_state.grade == "ALL":
        current_list = []
        for g in ["6", "7", "8", "9"]:
            current_list.extend(QUESTIONS_BY_GRADE[g])
    else:
        current_list = QUESTIONS_BY_GRADE[st.session_state.grade]

    total_q = len(current_list)

    # Thanh tiến trình (Progress Bar)
    progress = (st.session_state.q_index + 1) / total_q if st.session_state.q_index < total_q else 1.0
    st.progress(progress)

    # Màn hình kết thúc
    if st.session_state.q_index >= total_q:
        st.markdown('<div class="question-title">🎉 Hoàn thành bài thi!</div>', unsafe_allow_html=True)
        st.metric(label="Điểm số của bạn", value=f"{st.session_state.score} / {total_q}")
        
        if st.session_state.score == total_q:
            st.balloons()
            st.success("Xuất sắc! Bạn đã trả lời đúng tất cả các câu hỏi!")
        else:
            st.info("Hãy tiếp tục luyện tập để đạt điểm tối đa nhé!")

        if st.button("🔄 Chọn lại lớp học"):
            st.session_state.grade = None
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.user_choice = None
            st.rerun()

    # Màn hình hiển thị câu hỏi
    else:
        q_data = current_list[st.session_state.q_index]
        st.markdown(f'<div class="question-title">{q_data["q"]}</div>', unsafe_allow_html=True)

        # Hiển thị các phương án dưới dạng nút bấm phong cách Duolingo
        for idx, option in enumerate(q_data["options"]):
            if st.button(f"{option}", key=f"opt_{idx}"):
                if not st.session_state.answered:
                    st.session_state.user_choice = idx
                    st.session_state.answered = True
                    if idx == q_data["ans"]:
                        st.session_state.score += 1

        # Hiển thị kết quả đúng/sai sau khi chọn
        if st.session_state.answered:
            st.markdown("---")
            if st.session_state.user_choice == q_data["ans"]:
                st.success("✅ Chính xác!")
            else:
                correct_ans_text = q_data["options"][q_data["ans"]]
                st.error(f"❌ Chưa đúng! Đáp án đúng là: **{correct_ans_text}**")
            
            st.info(f"💡 **Giải thích:** {q_data['exp']}")

            if st.button("Tiếp theo ➔", type="primary"):
                st.session_state.q_index += 1
                st.session_state.answered = False
                st.session_state.user_choice = None
                st.rerun()
  
