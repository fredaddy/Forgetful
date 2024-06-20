from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from google.cloud import storage
from config import Config
from flask_sqlalchemy import SQLAlchemy
from utils.email_scheduler import scheduler

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

storage_client = storage.Client()
bucket = storage_client.bucket(app.config['GCLOUD_STORAGE_BUCKET'])

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(256), nullable=False)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        blob = bucket.blob(filename)
        blob.upload_from_file(file)
        url = blob.public_url
        new_file = File(filename=filename, url=url)
        db.session.add(new_file)
        db.session.commit()
        return redirect(url_for('upload_form'))
    return "No file uploaded", 400

if __name__ == "__main__":
    scheduler.start()  # Start the scheduler
    app.run(debug=True)
