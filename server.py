from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# اتصال به دیتابیس PostgreSQL
conn = psycopg2.connect(
    host='dpg-d2381femcj7s73d8sbdg-a',
    database='parham',
    user='parham_user',
    password='ku5Ke7mDuTlAvCMWXy7KeTO6DwArAWtl',
    port=5432
)
cursor = conn.cursor()

# ایجاد جدول users اگر وجود نداشت
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    f_name TEXT PRIMARY KEY,
    Name TEXT,
    Email TEXT,
    tel TEXT,
    birth_d TEXT,
    inter_d TEXT,
    tamid_d TEXT,
    profession TEXT,
    khedmat_r TEXT,
    tel_code TEXT,
    instagram TEXT,
    khedmat1 TEXT,
    khedmat_v1 TEXT,
    khedmat_p1 TEXT,
    khedmat2 TEXT,
    khedmat_v2 TEXT,
    khedmat_p2 TEXT,
    khedmat3 TEXT,
    khedmat_v3 TEXT,
    khedmat_p3 TEXT,
    letter1 TEXT,
    letter2 TEXT,
    letter3 TEXT
)
""")
conn.commit()

# ایجاد جدول جدید برای پسوردها (حداقل 5 رمز)
cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    passwords TEXT PRIMARY KEY,
    password1 TEXT,
    password2 TEXT,
    password3 TEXT,
    password4 TEXT,
    password5 TEXT
)
""")
conn.commit()

# مسیر ذخیره یا آپدیت اطلاعات کاربر
@app.route("/send", methods=["POST"])
def save_user():
    data = request.json.get("message", {})
    f_name = request.json.get("user")

    if not f_name or not data:
        return jsonify({"error": "Invalid data"}), 400

    cursor.execute("DELETE FROM users WHERE f_name = %s", (f_name,))
    cursor.execute("""
        INSERT INTO users VALUES (
            %(f_name)s, %(Name)s, %(Email)s, %(tel)s,
            %(birth_d)s, %(inter_d)s, %(tamid_d)s, %(profession)s,
            %(khedmat_r)s, %(tel_code)s, %(instagram)s,
            %(khedmat1)s, %(khedmat_v1)s, %(khedmat_p1)s,
            %(khedmat2)s, %(khedmat_v2)s, %(khedmat_p2)s,
            %(khedmat3)s, %(khedmat_v3)s, %(khedmat_p3)s,
            %(letter1)s, %(letter2)s, %(letter3)s
        )
    """, {"f_name": f_name, **data})
    conn.commit()
    return jsonify({"status": "ok"})

# مسیر حذف کاربر
@app.route("/delete/<f_name>", methods=["DELETE"])
def delete_user(f_name):
    cursor.execute("SELECT * FROM users WHERE f_name = %s", (f_name,))
    if cursor.fetchone() is None:
        return jsonify({"error": "User not found"}), 404

    cursor.execute("DELETE FROM users WHERE f_name = %s", (f_name,))
    conn.commit()
    return jsonify({"status": f"User '{f_name}' deleted successfully"})

# مسیر دریافت تمام کاربران
@app.route("/rece", methods=["GET"])
def get_all_users():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    data = {row["f_name"]: row for row in rows}
    return jsonify(data)

# مسیر افزودن یا آپدیت رمزها
@app.route("/save_passwords", methods=["POST"])
def save_passwords():
    data = request.get_json()
    passwords_key = data.get("passwords")  # این شناسه برای شناسایی ردیف پسورد
    password1 = data.get("password1", "")
    password2 = data.get("password2", "")
    password3 = data.get("password3", "")
    password4 = data.get("password4", "")
    password5 = data.get("password5", "")

    if not passwords_key:
        return jsonify({"error": "Missing passwords key"}), 400

    cursor.execute("DELETE FROM passwords WHERE passwords = %s", (passwords_key,))
    cursor.execute("""
        INSERT INTO passwords (passwords, password1, password2, password3, password4, password5)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (passwords_key, password1, password2, password3, password4, password5))
    conn.commit()
    return jsonify({"status": "passwords saved"})

# مسیر دریافت پسوردها
@app.route("/get_passwords", methods=["GET"])
def get_passwords():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM passwords")
    rows = cur.fetchall()
    return jsonify(rows)

# حذف پسورد با شناسه
@app.route("/delete_passwords/<passwords_key>", methods=["DELETE"])
def delete_passwords(passwords_key):
    cursor.execute("SELECT * FROM passwords WHERE passwords = %s", (passwords_key,))
    if cursor.fetchone() is None:
        return jsonify({"error": "Passwords not found"}), 404

    cursor.execute("DELETE FROM passwords WHERE passwords = %s", (passwords_key,))
    conn.commit()
    return jsonify({"status": f"Passwords with key '{passwords_key}' deleted"})

# اجرای سرور
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5432)
