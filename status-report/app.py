from flask import Flask, request, render_template, jsonify
import pandas as pd
import os

import modules.provider_data as provider_data
import modules.staff_data as staff_data
import modules.imm_data as imm_data

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "" or not file.filename.endswith(".csv"):
        return jsonify({"error": file.filename + " is an invalid file format."}), 400
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        if file.filename == 'HRSSA_Staff_Data.csv':
            staffData = staff_data.cleanStaffData(filepath)
            # return jsonify({"staffData": staffData})
            return {"staffData": staffData}

        elif file.filename == 'HRSSA_Provider_Data.csv':
            providerData = provider_data.cleanProviderData(filepath)
            return {"providerData": providerData}
        
        elif file.filename == 'HRSSA_Child_Licensing_Immunization.csv':
            immData = imm_data.cleanImmData(filepath)
            return {"immData": immData}
        else:
            return {"error": file.filename + " is not a recognized file name."}, 400
    except Exception as error:
        return jsonify({"error:", error}), 500
    finally:
        os.remove(filepath)
if __name__ == "__main__":
    app.run(debug=True)
