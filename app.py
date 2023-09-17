import os
from flask import Flask, request, render_template
import boto3
import tempfile
from src.transcribe import upload_file
from src.standard import extract_audio, speech_to_text, generate_timestamps
# from src.standard import extract_audio, speech_to_text, generate_timestamps
app = Flask(__name__)

# AWS S3 configuration (replace with your own)
S3_BUCKET = 'storevdos'
s3_key = ''
filename = " "


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():

    global filename
    file = request.files['file']
    # If file name is empty then return no file selected
    if file.filename == '':
        return jsonify({'result': 'No file selected.'})

    # Inserted images
    allowed_extensions = {'mp4'}
    if file and file.filename.lower().rsplit('.', 1)[1] in allowed_extensions:
        filename = file.filename
        image_path = os.path.join("uploaded_vdos", filename)
        with open(image_path, "wb") as f:
            f.write(file.read())
    filename = image_path

    return render_template('index.html',results=f"Video uploaded")

    # if 'file' not in request.files:
    #     return "No file part"

    # file = request.files['file']

    # # Check if a file was selected
    # if file.filename == '':
    #     return "No selected file"

    # # Create a temporary file to store the uploaded data
    # global s3_key
    # with tempfile.NamedTemporaryFile(delete=False) as temp_file:
    #     file.save(temp_file.name)
    #     temp_file.close()
        
    #     # Generate a unique S3 key for the uploaded file
    #     s3_key = 'videos/' + file.filename

    #     # Upload the video file to S3
    #     response = upload_file(temp_file.name, S3_BUCKET, s3_key)
    
    # os.remove(temp_file.name)  # Remove the temporary file
    # return render_template('index.html',results=f"Video uploaded to S3: s3://{S3_BUCKET}/{s3_key}")

@app.route('/premium', methods=['POST'])
def action():
    print(s3_key)
    job_name = "minutes" # Change this to your desired job name
    job_uri = f"s3://{S3_BUCKET}/{s3_key}"  # Change this to the S3 URI of your audio file
    output_bucket = "storevdos"  # Change this to your desired output S3 bucket
    language_code = "en-US"  # Change this to the language code of your audio (e.g., "en-US" for English)

    settings = {
        "ChannelIdentification": False,
        "ShowSpeakerLabels": True,
        "MaxSpeakerLabels": 2
    }

    transcribe_client = boto3.client('transcribe')
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=language_code,
        MediaFormat="mp4",
        Media={
            "MediaFileUri": job_uri
        },
        OutputBucketName=output_bucket,
        Settings=settings
    )
    while True:
        response = transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name
        )
        status = response['TranscriptionJob']['TranscriptionJobStatus']
        if status in ['COMPLETED', 'FAILED']:
            break
        print("Transcription job status: {}".format(status))

    return render_template('index.html',results1="transcribed successfully")

@app.route('/standard', methods=['POST'])
def standard():
    extract_audio(filename, f'{filename}_output.wav')
    speech_to_text(f'{filename}_output.wav', f'{filename}_output.txt')
    generate_timestamps(f'{filename}_output.wav', f'{filename}_output.txt')

    return render_template('index.html',results1="transcribed successfully and generated output")

@app.route('/batch', methods=['POST'])
def download_file(filename):
    # Construct the file path
    file_path = os.path.join(app.root_path, 'uploads', filename)

    # Serve the file to the user
    return send_file(file_path, as_attachment=True)
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
