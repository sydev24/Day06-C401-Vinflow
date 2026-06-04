import streamlit as st
import os
import sys
import uuid
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ─── CẤU HÌNH TRANG ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI IN ACTION COPILOT", 
    page_icon="✨", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS CUSTOM (ÉP CỐ ĐỊNH LIGHT THEME & KHUNG GỢI Ý CLICK ĐƯỢC) ────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

/* HỆ THỐNG BIẾN MÀU SẮC (CHỈ DÙNG THEME SÁNG) */
:root {
    --bg-main: #ffffff;
    --bg-sidebar: #f8fafc;
    --text-main: #0f172a;
    --text-muted: #64748b;
    --border-color: #e2e8f0;
    --accent: #6366f1;
    --accent-hover: #4f46e5;
    --btn-bg: #ffffff;
    --btn-hover-bg: #f1f5f9;
    --chat-user-bg: #f8fafc;
    --chat-ai-bg: #ffffff;
    --chip-bg: rgba(99, 102, 241, 0.08);
    --chip-border: rgba(99, 102, 241, 0.15);
}

/* ÉP STYLE TOÀN TRANG TRÁNH LỖI DARK MODE MẶC ĐỊNH CỦA STREAMLIT */
html, body, [class*="css"], .stApp { 
    font-family: 'Plus Jakarta Sans', sans-serif !important; 
    color: var(--text-main) !important;
    background-color: var(--bg-main) !important;
}

[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar) !important;
}

