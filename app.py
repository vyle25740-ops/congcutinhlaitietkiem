import streamlit as st
st.image("tctt.jpg")
import math

st.set_page_config(
    page_title="App tính tiền gửi tiết kiệm_Lê Vy Bank",
    page_icon="💰",
    layout="centered"
)

st.title("💰 App tính tiền gửi tiết kiệm_Lê Vy Bank")
st.markdown("Tính lãi đơn & lãi kép – Lãnh lãi theo tháng / quý / cuối kỳ")

# ==================== INPUT ====================
st.subheader("Nhập thông tin")

col1, col2 = st.columns(2)

with col1:
    so_tien = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )
    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        value=12,
        step=1
    )

with col2:
    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        value=6.0,
        step=0.1,
        format="%.2f"
    )
    loai_lai = st.selectbox(
        "Loại lãi",
        ["Lãi đơn", "Lãi kép"]
    )

hinh_thuc = st.radio(
    "Hình thức lãnh lãi",
    ["Lãnh lãi theo tháng", "Lãnh lãi theo quý", "Lãnh lãi cuối kỳ"],
    horizontal=True
)

# ==================== HÀM TÍNH TOÁN ====================
def tinh_lai(so_tien, ky_han, lai_suat, loai_lai, hinh_thuc):
    """
    Trả về:
    - lai_dinh_ky: tiền lãi mỗi kỳ (nếu có)
    - tong_lai: tổng tiền lãi
    - tong_nhan: gốc + lãi
    - so_ky: số kỳ lãnh lãi
    - ghi_chu: giải thích ngắn
    """
    r = lai_suat / 100          # lãi suất năm dạng thập phân
    n = ky_han                  # số tháng

    # ---------- LÃI ĐƠN ----------
    if loai_lai == "Lãi đơn":
        tong_lai = so_tien * r * (n / 12)
        tong_nhan = so_tien + tong_lai

        if hinh_thuc == "Lãnh lãi theo tháng":
            lai_dinh_ky = so_tien * r / 12
            so_ky = n
            ghi_chu = "Lãi đơn – nhận lãi mỗi tháng (gốc không đổi)."
        elif hinh_thuc == "Lãnh lãi theo quý":
            if n % 3 != 0:
                return None, None, None, None, "Kỳ hạn phải chia hết cho 3 tháng khi lãnh lãi theo quý."
            lai_dinh_ky = so_tien * r / 4
            so_ky = n // 3
            ghi_chu = "Lãi đơn – nhận lãi mỗi quý (gốc không đổi)."
        else:  # Cuối kỳ
            lai_dinh_ky = tong_lai
            so_ky = 1
            ghi_chu = "Lãi đơn – nhận toàn bộ lãi cuối kỳ."

        return lai_dinh_ky, tong_lai, tong_nhan, so_ky, ghi_chu

    # ---------- LÃI KÉP ----------
    else:
        if hinh_thuc == "Lãnh lãi theo tháng":
            # Compound monthly
            rate = r / 12
            tong_nhan = so_tien * (1 + rate) ** n
            tong_lai = tong_nhan - so_tien
            # Tiền lãi định kỳ trung bình (hoặc lãi tháng đầu)
            lai_dinh_ky = so_tien * rate          # lãi tháng đầu tiên
            so_ky = n
            ghi_chu = "Lãi kép nhập gốc hàng tháng. Tiền lãi định kỳ hiển thị là lãi của tháng đầu tiên (sau đó tăng dần)."

        elif hinh_thuc == "Lãnh lãi theo quý":
            if n % 3 != 0:
                return None, None, None, None, "Kỳ hạn phải chia hết cho 3 tháng khi lãnh lãi theo quý."
            rate = r / 4
            so_ky_quy = n // 3
            tong_nhan = so_tien * (1 + rate) ** so_ky_quy
            tong_lai = tong_nhan - so_tien
            lai_dinh_ky = so_tien * rate          # lãi quý đầu
            so_ky = so_ky_quy
            ghi_chu = "Lãi kép nhập gốc hàng quý. Tiền lãi định kỳ hiển thị là lãi của quý đầu tiên (sau đó tăng dần)."

        else:  # Cuối kỳ – compound theo năm (nếu kỳ hạn ≥ 12 tháng) hoặc theo tháng
            if n >= 12 and n % 12 == 0:
                so_nam = n // 12
                tong_nhan = so_tien * (1 + r) ** so_nam
                ghi_chu = "Lãi kép nhập gốc hàng năm, nhận cả gốc + lãi cuối kỳ."
            else:
                # Compound monthly cho kỳ hạn không tròn năm
                rate = r / 12
                tong_nhan = so_tien * (1 + rate) ** n
                ghi_chu = "Lãi kép nhập gốc hàng tháng, nhận cả gốc + lãi cuối kỳ."
            tong_lai = tong_nhan - so_tien
            lai_dinh_ky = tong_lai
            so_ky = 1

        return lai_dinh_ky, tong_lai, tong_nhan, so_ky, ghi_chu

