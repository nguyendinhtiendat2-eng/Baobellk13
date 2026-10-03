import random
import time
import pandas as pd
import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Thuyền Trưởng Săn Cá - Câu Cá Giải Trí",
    page_icon="🎣",
    layout="wide",
)

# Khởi tạo trạng thái game (Session State)
if "gold" not in st.session_state:
    st.session_state.gold = 100
if "energy" not in st.session_state:
    st.session_state.energy = 100
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "rods" not in st.session_state:
    st.session_state.rods = {"Cần tre cơ bản": {"power": 1, "owned": True}}
if "current_rod" not in st.session_state:
    st.session_state.current_rod = "Cần tre cơ bản"
if "stats" not in st.session_state:
    st.session_state.stats = {"total_caught": 0, "total_sold": 0}

# Định nghĩa dữ liệu cá theo khu vực
AREAS = {
    "Ao Làng Bình Yên": {
        "cost": 5,
        "fish": [
            {"name": "Cá Rô Phi", "rarity": "Phổ biến", "value": 10},
            {"name": "Cá Chép Nhỏ", "rarity": "Phổ biến", "value": 15},
            {"name": "Cá Trê Vàng", "rarity": "Hiếm", "value": 40},
            {"name": "Rác Nhựa", "rarity": "Đồ bỏ đi", "value": 1},
        ],
    },
    "Sông Sâu Chảy Xiết": {
        "cost": 15,
        "fish": [
            {"name": "Cá Hồi", "rarity": "Hiếm", "value": 60},
            {"name": "Cá Nheo Khổng Lồ", "rarity": "Cực hiếm", "value": 150},
            {"name": "Cá Trắm Cỏ", "rarity": "Phổ biến", "value": 30},
            {"name": "Chiếc Giày Cũ", "rarity": "Đồ bỏ đi", "value": 2},
        ],
    },
    "Đại Dương Sâu Thẳm": {
        "cost": 40,
        "fish": [
            {"name": "Cá Mập Con", "rarity": "Cực hiếm", "value": 300},
            {"name": "Cá Ngừ Đại Dương", "rarity": "Hiếm", "value": 180},
            {"name": "Mực Khổng Lồ", "rarity": "Huyền thoại", "value": 600},
            {"name": "Kho Báu Cổ", "rarity": "Huyền thoại", "value": 1000},
        ],
    },
}

# Định nghĩa các loại cần câu trong cửa hàng
RODS_SHOP = {
    "Cần Sợi Thủy Tinh": {"power": 2, "cost": 200, "desc": "Tăng tỷ lệ câu cá hiếm."},
    "Cần Carbon Chuyên Dụng": {
        "power": 3,
        "cost": 600,
        "desc": "Cần câu cực mạnh cho các vùng nước sâu."},
    "Cần Thần Thánh": {
        "power": 5,
        "cost": 2000,
        "desc": "Dễ dàng săn các loài cá huyền thoại."},
}

# Giao diện chính
st.title("🎣 Thuyền Trưởng Săn Cá - Streamlit Edition")
st.markdown(
    "Chào mừng bạn đến với chuyến phiêu lưu câu cá! Hãy chọn khu vực, câu cá, thu thập các loài vật quý hiếm và nâng cấp trang bị."
)

# Thanh trạng thái (Sidebar)
st.sidebar.header("📊 Thông Tin Cần Thủ")
st.sidebar.metric(label="💰 Vàng (Gold)", value=f"{st.session_state.gold} G")
st.sidebar.metric(
    label="⚡ Thể Lực (Energy)", value=f"{st.session_state.energy}/100"
)

if st.sidebar.button("Năng lượng thần tốc (Hồi Full +50G)"):
    if st.session_state.gold >= 50:
        st.session_state.gold -= 50
        st.session_state.energy = 100
        st.sidebar.success("Đã hồi đầy thể lực!")
    else:
        st.sidebar.error("Không đủ vàng để mua thể lực!")

st.sidebar.markdown("---")
st.sidebar.write(
    f"🏆 **Tổng cá đã câu:** {st.session_state.stats['total_caught']}"
)

# Các tab chức năng
tab1, tab2, tab3, tab4 = st.tabs(
    ["🌊 Khu Vực Câu Cá", "🎒 Túi Đồ & Bán Cá", "🛒 Cửa Hàng Cần Câu", "📜 Hướng Dẫn"]
)