/* DỌN DẸP UI STREAMLIT */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {background-color: transparent !important;}
.stAppDeployButton {display: none !important;}
[data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"] { border: none !important; }

/* 2. TÀNG HÌNH THANH CUỘN TỔNG CỦA SIDEBAR */
[data-testid="stSidebar"] > div:first-child {
    scrollbar-width: none !important; 
    -ms-overflow-style: none !important; 
}
[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar {
    display: none !important; 
}

/* HEADER GRADIENT */
.gradient-header {
    background: linear-gradient(135deg, #6366f1 0%, #a78bfa 50%, #ec4899 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-size: 2.2rem; font-weight: 800; margin-bottom: 0px; padding-bottom: 0px;
    letter-spacing: -0.02em;
}

/* THANH CUỘN (SCROLLBAR) */
::-webkit-scrollbar { width: 5px; background: transparent; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: transparent; border-radius: 10px; }
*:hover::-webkit-scrollbar-thumb { background: var(--border-color); } 
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* ANIMATION & STYLE TIN NHẮN CHAT */
[data-testid="stChatMessage"] {
    animation: slideUpFade 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    padding: 1.2rem !important; 
    border-radius: 16px; 
    margin-bottom: 12px;
    border: 1px solid transparent;
}
[data-testid="stChatMessage"]:nth-child(odd) { background-color: var(--chat-user-bg); border-color: var(--border-color); }
[data-testid="stChatMessage"]:nth-child(even) { background-color: var(--chat-ai-bg); }

@keyframes slideUpFade {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* SIDEBAR: NÚT LỊCH SỬ */
[data-testid="stSidebar"] .stButton > button:not([kind="primary"]) {
    border: none !important; background-color: transparent !important;
    box-shadow: none !important; padding: 0.4rem 0.6rem !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important; 
    border-radius: 10px !important;
}
[data-testid="stSidebar"] .stButton > button:not([kind="primary"]) p {
    color: var(--text-muted) !important; font-size: 0.9rem !important;
    font-weight: 500 !important; text-align: left !important;
}
[data-testid="stSidebar"] .stButton > button:not([kind="primary"]):hover {
    background-color: var(--btn-hover-bg) !important; 
    transform: translateX(4px);
}
[data-testid="stSidebar"] .stButton > button:not([kind="primary"]):hover p { color: var(--accent) !important; }

/* SIDEBAR: NÚT TẠO CHAT MỚI */
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent), #a78bfa) !important;
    border: none !important; color: white !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important; 
    border-radius: 10px !important;
    padding: 0.3rem 0.5rem !important; width: 100% !important; min-height: 40px !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] p { 
    font-weight: 600 !important; color: white !important; font-size: 0.85rem !important; 
}
[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important; 
    transform: translateY(-2px) !important;
}

/* MÀN HÌNH CHÍNH: NÚT GỢI Ý & BƯỚC TIẾP ĐẦY ĐỦ */
.main .stButton > button {
    border-radius: 12px !important; 
    border: 1px solid var(--border-color) !important;
    color: var(--text-main) !important;
    background-color: var(--chip-bg) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    padding: 0.8rem 1rem !important;
    height: auto !important; /* Đảm bảo text dài xuống dòng không bị cắt */
    text-align: left !important;
    border-left: 4px solid var(--accent) !important; /* Viền trái giống box cũ */
}
.main .stButton > button p { 
    font-size: 0.9rem !important; 
    font-weight: 500 !important; 
    white-space: normal !important; /* Quan trọng: cho phép text xuống dòng */
}
.main .stButton > button:hover {
    background-color: var(--border-color) !important;
    transform: translateY(-2px); 
    color: var(--accent) !important;
}

/* NGUỒN TÀI LIỆU (CHIPS) */
.source-chip {
    display: inline-flex; align-items: center; padding: 4px 12px; margin: 6px 8px 0 0;
    border-radius: 20px; background-color: var(--chip-bg);
    color: var(--accent); font-size: 0.75rem; font-weight: 600;
    border: 1px solid var(--chip-border); transition: all 0.2s ease; cursor: default;
}
.source-chip:hover { background-color: var(--chip-border); transform: translateY(-2px); }

/* HIỆU ỨNG THINKING DOTS */
.thinking-container {
    display: flex; align-items: center; gap: 6px; padding: 10px; color: var(--accent); font-weight: 600; font-size: 0.9rem;
}
.dot {
    width: 6px; height: 6px; border-radius: 50%; background-color: var(--accent);
    animation: typingBounce 1.4s infinite ease-in-out both;
}
.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }
@keyframes typingBounce { 0%, 80%, 100% { transform: scale(0); opacity: 0.5; } 40% { transform: scale(1); opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# ─── PATH SETUP & MODULE IMPORT ──────────────────────────────────────────────
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, "src")
for path in [src_path, project_root]:
    if path not in sys.path: sys.path.insert(0, path)

try:
    from src.rag_chain import ask_copilot
    import_ok = True
except ImportError as e:
    st.error(f"Không import được src.rag_chain. Chi tiết: {e}")
    import_ok = False

# ─── STATE QUẢN LÝ LỊCH SỬ CHAT ──────────────────────────────────────────────
if "chat_sessions" not in st.session_state:
    init_id = str(uuid.uuid4())
    st.session_state.chat_sessions = {
        init_id: {"title": "Chat mới", "messages": [], "created_at": datetime.now()}
    }
    st.session_state.current_session = init_id

if "suggestion_clicked" not in st.session_state:
    st.session_state.suggestion_clicked = None

def create_new_chat():
    new_id = str(uuid.uuid4())
    st.session_state.chat_sessions[new_id] = {
        "title": "Chat mới", "messages": [], "created_at": datetime.now()
    }
    st.session_state.current_session = new_id

# ─── GIAO DIỆN CHÍNH ─────────────────────────────────────────────────────────
st.markdown('<h1 class="gradient-header">✨ AI IN ACTION COPILOT</h1>', unsafe_allow_html=True)
st.caption("🚀 RAG Copilot · Vin AI Thực Chiến · Batch 02")
st.markdown("---")

# ─── SIDEBAR (CHỈ CÒN LỊCH SỬ CHAT) ──────────────────────────────────────────
st.sidebar.button("➕ Tạo Chat Mới", on_click=create_new_chat, type="primary", use_container_width=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

st.sidebar.markdown("### 🕒 Lịch sử Chat")
history_container = st.sidebar.container(height=600)
with history_container:
    sorted_sessions = sorted(
        st.session_state.chat_sessions.items(), key=lambda x: x[1]['created_at'], reverse=True
    )
    for s_id, s_data in sorted_sessions:
        prefix = "🟢 " if s_id == st.session_state.current_session else "💬 "
        if st.button(f"{prefix}{s_data['title']}", key=f"btn_{s_id}", use_container_width=True):
            st.session_state.current_session = s_id
            st.rerun()

# ─── LUỒNG CHAT CHÍNH VÀ GỢI Ý NGỮ CẢNH ──────────────────────────────────────
current_session_id = st.session_state.current_session
current_messages = st.session_state.chat_sessions[current_session_id]["messages"]

# MÀN HÌNH CHÀO MỪNG 
if not current_messages:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: var(--text-muted); font-weight: 500;'>Bạn muốn hỏi gì hôm nay?</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    cols = st.columns(4)
    defaults = ["Nộp gì Day 5?", "Evidence Pack có gì?", "Yêu cầu Prototype L3?", "Thin SPEC là gì?"]
    for idx, q in enumerate(defaults):
        if cols[idx].button(q, key=f"def_sug_{idx}", use_container_width=True):
            st.session_state.suggestion_clicked = q
            st.rerun()

# HIỂN THỊ LỊCH SỬ TIN NHẮN
for i, msg in enumerate(current_messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        if msg["role"] == "assistant":
            # Hiển thị nguồn (nếu có)
            if msg.get("sources"):
                chips_html = "".join([f'<span class="source-chip">📄 {s}</span>' for s in msg["sources"]])
                st.markdown(f'<div style="margin-top: 5px;">{chips_html}</div>', unsafe_allow_html=True)
            
            # HIỂN THỊ "BƯỚC TIẾP" DƯỚI DẠNG NÚT BẤM (Cho phép Click)
            if msg.get("next_action"):
                st.markdown("<br>", unsafe_allow_html=True) # Khoảng trống nhỏ cho dễ nhìn
                if st.button(f"💡 Gợi ý bước tiếp theo: {msg['next_action']}", key=f"hist_sug_{i}", use_container_width=True):
                    st.session_state.suggestion_clicked = msg['next_action']
                    st.rerun()

# ─── XỬ LÝ ĐẦU VÀO CỦA USER ──────────────────────────────────────────────────
if not import_ok:
    st.warning("⚠️ Kiểm tra file src/rag_chain.py và dependencies.")
else:
    user_input = st.chat_input("Nhập câu hỏi của bạn tại đây...")
    
    # Xử lý input từ click gợi ý
    if st.session_state.suggestion_clicked:
        user_input = st.session_state.suggestion_clicked
        st.session_state.suggestion_clicked = None 

    if user_input:
        st.session_state.chat_sessions[current_session_id]["messages"].append({"role": "user", "content": user_input})
        
        if len(st.session_state.chat_sessions[current_session_id]["messages"]) == 1:
            short_title = user_input[:20] + "..." if len(user_input) > 20 else user_input
            st.session_state.chat_sessions[current_session_id]["title"] = short_title
            
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            thinking_placeholder = st.empty()
            thinking_placeholder.markdown("""
                <div class="thinking-container">
                    Thinking <div class="dot"></div><div class="dot"></div><div class="dot"></div>
                </div>
            """, unsafe_allow_html=True)
            
            try:
                response = ask_copilot(user_input)
                
                thinking_placeholder.empty()

                answer = response.get("answer", "Không nhận được câu trả lời.")
                sources = response.get("sources", [])
                next_action = response.get("next_action", "")

                st.markdown(answer)

                if sources:
                    chips_html = "".join([f'<span class="source-chip">📄 {s}</span>' for s in sources])
                    st.markdown(f'<div style="margin-top: 5px;">{chips_html}</div>', unsafe_allow_html=True)

                # Nút bấm Gợi ý cho tin nhắn mới nhất
                if next_action:
                    new_idx = len(st.session_state.chat_sessions[current_session_id]["messages"])
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button(f"💡 Gợi ý bước tiếp theo: {next_action}", key=f"hist_sug_{new_idx}", use_container_width=True):
                        st.session_state.suggestion_clicked = next_action
                        st.rerun()

                st.session_state.chat_sessions[current_session_id]["messages"].append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                    "next_action": next_action,
                })
                
            except Exception as e:
                thinking_placeholder.empty()
                st.error(f"Lỗi: {e}")