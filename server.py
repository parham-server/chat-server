from flask import Flask, request, jsonify

app = Flask(__name__)

messages = {}

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    user = data.get("user")
    content = data.get("message")

    if user and isinstance(content, dict):
        messages[user] = content
        return jsonify({"status": "received", "user": user})
    else:
        return jsonify({"status": "error", "message": "user not specified or message invalid"}), 400

@app.route('/delete_user', methods=['POST'])
def delete_user():
    data = request.json
    user = data.get("user")
    
    if user in messages:
        del messages[user]
        return jsonify({"status": "deleted", "user": user})
    else:
        return jsonify({"status": "not found", "user": user}), 404

@app.route('/rece', methods=['GET'])   
def get_messages():
    return jsonify(messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
