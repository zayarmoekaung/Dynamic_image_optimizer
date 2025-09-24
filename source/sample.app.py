from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Hello, Dynamic Image Optimizer!</h1><p>Upload an image to get started.</p>'

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs('uploads', exist_ok=True)
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename, 'path': filepath})
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/optimize', methods=['POST'])
def optimize():
    filename = request.form.get('filename')
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400
    
    upload_path = os.path.join('uploads', filename)
    if not os.path.exists(upload_path):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        img = Image.open(upload_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        width, height = img.size
        max_width = 800
        if width > max_width:
            ratio = max_width / width
            new_height = int(height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        os.makedirs('optimized', exist_ok=True)
        base_name = os.path.splitext(filename)[0]
        optimized_filename = f"{base_name}_optimized.jpg"
        optimized_path = os.path.join('optimized', optimized_filename)
        img.save(optimized_path, 'JPEG', quality=80)
        
        return jsonify({'message': 'Image optimized successfully', 'optimized_filename': optimized_filename, 'path': optimized_path})
    except Exception as e:
        return jsonify({'error': f'Optimization failed: {str(e)}'}), 500

if __name__ == '__main__':
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Route not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)