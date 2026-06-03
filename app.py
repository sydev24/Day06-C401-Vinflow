import streamlit as st
import os
import sys
from dotenv import load_dotenv

st.set_page_config(page_title="AI Product Lab - RAG Copilot", page_icon="🤖", layout="wide")

# --- FIX IMPORT PATH ---
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, "src")
for path in [src_path, project_root]:
    if path not in sys.path:
        sys.path.insert(0, path)

try:
    from src.copilot import ask_copilot
    import_ok = True
except ImportError as e:
    st.error(f"❌ Không import được src.copilot. Chi tiết lỗi: {e}")
    import_ok = False

load_dotenv()

# ==========================================
# UI CHÍNH
# ==========================================
st.title("🤖 RAG Copilot – Production UI")
st.markdown("Hệ thống trợ lý ảo RAG đã kết nối trực tiếp với Vector Store và LLM.")

# --- SIDEBAR ---
st.sidebar.markdown("### ⚙️ Quản lý hệ thống")

if st.sidebar.button("🗑️ Xóa lịch sử phiên làm việc"):
    st.session_state.messages = []
    st.rerun()

# LOG CHAT (sidebar)
st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Lịch sử câu hỏi")
if "messages" in st.session_state and st.session_state.messages:
    user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
    if user_msgs:
        for i, m in enumerate(user_msgs, 1):
            preview = m["content"][:60] + "..." if len(m["content"]) > 60 else m["content"]
            st.sidebar.markdown(f"`{i}.` {preview}")
    else:
        st.sidebar.caption("Chưa có câu hỏi nào.")
else:
    st.sidebar.caption("Chưa có câu hỏi nào.")

# --- KHỞI TẠO SESSION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- HIỂN THỊ LỊCH SỬ CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            # KEY ĐÚNG: "sources" (list), "next_action" (str)
            if msg.get("sources"):
                st.caption(f"📚 **Nguồn tham chiếu:** {', '.join(msg['sources'])}")
            if msg.get("next_action"):
                st.info(f"💡 **Gợi ý hành động:** {msg['next_action']}")

# --- LUỒNG XỬ LÝ CHAT ---
if not import_ok:
    st.warning("Vui lòng kiểm tra và đảm bảo file copilot.py tồn tại trong thư mục src.")
else:
    if prompt := st.chat_input("Nhập câu hỏi của bạn tại đây..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Đang truy xuất dữ liệu..."):
                try:
                    response = ask_copilot(prompt)

                    answer      = response.get("answer", "Không nhận được câu trả lời hợp lệ.")
                    sources     = response.get("sources", [])     # list[str] – KEY ĐÚNG
                    next_action = response.get("next_action", "") # str – không phải list

                    st.markdown(answer)

                    if sources:
                        st.caption(f"📚 **Nguồn tham chiếu:** {', '.join(sources)}")
                    if next_action:
                        st.info(f"💡 **Hành động tiếp theo:** {next_action}")

                    st.session_state.messages.append({
                        "role":        "assistant",
                        "content":     answer,
                        "sources":     sources,
                        "next_action": next_action,
                    })

                except Exception as e:
                    st.error(f"🔴 Lỗi backend: {str(e)}")

        st.rerun()  # Cập nhật sidebar log ngay sau khi có câu trả lời