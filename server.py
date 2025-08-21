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
cursor_pass = conn.cursor()

# ایجاد جدول users
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

# ایجاد جدول user_passwords
cursor_pass.execute("""
CREATE TABLE IF NOT EXISTS user_passwords (
    passworda TEXT PRIMARY KEY,
    pass1 TEXT,
    pass2 TEXT,
    pass3 TEXT,
    pass4 TEXT,
    pass5 TEXT,
    passcall TEXT,
    passdelete TEXT,
    passedit TEXT
)
""")
conn.commit()


# ---------------------------
# مسیر ذخیره یا آپدیت اطلاعات کاربر
# ---------------------------
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


# ---------------------------
# مسیر ذخیره یا آپدیت پسورد کاربر
# ---------------------------
@app.route("/sendpass", methods=["POST"])
def save_user_password():
    data = request.json.get("message", {})
    passworda = request.json.get("user")

    if not passworda or not data:
        return jsonify({"error": "Invalid data"}), 400

    cursor_pass.execute("DELETE FROM user_passwords WHERE passworda = %s", (passwords,))
    cursor_pass.execute("""
        INSERT INTO user_passwords VALUES (
        %(pass1)s, %(pass2)s, %(pass3)s, %(pass4)s, %(pass5)s, %(passcall)s, %(passdelete)s, %(passedit)s
        )
    """, {"passworda": passworda, **data})
    conn.commit()
    return jsonify({"status": "ok"})


# ---------------------------
# مسیر حذف کاربر
# ---------------------------
@app.route("/delete/<f_name>", methods=["DELETE"])
def delete_user(f_name):
    cursor.execute("SELECT * FROM users WHERE f_name = %s", (f_name,))
    if cursor.fetchone() is None:
        return jsonify({"error": "User not found"}), 404

    cursor.execute("DELETE FROM users WHERE f_name = %s", (f_name,))
    conn.commit()
    return jsonify({"status": f"User '{f_name}' deleted successfully"})


# ---------------------------
# مسیر حذف پسورد کاربر
# ---------------------------
@app.route("/deletepass/<passworda>", methods=["DELETE"])
def delete_user_password(passworda):
    cursor_pass.execute("SELECT * FROM user_passwords WHERE passwords = %s", (passwords,))
    if cursor_pass.fetchone() is None:
        return jsonify({"error": "Password not found"}), 404

    cursor_pass.execute("DELETE FROM user_passwords WHERE passwords = %s", (passwords,))
    conn.commit()
    return jsonify({"status": f"Password '{passwords}' deleted successfully"})


# ---------------------------
# مسیر دریافت تمام کاربران
# ---------------------------
@app.route("/rece", methods=["GET"])
def get_all_users():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    data = {row["f_name"]: row for row in rows}
    return jsonify(data)


# ---------------------------
# مسیر دریافت تمام پسوردها
# ---------------------------
@app.route("/recepass", methods=["GET"])
def get_all_passwords():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM user_passwords")
    rows = cur.fetchall()
    data = {row["passwords"]: row for row in rows}
    return jsonify(data)


# ---------------------------
# اجرای سرور
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # تغییر پورت


