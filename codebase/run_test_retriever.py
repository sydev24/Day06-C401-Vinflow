import csv
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.retriever import CourseRetriever

def main():
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    print("🚀 Đang khởi tạo Retriever (Có thể mất vài giây để load model/vectorstore)...")
    try:
        retriever = CourseRetriever()
    except Exception as e:
        print(f"❌ Lỗi khởi tạo Retriever: {e}")
        print("Vui lòng chắc chắn rằng bạn đã chạy 'python -m src.dataset.build_index' trước đó.")
        return

    csv_path = project_root / "data" / "test_cases.csv"
    if not csv_path.exists():
        print(f"❌ Không tìm thấy file {csv_path}")
        return

    print(f"\n✅ Đã load Retriever thành công!")
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
            print(f"❓ Câu hỏi: {question}")
            print(f"🎯 Trả lời mong đợi: {expected}")
            
            # Chỉ test với các câu không phải là (Fallback) vì RAG có thể không tìm thấy
            if "(Fallback)" in expected:
                print("⚠️  [Skip search] Câu hỏi này nằm ngoài phạm vi hoặc yêu cầu fallback.")
                print("=" * 80 + "\n")
                continue
                
            print("-" * 40)
            print("🔍 Đang tìm kiếm trong cơ sở dữ liệu...")
            try:
                results = retriever.search(question, top_k=2)
                
                if not results:
                    print("❌ Không tìm thấy đoạn tài liệu nào phù hợp.")
                else:
                    for i, res in enumerate(results, 1):
                        score = res.get('score', 0.0)
                        source = res.get('source_file', 'Unknown')
                        content = res.get('content', '')
                        
                        # Chỉ in ra 150 ký tự đầu tiên để dễ nhìn
                        preview = content[:150].replace('\n', ' ') + "..."
                        
                        print(f"  [{i}] File: {source} | Score: {score:.4f}")
                        print(f"      Đoạn trích: {preview}")
            except Exception as e:
                print(f"❌ Lỗi khi tìm kiếm: {e}")
            
            print("=" * 80 + "\n")
            
            # Hỏi người dùng có muốn chạy tiếp không để tránh trôi Terminal
            if idx % 3 == 0:
                cont = input("💡 Nhấn Enter để xem tiếp 3 câu nữa, hoặc gõ 'q' để thoát: ")
                if cont.strip().lower() == 'q':
                    break

    print("✅ Đã hoàn thành bài test Retriever!")

if __name__ == "__main__":
    main()
