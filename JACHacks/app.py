from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from werkzeug.utils import secure_filename
import os
from getTextPDF import *
from main import getsentences, gemini
from topics_excavator import topics_excavator

app = Flask(__name__)

# Configure upload folder (adjust as needed)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Function to check allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Check if file is selected
        if 'file' not in request.files:
            flash('No file selected!')
            return redirect(url_for('index'))

        file = request.files['file']
        # Check if file has a filename
        if file.filename == '':
            flash('No selected file!')
            return redirect(url_for('index'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            flash('File uploaded successfully! Filename: ' + filename, 'info')

            # Get the list of all files in the uploads folder
            existing_files = os.listdir(app.config['UPLOAD_FOLDER'])

            # Delete all existing files (assuming only one file is allowed)
            for existing_file in existing_files:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], existing_file)
                os.remove(filepath)

            # Save the file with a new name "file.pdf"
            new_filename = "file.pdf"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

            file.save(filepath)
            flash('File uploaded and renamed successfully!', 'success')

            text = pdf_reader(filepath)
            topic = topics_excavator(text)
            result = getsentences(text, topic)

            answer = gemini(text, result)
            print(answer)

            # Save the result to a PDF file
            save_result_to_txt(answer)

            return redirect(url_for('download_file'))
        else:
            flash('Invalid file type!')
            return redirect(url_for('index'))

    return render_template('index.html')


def save_result_to_txt(result):
    # Join all sentences in result into a single string
    # result_text = ' '.join(result)

    # Write the result text to a .txt file
    with open("./uploads/result.txt", "w") as text_file:
        text_file.write(result)


@app.route('/download')
def download_file():
    # Specify the filename
    filename = "result.txt"
    # Send the file to the user
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# Access the secret key from environment variable
app.config['SECRET_KEY'] = 'theOnePieceIsReal'

if __name__ == '__main__':
    app.run(debug=True)
