# OCR Document Converter

A Python + React application that uses Microsoft's MarkItDown library to convert documents to text format.

## Features

- Convert PDF, images, Word, PowerPoint, and Excel files to text
- Drag and drop file upload interface
- Real-time conversion with progress indicator
- Copy converted text to clipboard
- Responsive web interface

## Setup

### Backend (Python Flask)

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend (React)

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000` and proxy API requests to the backend.

## Supported File Formats

- **Text**: .txt
- **PDF**: .pdf
- **Images**: .png, .jpg, .jpeg, .gif
- **Microsoft Office**: .docx, .pptx, .xlsx

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/convert` - Convert uploaded file to text
- `GET /api/supported-formats` - Get list of supported file formats

## Usage

1. Start both backend and frontend servers
2. Open your browser to `http://localhost:3000`
3. Upload a file by dragging and dropping or clicking to select
4. Click "Convert to Text" to process the file
5. Copy the converted text using the "Copy Text" button

## Dependencies

### Backend
- Flask - Web framework
- MarkItDown - Document conversion library
- Flask-CORS - Cross-origin resource sharing
- Pillow - Image processing

### Frontend
- React with TypeScript
- Modern responsive CSS design# OCRFlow
