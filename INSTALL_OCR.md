# Cài đặt OCR cho PDF scan và hình ảnh

## Cách 1: Cài Tesseract (Khuyến nghị)

### Windows:
1. Tải Tesseract từ: https://github.com/UB-Mannheim/tesseract/wiki
2. Chạy file .exe và cài đặt
3. Thêm vào system PATH hoặc uncomment dòng trong `backend/app.py`:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

### Với Chocolatey:
```bash
choco install tesseract
```

### Với winget:
```bash
winget install UB-Mannheim.TesseractOCR
```

## Cách 2: Thêm Tesseract vào requirements

Thêm vào `backend/requirements.txt`:
```
pytesseract==0.3.10
```

Sau đó:
```bash
cd backend
pip install pytesseract
```

## Test OCR

Sau khi cài xong, restart backend server và thử upload PDF scan hoặc hình ảnh.

## Ghi chú

- **Text-based PDF**: Hoạt động ngay không cần OCR
- **Scanned PDF/Images**: Cần Tesseract
- **Word/Excel/PowerPoint**: Hoạt động ngay