# Auto install required modules
import subprocess
import sys

required_modules = ["flask", "pywhatkit"]
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

# After ensuring modules are installed
from flask import Flask, render_template_string, request
import pywhatkit
import time
import datetime
import os

app = Flask(__name__)

# HTML template string
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>❤️ THE LEGEND PRINCE INSIDE ❤️</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            width: 400px;
            text-align: center;
        }
        .container h1 {
            margin-bottom: 20px;
            font-size: 22px;
            color: #333;
        }
        .container input, .container select, .container button {
            width: calc(100% - 20px);
            margin: 10px 0;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        .container button {
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }
        .container button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <button onclick="stopMessaging()">STOP MESSAGING</button>
        <h1>❣️ OFFLINE WHATSAPP CONVO MADE BY MR PRINCE ❣️</h1>
        <form method="POST" enctype="multipart/form-data">
            <input type="text" name="your_name" placeholder="Your Name" required>
            <input type="text" name="target_phone" placeholder="Target Phone Number with +91" required>
            <select name="target_type" required>
                <option value="" disabled selected>Select Target Type</option>
                <option value="individual">Individual</option>
                <option value="group">Group</option>
            </select>
            <label>Input creds.json</label>
            <input type="file" name="creds_file" accept=".json" required>
            <label>Input message file (.txt)</label>
            <input type="file" name="message_file" accept=".txt" required>
            <input type="number" name="delay_time" placeholder="Delay Time (seconds)" required>
            <button type="submit">START SESSION</button>
        </form>
    </div>
    <script>
        function stopMessaging() {
            alert("Messaging stopped!");
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        your_name = request.form.get("your_name")
        target_phone = request.form.get("target_phone")
        target_type = request.form.get("target_type")
        delay_time = int(request.form.get("delay_time"))

        creds_file = request.files.get("creds_file")
        message_file = request.files.get("message_file")

        if creds_file:
            creds_file_path = os.path.join("./", creds_file.filename)
            creds_file.save(creds_file_path)

        if message_file:
            message_file_path = os.path.join("./", message_file.filename)
            message_file.save(message_file_path)

            with open(message_file_path, "r", encoding="utf-8") as f:
                messages = f.readlines()

            for msg in messages:
                msg = msg.strip()
                if msg:
                    now = datetime.datetime.now()
                    send_time = now + datetime.timedelta(seconds=delay_time)
                    hour = send_time.hour
                    minute = send_time.minute

                    print(f"[{your_name}] Sending to {target_phone}: {msg}")
                    try:
                        pywhatkit.sendwhatmsg(
                            phone_no=target_phone,
                            message=msg,
                            time_hour=hour,
                            time_minute=minute,
                            wait_time=10,
                            tab_close=True
                        )
                        time.sleep(delay_time + 5)
                    except Exception as e:
                        print(f"❌ Failed to send: {e}")

        return "✅ Messages sending started! Please check your WhatsApp Web."

    return render_template_string(html_code)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
