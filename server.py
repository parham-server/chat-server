from flask import Flask, request, jsonify

app = Flask(__name__)

# ساختار جدید: دیکشنری اصلی برای ذخیره اطلاعات
messages = {}

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    user = data.get("user")       # مثلاً: "parham"
    content = data.get("message") # مثلاً: "salam"

    if user:
        # اگر این کاربر قبلاً نبود، اضافه کن
        if user not in messages:
            messages[user] = []

        # پیام جدید را به لیست پیام‌های آن کاربر اضافه کن
        messages[user].append(content)

        return jsonify({"status": "received", "user": user})
    else:
        return jsonify({"status": "error", "message": "user not specified"}), 400

@app.route('/rece', methods=['GET'])
def get_messages():
    return jsonify(messages)


@app.route('/delete_msg', methods=['POST'])
def delete_message():
    data = request.json
    user = data.get("user")
    message_to_delete = data.get("message")

    if user in messages:
        try:
            messages[user].remove(message_to_delete)
            return jsonify({"status": "message deleted", "user": user})
        except ValueError:
            return jsonify({"status": "message not found"}), 404
    else:
        return jsonify({"status": "user not found"}), 404



@app.route('/delete_user', methods=['POST'])
def delete_user():
    data = request.json
    user = data.get("user")

    if user in messages:
        del messages[user]
        return jsonify({"status": "deleted", "user": user})
    else:
        return jsonify({"status": "not found", "user": user}), 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
