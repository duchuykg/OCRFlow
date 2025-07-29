@echo off
echo Installing Vietnamese language data for Tesseract...

REM Download Vietnamese language data
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/tesseract-ocr/tessdata/raw/main/vie.traineddata' -OutFile 'vie.traineddata'"

REM Find Tesseract installation directory
for %%i in ("C:\Program Files\Tesseract-OCR\tessdata" "C:\Program Files (x86)\Tesseract-OCR\tessdata") do (
    if exist "%%i" (
        echo Copying Vietnamese data to %%i
        copy "vie.traineddata" "%%i\"
        del "vie.traineddata"
        echo Vietnamese OCR language installed successfully!
        goto :done
    )
)

echo Could not find Tesseract installation directory
echo Please manually copy vie.traineddata to your Tesseract tessdata folder

:done
pause