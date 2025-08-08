# 플라스크 사용
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import jwt, datetime, os

SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD", "test_password")
JWT_SECRET = os.getenv("JWT_SECRET", "test_secret")

app = Flask(__name__)
SECRET_KEY = "verysecret"  # 실제 서비스라면 환경변수로

# 가짜 사용자 DB
users = {
    "user": {"password": "userpass", "role": "user"},
    "admin": {"password": "adminpass", "role": "admin"}
}

# @app.route("/")
# def index():
#     return "Hello from Flask! Login page will be here."
@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username in users and users[username]["password"] == password:
        token = jwt.encode({
            "user": username,
            "role": users[username]["role"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        }, SECRET_KEY, algorithm="HS256")

        resp = make_response(redirect(url_for("user_page")))
        resp.set_cookie("access_token", token)
        return resp

    return "Invalid credentials", 401

@app.route("/user")
def user_page():
    token = request.cookies.get("access_token")
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return "Invalid or expired token", 401

    return render_template("user.html", role=decoded["role"])

@app.route("/admin")
def admin_page():
    token = request.cookies.get("access_token")
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if decoded.get("role") != "admin":
            return "Access denied", 403
    except:
        return "Invalid or expired token", 401

    return render_template("admin.html")

# 관리자 전용 API
@app.route("/admin/data")
def admin_data():
    token = request.cookies.get("access_token")
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if decoded.get("role") != "admin":
            return jsonify({"error": "Access denied"}), 403
    except:
        return jsonify({"error": "Invalid token"}), 401

    return jsonify({"flag": "CTF{admin_access_granted}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
