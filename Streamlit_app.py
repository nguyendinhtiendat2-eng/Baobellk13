import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Thám Tử Hóa Học",
    page_icon="🧪",
    layout="centered"
)

# Thêm CSS tùy chỉnh giao diện phong cách Duolingo
st.markdown("""
<style>
    .stApp {
        background-color: #f7f7f7;
        font-family: 'Avenir', 'Feather', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
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
    .group-label {
        color: #afafaf;
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        margin-top: 20px;
        margin-bottom: 10px;
        letter-spacing: 0.8px;
    }
    .question-title {
        color: #3c3c3c;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Bộ câu hỏi mở rộng phong phú cho từng lớp
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
            "exp": "Đinh sắt bị gỉ sét tạo ra chất mới (sắt oxit), đây là hiện tượng hóa học."
        },
        {
            "q": "Trong các chất sau, đâu là chất tinh khiết?",
            "options": ["Nước khoáng", "Nước cất", "Không khí", "Sữa tươi"],
            "ans": 1,
            "exp": "Nước cất là chất tinh khiết (chỉ gồm các phân tử H2O), các chất còn lại là hỗn hợp."
        },
        {
            "q": "Nhiệt độ sôi của nước nguyên chất ở áp suất khí quyển tiêu chuẩn là bao nhiêu?",
            "options": ["50°C", "100°C", "0°C", "80°C"],
            "ans": 1,
            "exp": "Ở áp suất tiêu chuẩn, nước sôi ở nhiệt độ 100°C."
        },
        {
            "q": "Hỗn hợp nào sau đây có thể tách chất bằng phương pháp lọc?",
            "options": ["Muối ăn và nước", "Đường và nước", "Cát và nước", "Giấm ăn và nước"],
            "ans": 2,
            "exp": "Cát không tan trong nước, tạo thành hỗn hợp huyền phù nên có thể dùng giấy lọc để giữ cát lại."
        },
        {
            "q": "Quá trình chuyển đổi từ thể lỏng sang thể khí của chất được gọi là gì?",
            "options": ["Sự nóng chảy", "Sự đông đặc", "Sự bay hơi", "Sự ngưng tụ"],
            "ans": 2,
            "exp": "Sự bay hơi là quá trình chuyển từ thể lỏng sang thể khí."
        }
    ],
    "7": [
        {
            "q": "Ký hiệu hóa học của nguyên tố Natri là gì?",
            "options": ["Na", "N", "K", "Cu"],
            "ans": 0,
            "exp": "Natri có ký hiệu hóa học là Na (tên tiếng Latinh: Natrium)."
        },
        {
            "q": "Công thức hóa học của nước là gì?",
            "options": ["H2O2", "H2O", "HO2", "OH2"],
            "ans": 1,
            "exp": "Phân tử nước gồm 2 nguyên tử Hydro và 1 nguyên tử Oxi kết hợp lại (H2O)."
        },
        {
            "q": "Nguyên tố hóa học nào chiếm phần trăm khối lượng lớn nhất trong vỏ Trái Đất?",
            "options": ["Silic", "Sắt", "Oxi", "Nhôm"],
            "ans": 2,
            "exp": "Oxi là nguyên tố phổ biến nhất, chiếm khoảng 46,6% khối lượng vỏ Trái Đất."
        },
        {
            "q": "Hợp chất tạo bởi nguyên tố X (hóa trị III) với nhóm (SO4) (hóa trị II) có công thức hóa học là gì?",
            "options": ["XSO4", "X2(SO4)3", "X3(SO4)2", "X2SO4"],
            "ans": 1,
            "exp": "Theo quy tắc hóa trị: a x A = b x B => III x 2 = II x 3 => Công thức là X2(SO4)3."
        },
        {
            "q": "Phân tử khối của khí Cac-bon-đích (CO2) bằng bao nhiêu? (Biết C=12, O=16)",
            "options": ["28 đvc", "32 đvc", "44 đvc", "56 đvc"],
            "ans": 2,
            "exp": "Phân tử khối CO2 = 12 + (16 x 2) = 44 đvc."
        },
        {
            "q": "Hóa trị của nguyên tố Canxi (Ca) trong các hợp chất phổ biến là mấy?",
            "options": ["Hóa trị I", "Hóa trị II", "Hóa trị III", "Hóa trị IV"],
            "ans": 1,
            "exp": "Canxi (Ca) thuộc nhóm IIA nên luôn có hóa trị II trong các hợp chất."
        }
    ],
    "8": [
        {
            "q": "Công thức hóa học của Axit Sunfuric là gì?",
            "options": ["HCl", "H2SO4", "HNO3", "H3PO4"],
            "ans": 1,
            "exp": "Axit Sunfuric có công thức hóa học là H2SO4."
        },
        {
            "q": "Dãy chất nào sau đây chỉ gồm các Oxit bazơ?",
            "options": ["CaO, Na2O, CuO", "SO2, CO2, P2O5", "HCl, H2SO4, HNO3", "NaOH, KOH"],
            "ans": 0,
            "exp": "CaO, Na2O, CuO là các oxit bazơ cấu tạo từ kim loại liên kết với nguyên tử Oxi."
        },
        {
            "q": "Tính thể tích của 0,5 mol khí Hidro (ở đktc)?",
            "options": ["11,2 lít", "22,4 lít", "5,6 lít", "3,36 lít"],
            "ans": 0,
            "exp": "Ở đktc, thể tích chất khí = số mol x 22,4 = 0,5 x 22,4 = 11,2 lít."
        },
        {
            "q": "Hóa trị của nhóm (OH) trong hợp chất bazơ thường là mấy?",
            "options": ["Hóa trị I", "Hóa trị II", "Hóa trị III", "Hóa trị IV"],
            "ans": 0,
            "exp": "Nhóm Hydroxit (OH) luôn có hóa trị I."
        },
        {
            "q": "Để trung hòa hoàn toàn 100ml dung dịch NaOH cần dùng bao nhiêu ml dung dịch HCl có cùng nồng độ mol?",
            "options": ["50 ml", "100 ml", "200 ml", "300 ml"],
            "ans": 1,
            "exp": "Phương trình: NaOH + HCl -> NaCl + H2O (tỉ lệ mol 1:1, cùng nồng độ nên thể tích bằng nhau là 100ml)."
        },
        {
            "q": "Công thức hóa học của Khí đá (Hay còn gọi là Axetilen) là gì?",
            "options": ["CH4", "C2H4", "C2H2", "C6H6"],
            "ans": 2,
            "exp": "Axetilen có công thức hóa học là C2H2."
        },
        {
            "q": "Khối lượng mol của hợp chất Canxi Cacbonat (CaCO3) là bao nhiêu? (Biết Ca=40, C=12, O=16)",
            "options": ["84 g/mol", "100 g/mol", "106 g/mol", "112 g/mol"],
            "ans": 1,
            "exp": "Khối lượng mol CaCO3 = 40 + 12 + (16 x 3) = 100 g/mol."
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
            "q": "Cho thanh sắt vào dung dịch muối nào sau đây sẽ xảy ra phản ứng?",
            "options": ["MgSO4", "ZnSO4", "CuSO4", "NaCl"],
            "ans": 2,
            "exp": "Sắt đứng trước Đồng (Cu) trong dãy hoạt động hóa học nên đẩy được Cu ra khỏi dung dịch CuSO4."
        },
        {
            "q": "Công thức hóa học của đường Saccarozơ là gì?",
            "options": ["C6H12O6", "C12H22O11", "(C6H10O5)n", "CH3COOH"],
            "ans": 1,
            "exp": "Đường mía (Saccarozơ) có công thức hóa học là C12H22O11."
        },
        {
            "q": "Kim loại nào sau đây có thể tác dụng với dung dịch H2SO4 loãng tạo ra khí Hidro?",
            "options": ["Đồng (Cu)", "Bạc (Ag)", "Kẽm (Zn)", "Vàng (Au)"],
            "ans": 2,
            "exp": "Các kim loại đứng trước Hidro trong dãy hoạt động hóa học (như Zn, Fe, Al) mới tác dụng với axit loãng giải phóng khí H2."
        },
        {
            "q": "Chất nào sau đây thuộc loại phân bón kép?",
            "options": ["NH4NO3", "KNO3", "Ca(H2PO4)2", "(NH2)2CO"],
            "ans": 1,
            "exp": "KNO3 chứa cả nguyên tố dinh dưỡng N và K nên là phân bón kép."
        },
        {
            "q": "Dung dịch chất nào sau đây làm dung dịch phenolphtalein chuyển sang màu hồng?",
            "options": ["HCl", "NaCl", "NaOH", "H2SO4"],
            "ans": 2,
            "exp": "Dung dịch bazơ (như NaOH) làm phenolphtalein không màu chuyển sang màu hồng."
        },
        {
            "q": "Thủy tinh hữu cơ (Plexigias) được tổng hợp từ chất nào sau đây?",
            "options": ["Metyl metacrilat", "Etilen", "Vinyl clorua", "Stiren"],
            "ans": 0,
            "exp": "Thủy tinh hữu cơ được điều chế bằng phản ứng trùng hợp metyl metacrilat."
        }
    ]
}

# Khởi tạo session state
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

# MÀN HÌNH 1: CHỌN LỚP HỌC
if st.session_state.grade is None:
    st.markdown('<div class="question-title">🧪 Bạn muốn thử sức kiến thức Hóa học lớp mấy?</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="group-label">Tổng hợp THCS</div>', unsafe_allow_html=True)
    if st.button("🔴  Tất cả các lớp (6 - 9)"):
        st.session_state.grade = "ALL"
        st.rerun()

    st.markdown('<div class="group-label">Chọn theo từng cấp độ</div>', unsafe_allow_html=True)
    if st.button("🟣  Lớp 6 - Khoa học Tự nhiên"):
        st.session_state.grade = "6"
        st.rerun()
    if st.button("🔵  Lớp 7 - Khoa học Tự nhiên"):
        st.session_state.grade = "7"
        st.rerun()
    if st.button("🟢  Lớp 8 - Hóa học cơ bản & Công thức"):
        st.session_state.grade = "8"
        st.rerun()
    if st.button("🟡  Lớp 9 - Hóa học nâng cao & Phản ứng"):
        st.session_state.grade = "9"
        st.rerun()

# MÀN HÌNH 2: CHƠI GAME & GIẢI ĐỐ
else:
    # Lọc danh sách câu hỏi
    if st.session_state.grade == "ALL":
        current_list = []
        for g in ["6", "7", "8", "9"]:
            current_list.extend(QUESTIONS_BY_GRADE[g])
    else:
        current_list = QUESTIONS_BY_GRADE[st.session_state.grade]

    total_q = len(current_list)
    progress = (st.session_state.q_index + 1) / total_q if st.session_state.q_index < total_q else 1.0
    st.progress(progress)

    # Màn hình kết quả cuối cùng
    if st.session_state.q_index >= total_q:
        st.markdown('<div class="question-title">🎉 Hoàn thành xuất sắc bài thử thách!</div>', unsafe_allow_html=True)
        st.metric(label="Điểm số tổng kết", value=f"{st.session_state.score} / {total_q}")
        
        if st.session_state.score == total_q:
            st.balloons()
            st.success("🌟 Tuyệt đỉnh! Bạn là một bậc thầy Hóa học thực thụ!")
        elif st.session_state.score >= total_q / 2:
            st.success("👍 Rất tốt! Bạn nắm vững kiến thức nền tảng vững chắc.")
        else:
            st.warning("💡 Hãy xem lại lý thuyết công thức và luyện tập thêm nhé!")

        if st.button("🔄 Chọn lại cấp độ khác"):
            st.session_state.grade = None
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.user_choice = None
            st.rerun()

    # Màn hình câu hỏi đang chơi
    else:
        q_data = current_list[st.session_state.q_index]
        st.markdown(f'<div class="question-title">Câu {st.session_state.q_index + 1}: {q_data["q"]}</div>', unsafe_allow_html=True)

        # Hiển thị nút lựa chọn
        for idx, option in enumerate(q_data["options"]):
            if st.button(f"{option}", key=f"opt_{idx}"):
                if not st.session_state.answered:
                    st.session_state.user_choice = idx
                    st.session_state.answered = True
                    if idx == q_data["ans"]:
                        st.session_state.score += 1

        # Hiển thị hiệu ứng và đáp án sau khi người dùng chọn
        if st.session_state.answered:
            st.markdown("---")
            correct_idx = q_data["ans"]
            correct_text = q_data["options"][correct_idx]
            
            if st.session_state.user_choice == correct_idx:
                st.balloons()  # Hiệu ứng pháo hoa ăn mừng khi trả lời đúng
                st.success("✅ Chính xác! Bạn thật xuất sắc!")
            else:
                st.error(f"❌ Rất tiếc, chưa chính xác!\n\n👉 **Đáp án đúng là:** **{correct_text}**")
            
            st.info(f"💡 **Giải thích chi tiết:** {q_data['exp']}")

            if st.button("Tiếp theo ➔", type="primary"):
                st.session_state.q_index += 1
                st.session_state.answered = False
                st.session_state.user_choice = None
                st.rerun()
