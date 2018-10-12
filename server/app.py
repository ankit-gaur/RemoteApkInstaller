import os
from werkzeug.utils import secure_filename
from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    Response
)

# Create the application instance
app = Flask(__name__, template_folder="templates")

is_app_updated = False

app_upload_path = os.path.join(app.instance_path, "apks")

if not os.path.exists(app_upload_path):
    os.makedirs(app_upload_path)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload_apk')
def upload_apk_web():
    return render_template("upload_apk.html")


@app.route('/api/upload_apk', methods=['POST'])
def upload_apk():
    global is_app_updated
    is_app_updated = True
    f = request.files["file"]
    f.save(os.path.join(app_upload_path, secure_filename(f.filename)))
    return "apk uploaded successfully"


@app.route('/api/is_app_updated')
def is_app_updated():
    global is_app_updated
    if(is_app_updated):
        response = '{"is_app_updated" : 1}'
    else:
        response = '{"is_app_updated" : 0}'
    return Response(response,status=200,mimetype="application/json")


@app.route('/api/get_apk', methods=['GET'])
def get_apk():
    # return "le apks"
    global is_app_updated
    is_app_updated = False
    return send_from_directory(app_upload_path, "debug.apk", as_attachment=True, attachment_filename="debug.apk")


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)

