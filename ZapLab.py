from flask import Flask, render_template, request, jsonify
import webview
import os

app = Flask(__name__)

# Store the current project directory
current_directory = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save():
    global current_directory
    data = request.json
    filename = data.get("filename", "untitled.txt")
    content = data.get("content", "")

    if current_directory:
        file_path = os.path.join(current_directory, filename)
        with open(file_path, 'w') as f:
            f.write(content)
        return jsonify({"status": "success", "message": f"File '{filename}' saved."})
    return jsonify({"status": "error", "message": "No directory selected."})

@app.route("/open/<filename>", methods=["GET"])
def open_file(filename):
    global current_directory
    if current_directory:
        file_path = os.path.join(current_directory, filename)
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return jsonify({"status": "success", "content": content})
        except FileNotFoundError:
            return jsonify({"status": "error", "message": "File not found."})
    return jsonify({"status": "error", "message": "No directory selected."})

@app.route("/set_directory", methods=["POST"])
def set_directory():
    global current_directory
    directory = request.json.get("directory")
    if os.path.isdir(directory):
        current_directory = directory
        files = os.listdir(directory)
        return jsonify({"status": "success", "files": files})
    return jsonify({"status": "error", "message": "Invalid directory."})

def start_app():
    webview.create_window('Code Editor', app, width=800, height=600)
    webview.start()

if __name__ == "__main__":
    start_app()
