"""TTomorrow Studio - bộ công cụ sửa video/ảnh chạy trên máy, gọi qua Claude Code."""

# Dùng kho chứng chỉ của hệ điều hành (kể cả CA do antivirus/công ty cài).
# Phải thực hiện trước khi Requests/urllib3 hay Hugging Face tạo SSL context.
try:
    import truststore

    truststore.inject_into_ssl()
except Exception:  # noqa: BLE001 - thiếu/lỗi truststore không được làm CLI ngừng chạy
    pass

__version__ = "1.0.0"
