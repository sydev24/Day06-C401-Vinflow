import streamlit as st
import os
import sys
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI IN ACTION COPILOT", page_icon="🤖", layout="wide")

project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, "src")
for path in [src_path, project_root]:
    if path not in sys.path:
        sys.path.insert(0, path)

try:
    from src.copilot import ask_copilot
    import_ok = True
except ImportError as e:
    st.error(f"Không import được src.copilot. Chi tiết: {e}")
    import_ok = False

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 AI IN ACTION COPILOT")
st.caption("RAG Copilot · Vin AI Thực Chiến · Batch 02")

st.sidebar.markdown("### ⚙️ Quản lý")
if st.sidebar.button("🗑️ Xóa lịch sử"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Câu hỏi đã hỏi")
user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
if user_msgs:
    for i, m in enumerate(user_msgs, 1):
        preview = m["content"][:50] + "..." if len(m["content"]) > 50 else m["content"]
        st.sidebar.markdown(f"`{i}.` {preview}")
else:
    st.sidebar.caption("Chưa có câu hỏi nào.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Câu hỏi gợi ý")
suggestions = [
    "Day 5 cần nộp gì?",
    "Evidence Pack gồm những phần nào?",
    "Prototype Level 3 yêu cầu gì?",
    "Thin SPEC là gì?",
]
for q in suggestions:
    st.sidebar.markdown(f"- {q}")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if msg.get("sources"):
                st.caption(f"📚 **Nguồn:** {', '.join(msg['sources'])}")
            if msg.get("next_action"):
                st.info(f"💡 **Bước tiếp:** {msg['next_action']}")

if not import_ok:
    st.warning("Kiểm tra file src/copilot.py và dependencies.")
else:
    if prompt := st.chat_input("Nhập câu hỏi..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Đang tìm kiếm..."):
                try:
                    response = ask_copilot(prompt)

                    answer = response.get("answer", "Không nhận được câu trả lời.")
                    sources = response.get("sources", [])
                    next_action = response.get("next_action", "")

                    st.markdown(answer)

                    if sources:
                        st.caption(f"📚 **Nguồn:** {', '.join(sources)}")
                    if next_action:
                        st.info(f"💡 **Bước tiếp:** {next_action}")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                        "next_action": next_action,
                    })

                except Exception as e:
                    st.error(f"Lỗi: {e}")
