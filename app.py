from flask import Flask, request, jsonify
from PIL import Image
import pytesseract

app = Flask(__name__)

def extract_text_from_image(img):
    # Ekstrak teks menggunakan Tesseract OCR
    # extracted_text = pytesseract.image_to_string(img)

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    extracted_text = pytesseract.image_to_string(img)
    return extracted_text


@app.route('/extract-text', methods=['POST', 'GET'])
def extract_text():
    try:
        if request.method == 'POST':
            # Dapatkan file gambar dari POST request
            file = request.files['image']
            
            # Simpan file gambar ke server
            image_path = 'uploaded_image.jpg'
            file.save(image_path)

            # Baca gambar dan ekstrak teks
            img = Image.open(image_path)
            extracted_text = extract_text_from_image(img)

            # Hapus file gambar yang diunggah
            img.close()
            file.close()
            remove_uploaded_image(image_path)

            return jsonify({'success': True, 'extracted_text': extracted_text})
        elif request.method == 'GET':
            # URL gambar sebagai parameter query
            image_url = request.args.get('image_url')
            
            # Baca gambar dari URL dan ekstrak teks
            img = Image.open(requests.get(image_url, stream=True).raw)
            extracted_text = extract_text_from_image(img)

            return jsonify({'success': True, 'extracted_text': extracted_text})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def remove_uploaded_image(image_path):
    import os
    os.remove(image_path)

if __name__ == '__main__':
    app.run(debug=True, port=7000)
