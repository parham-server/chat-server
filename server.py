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

# ایجاد جدول user_passworda
cursor_pass.execute("""
CREATE TABLE IF NOT EXISTS user_passworda (
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
# ذخیره یا آپدیت اطلاعات کاربر
# ---------------------------
@app.route("/send", methods=["POST"])
def save_user():
    data = request.json.get("message", {})
    f_name = request.json.get("user")

    if not f_name or not data:
        return jsonify({"error": "Invalid data"}), 400

    try:
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
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


# ---------------------------
# ذخیره یا آپدیت پسورد کاربر
# ---------------------------
@app.route("/sendpass", methods=["POST"])
def save_user_password():
    data = request.json.get("message", {})
    passworda = request.json.get("user")

    if not passworda or not isinstance(data, dict):
        return jsonify({"error": "Invalid data"}), 400

    try:
        # ستون‌های معتبر جدول
        all_columns = ["pass1","pass2","pass3","pass4","pass5","passcall","passdelete","passedit"]

        # آماده کردن داده فقط برای ستون‌های معتبر
        update_data = {col: data[col] for col in all_columns if col in data}

        if not update_data:
            return jsonify({"error": "No valid columns to update"}), 400

        # بررسی اینکه رکورد وجود دارد یا نه
        cursor_pass.execute("SELECT 1 FROM user_passworda WHERE passworda = %s", (passworda,))
        exists = cursor_pass.fetchone()

        if exists:
            # آپدیت فقط ستون‌های فرستاده شده
            set_clause = ", ".join([f"{col} = %({col})s" for col in update_data])
            query = f"UPDATE user_passworda SET {set_clause} WHERE passworda = %(passworda)s"
            cursor_pass.execute(query, {"passworda": passworda, **update_data})
        else:
            # رکورد وجود ندارد → درج همه ستون‌ها، ستون‌هایی که ارسال نشده خالی می‌شوند
            insert_data = {col: data.get(col, "") for col in all_columns}
            insert_data["passworda"] = passworda
            cols = ", ".join(insert_data.keys())
            vals = ", ".join([f"%({col})s" for col in insert_data])
            query = f"INSERT INTO user_passworda ({cols}) VALUES ({vals})"
            cursor_pass.execute(query, insert_data)

        conn.commit()
        return jsonify({"status": "ok"})
    except Exception as e:
        conn.rollback()
        # چاپ خطا در کنسول سرور برای دیباگ
        print("Error in /sendpass:", e)
        return jsonify({"error": str(e)}), 500

# ---------------------------
# حذف کاربر
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
# حذف پسورد کاربر
# ---------------------------
@app.route("/deletepass/<passworda>", methods=["DELETE"])
def delete_user_password(passworda):
    cursor_pass.execute("SELECT * FROM user_passworda WHERE passworda = %s", (passworda,))
    if cursor_pass.fetchone() is None:
        return jsonify({"error": "Password not found"}), 404

    cursor_pass.execute("DELETE FROM user_passworda WHERE passworda = %s", (passworda,))
    conn.commit()
    return jsonify({"status": f"Password '{passworda}' deleted successfully"})


# ---------------------------
# دریافت تمام کاربران
# ---------------------------
@app.route("/rece", methods=["GET"])
def get_all_users():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    data = {row["f_name"]: row for row in rows}
    return jsonify(data)


# ---------------------------
# دریافت تمام پسوردها
# ---------------------------
@app.route("/recepass", methods=["GET"])
def get_all_passworda():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM user_passworda")
    rows = cur.fetchall()
    
    # اضافه کردن لاگ برای بررسی رکوردها
    print("rows from user_passworda:", rows)
    
    if not rows:
        return jsonify({})
    
    data = {}
    for row in rows:
        # مطمئن می‌شیم کلید وجود داره
        key = row.get("passworda")
        if key:
            data[key] = row
    return jsonify(data)



# ---------------------------
# اجرای سرور
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)




