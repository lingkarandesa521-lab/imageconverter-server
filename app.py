import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "ImageConverter Server is running!"

@app.route("/convert", methods=["POST"])
def convert():
    api_key = os.environ.get("JUSTVECTORIZE_API_KEY")

    if not api_key:
        return jsonify({"error": "API key belum dipasang di server"}), 500

    uploaded_file = request.files.get("file")
    output_format = request.form.get("format", "svg").lower()

    if not uploaded_file:
        return jsonify({"error": "Gambar belum dikirim"}), 400

    if output_format not in ["svg", "eps", "png"]:
        return jsonify({"error": "Format tidak didukung"}), 400

    try:
        response = requests.post(
            "https://api.justvectorize.com/api/v1/vectorize",
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": (
                uploaded_file.filename,
                uploaded_file.stream,
                uploaded_file.mimetype
            )},
            data={"format": output_format},
            timeout=120
        )

        response.raise_for_status()
        result = response.json()

        return jsonify({"fileUrl": result.get("fileUrl")})

    except requests.RequestException as error:
        return jsonify({"error": str(error)}), 502

