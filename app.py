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

# ─── CSS CUSTOM (ĐÃ KHÔI PHỤC NÚT MỞ SIDEBAR) ───────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }

/* 1. XÓA NÚT DEPLOY & WATERMARK NHƯNG GIỮ NÚT MỞ SIDEBAR */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stAppDeployButton {display: none !important;}
header {background-color: transparent !important;} /* Cho cái thanh trên cùng trong suốt để đẹp hơn */

/* 2. TÀNG HÌNH THANH CUỘN TỔNG CỦA SIDEBAR */
[data-testid="stSidebar"] > div:first-child {
    scrollbar-width: none !important; /* Firefox */
    -ms-overflow-style: none !important; /* IE/Edge */
}
[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar {
    display: none !important; /* Chrome/Safari */
}

/* 3. TÙY CHỈNH THANH CUỘN TRONG KHUNG LỊCH SỬ (Nhỏ, mượt, tàng hình) */
::-webkit-scrollbar { width: 5px; background: transparent; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: transparent; border-radius: 10px; }
*:hover::-webkit-scrollbar-thumb { background: #cbd5e1; } /* Chỉ hiện khi rê chuột */
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

/* 4. TẮT VIỀN CỦA CONTAINER TRONG SIDEBAR */
[data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"] { border: none !important; }

/* Animation trượt tin nhắn */
[data-testid="stChatMessage"] {
    animation: slideUpFade 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    padding: 1.2rem !important; border-radius: 12px; margin-bottom: 12px;
}
@keyframes slideUpFade {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.gradient-header {
    background: linear-gradient(135deg, #6366f1 0%, #a78bfa 50%, #ec4899 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-size: 2.2rem; font-weight: 800; margin-bottom: 0px; padding-bottom: 0px;
}

/* NÚT LỊCH SỬ CHAT */
[data-testid="stSidebar"] .stButton > button:not([kind="primary"]) {
    border: none !important; background-color: transparent !important;
    box-shadow: none !important; padding: 0.2rem 0.5rem !important;
    transition: all 0.2s ease !important; border-radius: 8px !important;
}
[data-testid="stSidebar"] .stButton > button:not([kind="primary"]) > div {
    width: 100%; justify-content: flex-start !important;
}
[data-testid="stSidebar"] .stButton > button:not([kind="primary"]) p {
    color: #4b5563 !important; font-size: 0.9rem !important;
    font-weight: 500 !important; text-align: left !important;
}
[data-testid="stSidebar"] .stButton > button:not([kind="primary"]):hover {
    background-color: #ede9fe !important; transform: translateX(4px);
}
[data-testid="stSidebar"] .stButton > button:not([kind="primary"]):hover p { color: #6366f1 !important; }

/* NÚT TẠO CHAT MỚI */
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1, #818cf8) !important;
    border: none !important; color: white !important;
    transition: all 0.3s ease !important; border-radius: 8px !important;
    padding: 0.3rem 0.5rem !important; width: 100% !important; min-height: 38px !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] p { 
    font-weight: 600 !important; color: white !important; font-size: 0.85rem !important; 
}
[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important; transform: translateY(-2px) !important;
}

/* NÚT GỢI Ý NGỮ CẢNH (DƯỚI CHAT) */
.main .stButton > button {
    border-radius: 20px !important; 
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    color: #6366f1 !important; background-color: #ffffff !important;
    transition: all 0.2s ease !important; padding: 0.1rem 0.8rem !important;
}
.main .stButton > button p { font-size: 0.85rem !important; font-weight: 500 !important; }
.main .stButton > button:hover {
    background-color: rgba(99, 102, 241, 0.08) !important;
    border-color: #6366f1 !important; transform: translateY(-2px);
}

/* Nguồn (Chips) */
.source-chip {
    display: inline-flex; align-items: center; padding: 4px 12px; margin: 6px 6px 0 0;
    border-radius: 20px; background-color: rgba(99, 102, 241, 0.08);
    color: #6366f1; font-size: 0.75rem; font-weight: 600;
    border: 1px solid rgba(99, 102, 241, 0.15); transition: all 0.2s ease;
}
.source-chip:hover { background-color: rgba(99, 102, 241, 0.15); transform: translateY(-2px); }

/* Hiệu ứng Thinking Dots */
.thinking-container {
    display: flex; align-items: center; gap: 6px; padding: 10px; color: #6366f1; font-weight: 600; font-size: 0.9rem;
}
.dot {
    width: 6px; height: 6px; border-radius: 50%; background-color: #6366f1;
    animation: typingBounce 1.4s infinite ease-in-out both;
}
.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }
@keyframes typingBounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }
</style>
""", unsafe_allow_html=True)

# ─── PATH SETUP & MODULE IMPORT ──────────────────────────────────────────────
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, "src")
for path in [src_path, project_root]:
    if path not in sys.path: sys.path.insert(0, path)

try:
    from src.copilot import ask_copilot
    import_ok = True
except ImportError as e:
    st.error(f"Không import được src.copilot. Chi tiết: {e}")
    import_ok = False

# ─── HÀM BÓC TÁCH TỪ KHÓA THÔNG MINH ─────────────────────────────────────────
def generate_short_suggestions(text):
    fluff_patterns = [
        r"(?i)bạn có muốn( tìm hiểu)?( biết)?( thêm)?( chi tiết)?( hơn)?( về)?",
        r"(?i)bạn( có)? muốn( hỏi)?( thêm)?( về)?",
        r"(?i)bạn có thể( tham khảo)?( hỏi)?( tiếp)?( về)?",
        r"(?i)ví dụ(:)?", r"(?i)gợi ý(:)?", r"(?i)bước tiếp( theo)?(:)?",
        r"(?i)có thể bạn( sẽ)? quan tâm(:)?", r"(?i)hãy hỏi( tôi)?( về)?"
    ]
    cleaned_text = text
    for pattern in fluff_patterns:
        cleaned_text = re.sub(pattern, "", cleaned_text).strip()
        
    cleaned_text = re.sub(r"^[\:\-\.\,\s]+", "", cleaned_text)
    parts = re.split(r'[,;?.]|\bhay\b|\bhoặc\b', cleaned_text)
    
    suggestions = []
    for p in parts:
        p = p.strip(" -\"'") 
        if len(p) > 2:
            words = p.split()
            short_text = " ".join(words[:5]) + "..." if len(words) > 5 else p
            short_text = short_text.capitalize()
            if short_text not in suggestions:
                suggestions.append(short_text)
                
    if not suggestions:
        words = text.split()
        return [" ".join(words[:5]) + "..."] if len(words) > 5 else [text]
    return suggestions

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
history_container = st.sidebar.container(height=500)
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
    st.markdown("<h3 style='text-align: center; color: #4b5563; font-weight: 500;'>Bạn muốn hỏi gì hôm nay?</h3>", unsafe_allow_html=True)
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
            if msg.get("sources"):
                chips_html = "".join([f'<span class="source-chip">📄 {s}</span>' for s in msg["sources"]])
                st.markdown(f'<div style="margin-top: 5px;">{chips_html}</div>', unsafe_allow_html=True)
            
            # GỢI Ý NÚT CHUẨN CHATGPT Ở CUỐI CÂU 
            is_last_message = (i == len(current_messages) - 1)
            if is_last_message and msg.get("next_action"):
                sugs = generate_short_suggestions(msg["next_action"])
                if sugs:
                    st.markdown("<div style='margin-top: 15px; margin-bottom: 8px; font-size: 0.85rem; color: #6b7280; font-weight: 600;'>💡 Có thể bạn quan tâm:</div>", unsafe_allow_html=True)
                    
                    cols = st.columns(min(len(sugs), 4))
                    for c_idx, q in enumerate(sugs[:4]):
                        if cols[c_idx].button(q, key=f"chat_sug_{c_idx}", use_container_width=True):
                            st.session_state.suggestion_clicked = q
                            st.rerun()

# ─── XỬ LÝ ĐẦU VÀO CỦA USER ──────────────────────────────────────────────────
if not import_ok:
    st.warning("⚠️ Kiểm tra file src/copilot.py và dependencies.")
else:
    user_input = st.chat_input("Nhập câu hỏi của bạn tại đây...")
    
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

                st.session_state.chat_sessions[current_session_id]["messages"].append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                    "next_action": next_action,
                })
                
                # Bắt buộc Rerun để sinh ra cụm nút bấm Gợi ý ở cuối tin nhắn vừa trả lời
                st.rerun()

            except Exception as e:
                thinking_placeholder.empty()
                st.error(f"Lỗi: {e}")