import random
import time
import pandas as pd
import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Hành Trình Câu Cá Đại Dương", page_icon="🎣", layout="wide"
)

# Khởi tạo trạng thái game (Session State)
if "gold" not in st.session_state:
    st.session_state.gold = 150
if "energy" not in st.session_state:
    st.session_state.energy = 100
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "rods" not in st.session_state:
    st.session_state.rods = {"Cần tre cơ bản": {"power": 1, "owned": True}}
if "current_rod" not in st.session_state:
    st.session_state.current_rod = "Cần tre cơ bản"
if "character_name" not in st.session_state:
    st.session_state.character_name = "Cần Thủ Tập Sự"
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []  # Lưu danh sách cá khủng từng câu được

# Dữ liệu Bản đồ & Khu vực câu cá
MAP_AREAS = {
    "🌿 Ao Làng Thanh Bình": {
        "cost": 5,
        "desc": "Vùng nước nông, yên ả. Thích hợp cho người mới bắt đầu.",
        "icon": "🏡",
        "fish": [
            {
                "name": "Cá Rô Phi",
                "rarity": "Phổ biến",
                "value": 10,
                "emoji": "🐟",
            },
            {
                "name": "Cá Chép Nhỏ",
                "rarity": "Phổ biến",
                "value": 15,
                "emoji": "🐠",
            },
            {
                "name": "Cá Trê Vàng",
                "rarity": "Hiếm",
                "value": 45,
                "emoji": "🐡",
            },
            {
                "name": "Rác Nhựa",
                "rarity": "Đồ bỏ đi",
                "value": 1,
                "emoji": "🗑️",
            },
        ],
    },
    "🌊 Sông Sâu Chảy Xiết": {
        "cost": 15,
        "desc": "Dòng nước mạnh chứa nhiều loài cá lớn và có giá trị cao.",
        "icon": "🛶",
        "fish": [
            {
                "name": "Cá Hồi Hoang Dã",
                "rarity": "Hiếm",
                "value": 70,
                "emoji": "🦈",
            },
            {
                "name": "Cá Nheo Khổng Lồ",
                "rarity": "Cực hiếm",
                "value": 160,
                "emoji": "🐳",
            },
            {
                "name": "Cá Trắm Cỏ",
                "rarity": "Phổ biến",
                "value": 35,
                "emoji": "🐟",
            },
            {
                "name": "Chiếc Giày Cũ",
                "rarity": "Đồ bỏ đi",
                "value": 2,
                "emoji": "👞",
            },
        ],
    },
    "🌀 Đại Dương Huyền Ảo": {
        "cost": 40,
        "desc": "Vùng biển sâu thẳm ẩn chứa những sinh vật huyền thoại và kho báu quý giá.",
        "icon": "⛵",
        "fish": [
            {
                "name": "Cá Mập Trắng",
                "rarity": "Cực hiếm",
                "value": 320,
                "emoji": "🦈",
            },
            {
                "name": "Cá Ngừ Vây Xanh",
                "rarity": "Hiếm",
                "value": 190,
                "emoji": "🐟",
            },
            {
                "name": "Mực Khổng Lồ Kraken",
                "rarity": "Huyền thoại",
                "value": 650,
                "emoji": "🦑",
            },
            {
                "name": "Hòm Kho Báu Cổ",
                "rarity": "Huyền thoại",
                "value": 1200,
                "emoji": "💰",
            },
        ],
    },
}

# Cửa hàng cần câu
RODS_SHOP = {
    "Cần Sợi Thủy Tinh": {
        "power": 2,
        "cost": 250,
        "desc": "Tăng tỷ lệ gặp cá hiếm.",
    },
    "Cần Carbon Chuyên Dụng": {
        "power": 3,
        "cost": 700,
        "desc": "Thích hợp cho các dòng sông lớn.",
    },
    "Cần Thần Thánh Poseidon": {
        "power": 5,
        "cost": 2200,
        "desc": "Dễ dàng câu được các sinh vật huyền thoại.",
    },
}

# --- Sidebar: Thông tin cá nhân & Nhân vật ---
st.sidebar.header("🧑‍💻 Thông Tin Cần Thủ")
new_name = st.sidebar.text_input(
    "Tên của bạn:", value=st.session_state.character_name
)
if new_name:
    st.session_state.character_name = new_name

