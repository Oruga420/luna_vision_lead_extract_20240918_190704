import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from image_processor import process_images

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        if 'files[]' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        files = request.files.getlist('files[]')
        
        if not files or files[0].filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        filenames = []
        for file in files:
            if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                filenames.append(file_path)
        
        if not filenames:
            return jsonify({'error': 'No valid images uploaded'}), 400
        
        csv_path = process_images(filenames)
        
        if csv_path is None:
            return jsonify({'error': 'Failed to process images'}), 500
        
        return jsonify({'message': 'Files processed successfully', 'csv_path': csv_path}), 200
    except Exception as e:
        app.logger.error(f"Error processing upload: {str(e)}")
        return jsonify({'error': 'An error occurred while processing the upload'}), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

@app.errorhandler(Exception)
def handle_exception(e):
    # Log the error for debugging
    app.logger.error(f"Unhandled exception: {str(e)}")
    # Return JSON response
    return jsonify({"error": "An internal server error occurred"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
