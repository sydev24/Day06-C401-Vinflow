import csv
import sys
from pathlib import Path

# Thêm đường dẫn project để import được src
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.copilot import ask_copilot

def main():
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
        
    print("🚀 Đang khởi tạo AI Copilot (Sẽ kết nối với MIMO LLM API)...")

    csv_path = project_root / "data" / "test_cases.csv"
    if not csv_path.exists():
        print(f"❌ Không tìm thấy file {csv_path}")
        return

    print(f"Đang đọc danh sách câu hỏi từ {csv_path.name}...\n")

    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for idx, row in enumerate(reader, 1):
            category = row.get("Loại câu hỏi", "Unknown")
            question = row.get("Câu hỏi", "")
            expected = row.get("Câu trả lời mong đợi (Ground Truth)", "")
            
            if not question:
                continue

            print("=" * 80)
            print(f"📝 TEST CASE #{idx} [{category}]")
            print(f"❓ Hỏi: {question}")
            print(f"🎯 Trả lời mong đợi: {expected}")
            print("-" * 40)
            
            print("⏳ AI đang suy nghĩ và tổng hợp câu trả lời...")
            try:
                # Gọi thẳng hàm ask_copilot của Backend
                result = ask_copilot(question, top_k=3)
                
                print(f"🤖 AI Trả lời: {result.get('answer', '')}")
                print(f"💡 Gợi ý tiếp theo: {result.get('next_action', '')}")
                print("📚 Nguồn trích dẫn:")
                sources = result.get('sources', [])
                if sources:
                    for src in sources:
                        print(f"  - {src}")
                else:
                    print("  (Không có nguồn)")
            except Exception as e:
                print(f"❌ Lỗi khi gọi AI: {e}")
            
            print("=" * 80 + "\n")
            
            # Tạm dừng để dễ theo dõi
            if idx % 2 == 0:
                cont = input("💡 Nhấn Enter để test 2 câu tiếp theo, hoặc gõ 'q' để thoát: ")
                if cont.strip().lower() == 'q':
                    break

    print("✅ Đã hoàn thành bài test AI Copilot!")

if __name__ == "__main__":
    main()