st.sidebar.markdown(f"**Cần thủ:** 🤠 {st.session_state.character_name}")
st.sidebar.metric(label="💰 Vàng (Gold)", value=f"{st.session_state.gold} G")
st.sidebar.metric(
    label="⚡ Thể Lực", value=f"{st.session_state.energy}/100 ⚡"
)

if st.sidebar.button("Nạp Nhanh Thể Lực (Giá: 40 G)"):
    if st.session_state.gold >= 40:
        st.session_state.gold -= 40
        st.session_state.energy = 100
        st.sidebar.success("Đã hồi phục 100% thể lực!")
    else:
        st.sidebar.error("Không đủ vàng!")

st.sidebar.markdown("---")
current_rod_info = st.session_state.rods[st.session_state.current_rod]
st.sidebar.write(f"🎣 **Cần đang dùng:** {st.session_state.current_rod}")
st.sidebar.write(f"⚡ **Sức mạnh câu:** +{current_rod_info['power']}")

# Giao diện chính
st.title("🎣 Thế Giới Câu Cá: Hành Trình Chinh Phục Đại Dương")
st.markdown(
    "Chọn bản đồ thả câu, tung cần bắt những loài cá độc đáo, thu thập chiến tích và ghi danh lên Bảng Vàng danh dự!"
)

# Các tab chức năng chính
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🗺️ Bản Đồ & Câu Cá",
        "🎒 Kho Đồ & Bán Cá",
        "🛒 Cửa Hàng Trang Bị",
        "🏆 Bảng Vanh Danh Tên Tuổi",
    ]
)

with tab1:
    st.subheader("🗺️ Chọn Bản Đồ Khám Phá")

    # Hiển thị Bản đồ dưới dạng các thẻ (Columns)
    cols = st.columns(len(MAP_AREAS))
    selected_map_name = None

    for i, (area_name, info) in enumerate(MAP_AREAS.items()):
        with cols[i]:
            st.markdown(
                f"### {info['icon']} {area_name.split(' ', 1)[1] if ' ' in area_name else area_name}"
            )
            st.write(info["desc"])
            st.text(f"Phí: {info['cost']} Thể lực ⚡")

            if st.button(
                f"Đến vùng này", key=f"map_{i}", use_container_width=True
            ):
                st.session_state.selected_area = area_name

    # Đảm bảo có mặc định bản đồ đầu tiên
    if "selected_area" not in st.session_state:
        st.session_state.selected_area = list(MAP_AREAS.keys())[0]

    active_area = st.session_state.selected_area
    area_data = MAP_AREAS[active_area]

    st.markdown("---")
    st.markdown(
        f"### Vùng nước hiện tại: {active_area} {area_data['icon']}"
    )

    col_view1, col_view2 = st.columns([1.2, 1])

    with col_view1:
        st.markdown("#### 🐟 Các loài sinh vật tại đây:")
        fish_df = pd.DataFrame(area_data["fish"])
        # Hiển thị trực quan có icon
        for idx, row in fish_df.iterrows():
            st.write(
                f"{row['emoji']} **{row['name']}** — *{row['rarity']}* (Giá trị: **{row['value']} G**)"
            )

    with col_view2:
        st.markdown(
            "#### 🧍 Khu vực Thả Câu của Cần Thủ"
        )
        st.info(
            f"**Cần thủ:** {st.session_state.character_name}\n\n**Cần câu:** {st.session_state.current_rod}"
        )

        if st.button("🎣 THẢ CÂU NGAY!", type="primary", use_container_width=True):
            if st.session_state.energy < area_data["cost"]:
                st.warning(
                    "Thể lực đã cạn kiệt! Hãy nạp thể lực ở thanh bên trái."
                )
            else:
                st.session_state.energy -= area_data["cost"]

                with st.spinner(
                    f"{st.session_state.character_name} đang kiên nhẫn chờ cá cắn câu... 🌊"
                ):
                    time.sleep(1.2)

                # Thuật toán bắt cá theo hệ số cần câu
                power = current_rod_info["power"]
                fish_pool = area_data["fish"]
                weights = []
                for f in fish_pool:
                    if f["rarity"] in ["Phổ biến", "Đồ bỏ đi"]:
                        weights.append(50)
                    elif f["rarity"] == "Hiếm":
                        weights.append(20 * power)
                    elif f["rarity"] == "Cực hiếm":
                        weights.append(10 * power)
                    else:  # Huyền thoại
                        weights.append(3 * power)

                caught = random.choices(fish_pool, weights=weights, k=1)[0]

                # Lưu vào kho
                st.session_state.inventory.append(caught)

                # Nếu là cá hiếm hoặc huyền thoại, tự động ghi danh vào Bảng Vanh Danh
                if caught["rarity"] in ["Cực hiếm", "Huyền thoại"]:
                    st.session_state.leaderboard.append({
                        "name": st.session_state.character_name,
                        "fish": f"{caught['emoji']} {caught['name']}",
                        "rarity": caught["rarity"],
                        "area": active_area,
                    })

                # Giao diện thông báo kết quả bắt được
                st.success(
                    f"🎉 {st.session_state.character_name} đã câu được **{caught['emoji']} {caught['name']}**!"
                )
                st.markdown(
                    f"- **Độ hiếm:** {caught['rarity']}\n- **Giá trị:** {caught['value']} G"
                )

