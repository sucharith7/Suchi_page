from google.cloud import storage
import json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', github_link='https://github.com/sucharith7', linkedin_link='https://www.linkedin.com/in/sucharith-cherukumalli-30016a141/',resume_link='https://drive.google.com/file/d/1wUtpLrGR5rwQRCmfAVFSUd2DPigwppVC/view?usp=drive_link')

@app.route('/submit_enquiry', methods=['POST'])
def submit_enquiry():
    name = request.form.get('name')
    email = request.form.get('email')
    question = request.form.get('question')

    # Load existing data
    storage_client = storage.Client()
    bucket = storage_client.bucket('sucharith_target')
    blob = bucket.blob('config.json')
    try:
        data = json.loads(blob.download_as_text())
    except (AttributeError, json.JSONDecodeError):
        data = []

    # Append new enquiry
    data.append({
        'name': name,
        'email': email,
        'question': question
    })

    # Save data
    blob.upload_from_string(json.dumps(data))
        
    return 'Thank you for your enquiry!'

if __name__ == '__main__':
    app.run(debug=True)