# ==================== TÍNH & HIỂN THỊ ====================
if st.button("Tính lãi", type="primary", use_container_width=True):
    if so_tien <= 0 or ky_han <= 0 or lai_suat < 0:
        st.error("Vui lòng nhập số tiền > 0, kỳ hạn ≥ 1 tháng và lãi suất ≥ 0.")
    else:
        result = tinh_lai(so_tien, ky_han, lai_suat, loai_lai, hinh_thuc)

        if result[0] is None:
            st.error(result[4])
        else:
            lai_dinh_ky, tong_lai, tong_nhan, so_ky, ghi_chu = result

            st.success("Kết quả tính toán")
            st.markdown(f"**{ghi_chu}**")

            # Format số tiền kiểu Việt Nam
            def fmt(x):
                return f"{x:,.0f}".replace(",", ".")

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Tiền lãi định kỳ", f"{fmt(lai_dinh_ky)} VNĐ")
            with col_b:
                st.metric("Tổng tiền lãi", f"{fmt(tong_lai)} VNĐ")
            with col_c:
                st.metric("Tổng gốc + lãi", f"{fmt(tong_nhan)} VNĐ")

            st.markdown("---")
            st.markdown(f"""
            **Chi tiết:**
            - Số tiền gửi: **{fmt(so_tien)} VNĐ**
            - Kỳ hạn: **{ky_han} tháng**
            - Lãi suất: **{lai_suat}%/năm**
            - Loại lãi: **{loai_lai}**
            - Hình thức: **{hinh_thuc}**
            - Số kỳ nhận lãi: **{so_ky}**
            """)

# ==================== GHI CHÚ ====================
with st.expander("📌 Giải thích công thức"):
    st.markdown("""
    ### Lãi đơn
    - Tổng lãi = Số tiền gửi × Lãi suất năm × (Kỳ hạn tháng / 12)
    - Lãi tháng = Số tiền gửi × Lãi suất năm / 12
    - Lãi quý = Số tiền gửi × Lãi suất năm / 4
    - Gốc **không** thay đổi.

    ### Lãi kép
    - **Theo tháng**:  
      Tổng = Gốc × (1 + r/12)^n  
    - **Theo quý**:  
      Tổng = Gốc × (1 + r/4)^(n/3)  
    - **Cuối kỳ**:  
      - Kỳ hạn tròn năm → nhập gốc hàng năm  
      - Kỳ hạn khác → nhập gốc hàng tháng  

    > **Lưu ý**: Khi chọn “Lãnh lãi theo tháng/quý” với **lãi kép**, lãi được nhập gốc (compound).  
    Tiền lãi định kỳ hiển thị là lãi của **kỳ đầu tiên** (các kỳ sau sẽ cao hơn vì gốc tăng).
    """)

st.caption("Ứng dụng chỉ mang tính chất minh họa. Lãi suất thực tế ngân hàng có thể tính theo ngày (365 hoặc 360) và có quy định riêng.")
