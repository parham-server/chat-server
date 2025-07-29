from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

# اتصال به دیتابیس PostgreSQL از طریق متغیرهای محیطی
conn = psycopg2.connect(
    host='dpg-d2381femcj7s73d8sbdg-a',
    database='parham',
    user='parham_user',
    password='ku5Ke7mDuTlAvCMWXy7KeTO6DwArAWtl',
    port=5432
)
cursor = conn.cursor()

# ایجاد جدول اگر وجود ندارد
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

@app.route("/send", methods=["POST"])
def save_user():
    data = request.json.get("message", {})
    f_name = request.json.get("user")

    if not f_name or not data:
        return jsonify({"error": "Invalid data"}), 400

    # حذف اگر تکراری بود
    cursor.execute("DELETE FROM users WHERE f_name = %s", (f_name,))
    
    # درج اطلاعات
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

@app.route("/rece", methods=["GET"])
def get_all_users():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    data = {row["f_name"]: row for row in rows}
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
