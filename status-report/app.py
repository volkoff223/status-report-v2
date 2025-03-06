from flask import Flask, request, render_template, jsonify
import pandas as pd
import os
from werkzeug.utils import secure_filename

import modules.provider as provider_data
import modules.staff as staff_data
import modules.imm as imm_data
import modules.bgreport as bgreport_data
import modules.balance as balance_data
import modules.enrollment as enrol_data

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
IMG_FOLDER = "static/img"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(IMG_FOLDER, exist_ok=True)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/list-images")
def list_images():
    try:
        images = [f for f in os.listdir(IMG_FOLDER) if f.lower().endswith(tuple(f'.{ext}' for ext in ALLOWED_EXTENSIONS))]
        return jsonify(images)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/upload-image", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    
    if image.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if image and allowed_file(image.filename):
        # Secure the filename to prevent directory traversal
        filename = secure_filename(image.filename)
        
        # Ensure unique filename if needed
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(IMG_FOLDER, filename)):
            filename = f"{base}_{counter}{ext}"
            counter += 1
        
        # Save the file
        filepath = os.path.join(IMG_FOLDER, filename)
        image.save(filepath)
        
        return jsonify({"message": "Image uploaded successfully", "filename": filename})
    
    return jsonify({"error": "Invalid file type"}), 400

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
            return {"staffData": staffData}

        elif file.filename == 'HRSSA_Provider_Data.csv':
            providerData = provider_data.cleanProviderData(filepath)
            return {"providerData": providerData}
        
        elif file.filename == 'HRSSA_Child_Licensing_Immunization.csv':
            immData = imm_data.cleanImmData(filepath)
            return {"immData": immData}
        
        elif file.filename == 'Background_Check_Report.csv':
            bgdata = bgreport_data.cleanBGData(filepath)
            return {"bgdata" : bgdata}
        
        elif file.filename == 'HRSSA_Ledger_Transactions.csv':
            balanceData = balance_data.cleanBalanceData(filepath)
            return {"balanceData": balanceData}
        
        elif file.filename == 'HRSSA_Enrollment.csv':
            enrolData = enrol_data.cleanEnrolData(filepath)
            return {"enrolData": enrolData}
        else:
            return {"error": file.filename + " is not a recognized file name."}, 400
    except Exception as error:
        return jsonify({"error:", error}), 500
    finally:
        os.remove(filepath)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)