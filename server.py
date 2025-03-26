from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)

# Cấu hình SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///keys.db"
db = SQLAlchemy(app)

# Mô hình lưu key trong database
class LicenseKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    key = db.Column(db.String(32), unique=True, nullable=False)

# Tạo database
with app.app_context():
    db.create_all()

# Hàm tạo key ngẫu nhiên
def generate_random_key():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=16))

# Trang chủ
@app.route("/")
def home():
    return render_template("index.html")

# API tạo key mới
@app.route("/generate_key", methods=["POST"])
def generate_key():
    data = request.json
    username = data.get("username")

    new_key = generate_random_key()
    license_entry = LicenseKey(username=username, key=new_key)
    db.session.add(license_entry)
    db.session.commit()

    return jsonify({"username": username, "key": new_key})

# API kiểm tra key
@app.route("/check_key", methods=["POST"])
def check_key():
    data = request.json
    username = data.get("username")
    user_key = data.get("key")

    license_entry = LicenseKey.query.filter_by(username=username, key=user_key).first()

    if license_entry:
        return jsonify({"status": "valid"})
    else:
        return jsonify({"status": "invalid"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
