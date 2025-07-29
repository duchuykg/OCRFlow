from flask import Flask, request, jsonify
from flask_cors import CORS
from markitdown import MarkItDown
import os
import tempfile
from werkzeug.utils import secure_filename
from PIL import Image
import pdfplumber
from docx import Document
import openpyxl
from pptx import Presentation

# Try to import Tesseract
try:
    import pytesseract
    # Uncomment and set correct path if needed:
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    TESSERACT_AVAILABLE = True
    print("Tesseract OCR is available")
except ImportError:
    TESSERACT_AVAILABLE = False
    print("Tesseract not available - install for image/scan OCR")

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'pptx', 'xlsx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_fallback(file_path, file_extension):
    """Fallback text extraction methods if MarkItDown fails"""
    print(f"Trying fallback for file: {file_path}, extension: {file_extension}")
    try:
        if file_extension.lower() in ['.png', '.jpg', '.jpeg', '.gif']:
            # OCR for images
            if not TESSERACT_AVAILABLE:
                return "Tesseract OCR not installed. See INSTALL_OCR.md for setup instructions."
            
            try:
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image, lang='eng')
                return text if text.strip() else "No text found in image."
            except Exception as e:
                return f"OCR failed: {str(e)}"
        
        elif file_extension.lower() == '.pdf':
            # PDF text extraction
            print("Attempting PDF text extraction...")
            text = ""
            try:
                with pdfplumber.open(file_path) as pdf:
                    print(f"PDF has {len(pdf.pages)} pages")
                    for page_num, page in enumerate(pdf.pages):
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                            print(f"Page {page_num + 1} extracted {len(page_text)} characters")
                
                print(f"Total PDF text length: {len(text)}")
                
                if not text.strip():
                    if TESSERACT_AVAILABLE:
                        return "This PDF contains scanned content. OCR for PDF scans is not implemented yet. Try converting PDF pages to images first."
                    else:
                        return "This PDF contains scanned content. Install Tesseract OCR (see INSTALL_OCR.md) to extract text from scanned PDFs."
                
                return text
            except Exception as e:
                print(f"PDF extraction error: {e}")
                return f"Error reading PDF: {str(e)}"
        
        elif file_extension.lower() == '.docx':
            # Word document
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        
        elif file_extension.lower() == '.xlsx':
            # Excel file
            workbook = openpyxl.load_workbook(file_path)
            text = ""
            for sheet_name in workbook.sheetnames:
                sheet = workbook[sheet_name]
                text += f"Sheet: {sheet_name}\n"
                for row in sheet.iter_rows(values_only=True):
                    row_text = "\t".join([str(cell) if cell is not None else "" for cell in row])
                    if row_text.strip():
                        text += row_text + "\n"
                text += "\n"
            return text
        
        elif file_extension.lower() == '.pptx':
            # PowerPoint
            prs = Presentation(file_path)
            text = ""
            for slide_num, slide in enumerate(prs.slides, 1):
                text += f"Slide {slide_num}:\n"
                for shape in slide.shapes:
                    if hasattr(shape, 'text'):
                        text += shape.text + "\n"
                text += "\n"
            return text
        
        elif file_extension.lower() == '.txt':
            # Plain text
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
    
    except Exception as e:
        print(f"Fallback extraction failed: {e}")
        return None
    
    return None

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'OCR API is running'})

@app.route('/api/convert', methods=['POST'])
def convert_document():
    temp_file_path = None
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Create a temporary file
            temp_fd, temp_file_path = tempfile.mkstemp(suffix=os.path.splitext(filename)[1])
            try:
                # Write file data to temporary file
                with os.fdopen(temp_fd, 'wb') as temp_file:
                    file.save(temp_file)
                
                # Initialize MarkItDown
                md = MarkItDown()
                
                # Convert the document
                result = md.convert(temp_file_path)
                
                # Get extracted text
                extracted_text = result.text_content if result.text_content else ""
                
                # Debug logging
                print(f"MarkItDown result length: {len(extracted_text)}")
                
                # If MarkItDown failed, try fallback methods
                if not extracted_text.strip():
                    print("MarkItDown failed, trying fallback methods...")
                    extracted_text = extract_text_fallback(temp_file_path, os.path.splitext(filename)[1])
                    if extracted_text:
                        print(f"Fallback extraction successful, length: {len(extracted_text)}")
                    else:
                        print("Fallback extraction also failed")
                        extracted_text = "No text could be extracted from this file."
                
                return jsonify({
                    'success': True,
                    'text': extracted_text,
                    'filename': filename
                })
            finally:
                # Clean up temporary file
                if temp_file_path and os.path.exists(temp_file_path):
                    try:
                        os.unlink(temp_file_path)
                    except:
                        pass  # Ignore cleanup errors
        
        return jsonify({'error': 'File type not allowed'}), 400
        
    except Exception as e:
        # Clean up temporary file in case of error
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except:
                pass
        return jsonify({'error': str(e)}), 500

@app.route('/api/supported-formats', methods=['GET'])
def supported_formats():
    return jsonify({
        'formats': list(ALLOWED_EXTENSIONS),
        'description': 'Supported file formats for OCR conversion'
    })

@app.route('/api/test-ocr', methods=['GET'])
def test_ocr():
    """Test OCR functionality"""
    try:
        # Test Tesseract
        import subprocess
        result = subprocess.run(['tesseract', '--version'], capture_output=True, text=True)
        tesseract_version = result.stdout.split('\n')[0] if result.returncode == 0 else "Not found"
        
        return jsonify({
            'tesseract_available': result.returncode == 0,
            'tesseract_version': tesseract_version,
            'markitdown_available': True
        })
    except Exception as e:
        return jsonify({
            'tesseract_available': False,
            'error': str(e),
            'markitdown_available': True
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)