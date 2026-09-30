import streamlit as st
import random
import time

# --- Cấu hình trang Streamlit ---
st.set_page_config(
    page_title="Game Đua Vịt Chọn Người Bốc Thăm",
    page_icon="🦆",
    layout="wide"
)

# --- Thêm CSS tùy chỉnh cho sinh động ---
st.markdown("""
<style>
    .stApp {
        background-color: #f0f9ff;
    }
    .track-container {
        background-color: #e2e8f0;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    .duck-row {
        background-color: white;
        border-radius: 8px;
        padding: 8px 15px;
        margin: 8px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
    }
    .winner-box {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: #333;
        font-weight: bold;
        font-size: 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        animation: pulse 1.5s infinite;
    }
</style>
""", unsafe_allow_html=True)

# --- Danh sách màu sắc & Biểu tượng vịt ---
DUCK-EMOJIS = ["🦆", "🐤", "🐥", "🦅", "🦉", "🦩", "🦜", "🦚"]
COLORS = ["#FF5733", "#33FF57", "#3357FF", "#F39C12", "#9B59B6", "#1ABC9C", "#E91E63", "#34495E"]

# --- Tiêu đề ứng dụng ---
st.title("🦆 Game Đua Vịt - Bốc Thăm May Mắn")
st.caption("Nhập danh sách người chơi, mỗi người sẽ chọn một chú vịt để bắt đầu cuộc đua!")

# --- Sidebar: Cài đặt trò chơi ---
with st.sidebar:
    st.header("⚙️ Cài đặt cuộc đua")
    
    # Mẫu danh sách mặc định
    default_names = "Nguyễn Văn A\nTrần Thị B\nLê Văn C\nPhạm Thị D\nHoàng Văn E"
    
    input_text = st.text_area(
        "Nhập danh sách tên người chơi (mỗi dòng 1 tên):",
        value=default_names,
        height=200
    )
    
    # Xử lý danh sách tên
    player_names = [name.strip() for name in input_text.split("\n") if name.strip()]
    
    track_length = st.slider("Độ dài đường đua (bước):", min_value=30, max_value=100, value=50, step=10)
    race_speed = st.slider("Tốc độ đua (giây/bước):", min_value=0.01, max_value=0.2, value=0.05, step=0.01)

    start_button = st.button("🏁 Bắt đầu cuộc đua!", type="primary", use_container_width=True)

# --- Khu vực Đường Đua ---
st.subheader("🏁 Đường Đua Vịt")

if len(player_names) < 2:
    st.warning("⚠️ Vui lòng nhập ít nhất 2 người chơi để bắt đầu cuộc đua!")
else:
    # Gán màu và icon ngẫu nhiên cho từng con vịt
    ducks = []
    for i, name in enumerate(player_names):
        ducks.append({
            "id": i,
            "name": name,
            "icon": DUCK-EMOJIS[i % len(DUCK-EMOJIS)],
            "color": COLORS[i % len(COLORS)],
            "position": 0
        })

    # Khởi tạo container hiển thị đường đua
    race_placeholder = st.empty()

    def render_race(ducks_data):
        """Hàm vẽ giao diện đường đua theo vị trí hiện tại của các vịt"""
        html_content = "<div class='track-container'>"
        for duck in ducks_data:
            # Tính phần trăm tiến độ
            progress_percent = min(100, int((duck["position"] / track_length) * 100))
            
            html_content += f"""
            <div style='margin-bottom: 12px;'>
                <div style='display: flex; justify-content: space-between; font-weight: bold; font-size: 14px; margin-bottom: 3px;'>
                    <span style='color: {duck["color"]};'>{duck["icon"]} {duck["name"]}</span>
                    <span>{duck["position"]}/{track_length}</span>
                </div>
                <div style='background-color: #cbd5e1; border-radius: 10px; height: 24px; width: 100%; position: relative; overflow: hidden;'>
                    <div style='background-color: {duck["color"]}; width: {progress_percent}%; height: 100%; border-radius: 10px; transition: width 0.1s ease-in-out;'></div>
                    <span style='position: absolute; left: calc({progress_percent}% - 20px); top: -2px; font-size: 18px;'>{duck["icon"]}</span>
                </div>
            </div>
            """
        html_content += "</div>"
        return html_content

    # Hiển thị đường đua ban đầu ở mốc 0
    race_placeholder.markdown(render_race(ducks), unsafe_allow_html=True)

    # --- Xử lý Khi Bấm Bắt Đầu Đua ---
    if start_button:
        winner = None
        st.toast("🚀 Cuộc đua đã bắt đầu!", icon="🏁")

        # Vòng lặp đua
        while not winner:
            for duck in ducks:
                # Mỗi chú vịt tiến ngẫu nhiên từ 1 đến 3 bước
                step = random.randint(1, 3)
                duck["position"] += step
                
                # Kiểm tra xem có ai về đích chưa
                if duck["position"] >= track_length:
                    duck["position"] = track_length
                    winner = duck
                    break
            
            # Cập nhật lại giao diện đường đua
            race_placeholder.markdown(render_race(ducks), unsafe_allow_html=True)
            time.sleep(race_speed)

        # Hiệu ứng ăn mừng khi có người chiến thắng
        st.balloons()
        st.snow()
        
        # Hiển thị kết quả người thắng cuộc
        st.markdown(f"""
        <div class='winner-box'>
            🎉 CHÚC MỪNG CHIẾN THẮNG! 🎉<br>
            <span style='font-size: 36px; color: #d97706;'>{winner["icon"]} {winner["name"]}</span><br>
            đã về đích đầu tiên! 🏆
        </div>
        """, unsafe_allow_html=True)
          
