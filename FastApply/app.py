from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import subprocess

from modules.parseDocument import parseDocument

app = Flask(__name__)

# Create directories for static files and templates
if not os.path.exists('static'):
    os.makedirs('static')
if not os.path.exists('templates'):
    os.makedirs('templates')

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the form submission
@app.route('/process', methods=['POST'])
def process():
    inputfile = 'inputs/shashank_reddy.docx' # Automate later
    data = request.get_json()
    job_description = data.get('job_description')

    # Programs takes old resume and job description gets new resume and saves file in outputs
    command = ['Python3', '-f', f'{inputfile}', '-jd', f'{job_description}']
    my_env = os.environ.copy()
    subprocess.Popen(command, env=my_env)
    

    return jsonify({
        'status': 'success',
        'message': 'Received job description',
        'data': job_description
    })

if __name__ == '__main__':
    app.run(debug=True)