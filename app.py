import os
import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Virtual Cloud Storage",
    page_icon="☁️",
    layout="centered"
)

# Thư mục lưu trữ file ảo
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Khởi tạo Key truy cập trong st.session_state để lưu trữ trạng thái khi chạy trên Cloud
ADMIN_KEY = "ADMIN_MASTER_KEY_2026"

if 'valid_keys' not in st.session_state:
    st.session_state.valid_keys = {
        ADMIN_KEY: "admin",
        "VIP-SAMPLE-KEY-123": "user" # Key mẫu cho khách hàng
    }

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None

def logout():
    st.session_state.authenticated = False
    st.session_state.role = None
    st.rerun()

# --- GIAO DIỆN ĐĂNG NHẬP ---
if not st.session_state.authenticated:
    st.title("☁️ Hệ Thống Cloud Ảo Không Giới Hạn")
    st.write("Vui lòng nhập Key truy cập hợp lệ để sử dụng hệ thống lưu trữ.")

    with st.form("login_form"):
        key_input = st.text_input("Nhập Key Truy Cập:", type="password")
        submit_btn = st.form_submit_button("Truy Cập Cloud")

        if submit_btn:
            key_cleaned = key_input.strip()
            if key_cleaned in st.session_state.valid_keys:
                st.session_state.authenticated = True
                st.session_state.role = st.session_state.valid_keys[key_cleaned]
                st.success("Đăng nhập hệ thống Cloud thành công!")
                st.rerun()
            else:
                st.error("Key không hợp lệ hoặc chưa thanh toán! Vui lòng kiểm tra lại.")

    st.markdown("---")
    st.subheader("💳 Thông tin thanh toán mua Key / Thuê tài khoản:")
    st.markdown("""
    * **Chủ tài khoản:** HOANG HAI AN[span_0](start_span)[span_0](end_span)
    * **Số tài khoản:** `0030132291981`[span_1](start_span)[span_1](end_span)
    * **Ngân hàng:** MB (Ngân hàng Quân Đội)[span_2](start_span)[span_2](end_span)
    """)

    # Hiển thị ảnh QR từ thư mục static/qr.png nếu có
    qr_path = "static/qr.png"
    if os.path.exists(qr_path):
        st.image(qr_path, caption="Quét mã QR để chuyển khoản", width=250)
    else:
        st.info("💡 Mẹo: Hãy đẩy file ảnh QR của bạn lên đường dẫn `static/qr.png` trên GitHub để hiển thị mã QR tại đây.")

    st.markdown("""
    ---
    📞 **Sau khi thanh toán, liên hệ nhận Key qua:**
    * **SĐT / Zalo:** 0964058714
    * **Email:** anhh.compt@gmail.com
    """)

else:
    # --- GIAO DIỆN CHÍNH SAU KHI ĐĂNG NHẬP ---
    role = st.session_state.role
    
    st.sidebar.title("🛠️ Bảng Điều Khiển")
    st.sidebar.write(f"Vai trò: **{'Admin (Miễn phí)' if role == 'admin' else 'Khách hàng (Đã kích hoạt)'}**")
    if st.sidebar.button("Đăng xuất"):
        logout()

    st.title("☁️ Virtual Cloud (Unlimited Upload/Download)")

    # Khu vực Admin (Cấp key mới cho khách)
    if role == 'admin':
        st.subheader("⚙️ Quản Trị Admin - Cấp Key Mới")
        with st.form("add_key_form"):
            new_key = st.text_input("Nhập key mới cho khách hàng:")
            add_btn = st.form_submit_button("Tạo & Kích Hoạt Key")
            if add_btn:
                if new_key.strip():
                    st.session_state.valid_keys[new_key.strip()] = 'user'
                    st.success(f"Đã cấp key mới thành công: `{new_key.strip()}`")
                else:
                    st.warning("Vui lòng nhập nội dung key!")
        st.markdown("---")

    # Khu vực Upload file không giới hạn
    st.subheader("📤 Tải Lên File (Không giới hạn dung lượng)")
    uploaded_file = st.file_uploader("Chọn file bất kỳ từ thiết bị của bạn:")
    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Upload file thành công: **{uploaded_file.name}**")

    st.markdown("---")

    # Khu vực Danh sách file và Download
    st.subheader("📂 Danh Sách File Đã Lưu Trữ Trên Cloud")
    if os.path.exists(UPLOAD_FOLDER):
        files = os.listdir(UPLOAD_FOLDER)
        if files:
            for file_name in files:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text(file_name)
                with col2:
                    file_full_path = os.path.join(UPLOAD_FOLDER, file_name)
                    with open(file_full_path, "rb") as f:
                        st.download_button(
                            label="Download",
                            data=f,
                            file_name=file_name,
                            key=f"download_{file_name}"
                        )
        else:
            st.info("Chưa có file nào trên hệ thống cloud.")