with tab1:
    st.subheader("Chọn Khu Vực Thả Câu")

    selected_area = st.selectbox(
        "Chọn vùng nước bạn muốn đến:", list(AREAS.keys())
    )
    area_info = AREAS[selected_area]

    col1, col2 = st.columns([2, 1])
    with col1:
        st.info(
            f"**Phí thả câu:** {area_info['cost']} Thể lực | **Khu vực:** {selected_area}"
        )

        # Hiển thị danh sách cá có thể xuất hiện
        st.markdown("##### 🐟 Các loài cá có thể xuất hiện tại đây:")
        fish_preview = pd.DataFrame(area_info["fish"])
        st.dataframe(fish_preview, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("#### Hành động")
        current_power = st.session_state.rods[st.session_state.current_rod][
            "power"
        ]
        st.write(
            f"🎣 **Đang dùng:** {st.session_state.current_rod} (Sức mạnh: {current_power})"
        )

        if st.button("🎣 THẢ CÂU NGAY!", type="primary", use_container_width=True):
            if st.session_state.energy < area_info["cost"]:
                st.warning("Bạn đã hết thể lực! Hãy nghỉ ngơi hoặc mua thêm.")
            else:
                st.session_state.energy -= area_info["cost"]

                # Hiệu ứng giả lập đang câu
                with st.spinner("Đang thả mồi chờ cá cắn câu... 🌊"):
                    time.sleep(1.2)

                # Thuật toán bắt cá có tính đến sức mạnh cần câu
                fish_pool = area_info["fish"]
                # Cần câu xịn tăng tỷ lệ trúng cá hiếm
                weights = []
                for f in fish_pool:
                    if f["rarity"] == "Phổ biến" or f["rarity"] == "Đồ bỏ đi":
                        weights.append(50)
                    elif f["rarity"] == "Hiếm":
                        weights.append(20 * current_power)
                    elif f["rarity"] == "Cực hiếm":
                        weights.append(10 * current_power)
                    else:  # Huyền thoại
                        weights.append(2 * current_power)

                caught_fish = random.choices(fish_pool, weights=weights, k=1)[0]

                # Lưu vào túi đồ
                st.session_state.inventory.append(caught_fish)
                st.session_state.stats["total_caught"] += 1

                # Hiển thị kết quả bắt được
                st.success(f"🎉 Chúc mừng! Bạn đã câu được: **{caught_fish['name']}**!")
                st.markdown(
                    f"- **Độ hiếm:** {caught_fish['rarity']} \n- **Giá trị:** {caught_fish['value']} G"
                )

with tab2:
    st.subheader("🎒 Kho Chứa & Bán Cá")

    if not st.session_state.inventory:
        st.info("Túi đồ của bạn đang trống. Hãy đi câu cá ngay thôi!")
    else:
        # Thống kê nhanh túi đồ
        inv_df = pd.DataFrame(st.session_state.inventory)
        st.dataframe(inv_df, use_container_width=True, hide_index=True)

        total_value = sum([f["value"] for f in st.session_state.inventory])
        st.metric(
            label="💵 Tổng giá trị cá trong túi", value=f"{total_value} G"
        )

        col_sell1, col_sell2 = st.columns(2)
        with col_sell1:
            if st.button(
                "💰 Bán Tất Cả Cá", type="primary", use_container_width=True
            ):
                st.session_state.gold += total_value
                st.session_state.stats["total_sold"] += len(
                    st.session_state.inventory
                )
                st.session_state.inventory = []
                st.success(
                    f"Đã bán toàn bộ cá và thu về **{total_value} G**!"
                )
                st.rerun()

        with col_sell2:
            if st.button("🗑️ Đổ / Giải phóng túi đồ", use_container_width=True):
                st.session_state.inventory = []
                st.warning("Đã làm trống túi đồ.")
                st.rerun()

with tab3:
    st.subheader("🛒 Cửa Hàng Trang Bị")
    st.markdown("Nâng cấp cần câu để tăng tỷ lệ bắt các loài cá quý hiếm hơn!")

    for rod_name, info in RODS_SHOP.items():
        col_r1, col_r2, col_r3 = st.columns([2, 2, 1])

        with col_r1:
            st.markdown(f"### {rod_name}")
            st.write(info["desc"])
            st.text(
                f"Sức mạnh: +{info['power']} | Giá: {info['cost']} Vàng"
            )

        with col_r2:
            is_owned = rod_name in st.session_state.rods
            is_equipped = st.session_state.current_rod == rod_name

            if is_equipped:
                st.success("Đang sử dụng")
            elif is_owned:
                if st.button(f"Trang bị {rod_name}", key=f"eq_{rod_name}"):
                    st.session_state.current_rod = rod_name
                    st.success(f"Đã chuyển sang dùng {rod_name}!")
                    st.rerun()
            else:
                if st.button(f"Mua {rod_name}", key=f"buy_{rod_name}"):
                    if st.session_state.gold >= info["cost"]:
                        st.session_state.gold -= info["cost"]
                        st.session_state.rods[rod_name] = {
                            "power": info["power"],
                            "owned": True,
                        }
                        st.session_state.current_rod = rod_name
                        st.success(
                            f"Mua thành công {rod_name} và tự động trang bị!"
                        )
                        st.rerun()
                    else:
                        st.error("Bạn không đủ vàng để mua cần này!")
        st.markdown("---")

with tab4:
    st.subheader("📜 Luật Chơi & Hướng Dẫn")
    st.markdown("""
    1. **Chọn khu vực câu:** Mỗi khu vực sẽ tiêu tốn thể lực khác nhau và có các loài cá với độ hiếm, giá trị khác nhau.
    2. **Thả câu:** Nhấn nút thả câu và chờ đợi kết quả ngẫu nhiên. Cần câu có sức mạnh cao hơn sẽ giúp bạn dễ gặp cá hiếm hoặc cá huyền thoại.
    3. **Quản lý năng lượng:** Thể lực sẽ giảm dần mỗi lần câu. Bạn có thể mua hồi thể lực ở thanh bên trái (Sidebar).
    4. **Bán cá kiếm tiền:** Mang cá bắt được sang tab **Túi Đồ & Bán Cá** để đổi lấy Vàng (`G`), sau đó dùng vàng để mua các loại cần câu xịn hơn trong **Cửa Hàng**.
    """)