with tab2:
    st.subheader("🎒 Kho Đồ Cá Nhân & Chợ Bán Cá")

    if not st.session_state.inventory:
        st.info(
            "Túi đồ của bạn đang trống. Hãy ra bản đồ thả câu kiếm cá nhé!"
        )
    else:
        inv_list = []
        for idx, item in enumerate(st.session_state.inventory):
            inv_list.append({
                "STT": idx + 1,
                "Loài vật": f"{item['emoji']} {item['name']}",
                "Độ hiếm": item["rarity"],
                "Giá trị (G)": item["value"],
            })

        st.dataframe(
            pd.DataFrame(inv_list), use_container_width=True, hide_index=True
        )

        total_val = sum([f["value"] for f in st.session_state.inventory])
        st.metric(
            label="💵 Tổng giá trị kho cá hiện tại", value=f"{total_val} G"
        )

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button(
                "💰 Bán Toàn Bộ Cá", type="primary", use_container_width=True
            ):
                st.session_state.gold += total_val
                st.session_state.inventory = []
                st.success(
                    f"Đã bán hết cá và thu về **{total_val} G** vào tài khoản!"
                )
                st.rerun()
        with col_b2:
            if st.button("🗑️ Xóa sạch giỏ", use_container_width=True):
                st.session_state.inventory = []
                st.warning("Đã dọn sạch giỏ cá.")
                st.rerun()

with tab3:
    st.subheader("🛒 Cửa Hàng Cần Câu Chuyên Dụng")
    st.markdown(
        "Nâng cấp cần câu để mở khóa sức mạnh, săn các loài cá lớn hơn."
    )

    for r_name, r_info in RODS_SHOP.items():
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"### 🎣 {r_name}")
            st.write(r_info["desc"])
            st.text(
                f"Sức mạnh: +{r_info['power']} | Giá: {r_info['cost']} Vàng"
            )

        with c2:
            owned = r_name in st.session_state.rods
            equipped = st.session_state.current_rod == r_name

            if equipped:
                st.success("Đang sử dụng")
            elif owned:
                if st.button(f"Trang bị", key=f"eq_{r_name}"):
                    st.session_state.current_rod = r_name
                    st.success(f"Đã trang bị {r_name}!")
                    st.rerun()
            else:
                if st.button(f"Mua ngay", key=f"buy_{r_name}"):
                    if st.session_state.gold >= r_info["cost"]:
                        st.session_state.gold -= r_info["cost"]
                        st.session_state.rods[r_name] = {
                            "power": r_info["power"],
                            "owned": True,
                        }
                        st.session_state.current_rod = r_name
                        st.success(f"Đã sở hữu và trang bị {r_name}!")
                        st.rerun()
                    else:
                        st.error("Không đủ vàng để mua cần này!")
        st.markdown("---")

with tab4:
    st.subheader("🏆 Bảng Vàng Thành Tích Cần Thủ")
    st.markdown(
        "Bảng vinh danh lưu giữ tên tuổi những người chơi câu được các loài cá **Cực hiếm** hoặc **Huyền thoại**!"
    )

    if not st.session_state.leaderboard:
        st.info(
            "Chưa có chiến tích khủng nào được ghi nhận. Hãy đi câu các vùng nước sâu để ghi tên mình vào bảng vàng!"
        )
    else:
        lb_df = pd.DataFrame(st.session_state.leaderboard)
        # Đổi tên cột hiển thị thân thiện
        lb_df.columns = ["Tên Cần Thủ", "Loài Cá Săn Được", "Độ Hiếm", "Khu Vực"]
        st.dataframe(lb_df, use_container_width=True, hide_index=True)
