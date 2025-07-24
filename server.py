from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'

# اگر فایل وجود دارد، آن را بخوان
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        messages = json.load(f)
else:
    messages = {}

def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    user = data.get("user")
    content = data.get("message")

    if user and isinstance(content, dict):
        messages[user] = content
        save_data()  # بعد از تغییر، ذخیره در فایل
        return jsonify({"status": "received", "user": user})
    else:
        return jsonify({"status": "error", "message": "user not specified or message invalid"}), 400

@app.route('/delete_user', methods=['POST'])
def delete_user():
    data = request.json
    user = data.get("user")
    
    if user in messages:
        del messages[user]
        save_data()  # بعد از حذف، ذخیره در فایل
        return jsonify({"status": "deleted", "user": user})
    else:
        return jsonify({"status": "not found", "user": user}), 404

@app.route('/rece', methods=['GET'])
def get_messages():
    return jsonify(messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
