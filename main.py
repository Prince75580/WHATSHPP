from flask import Flask, render_template_string, request
import pywhatkit
import time
import datetime

app = Flask(__name__)

# Embedded HTML Code
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>❤️𝑻𝑯𝑬 𝑳𝑬𝑮𝑬𝑵𝑫 𝑷𝑹𝑰𝑵𝑪𝑬 𝑰𝑵𝑺𝑰𝑫𝑬❤️</title>
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
        <button onclick="stopMessaging()" style="background-color: #007bff; color: white; border: none; cursor: pointer; padding: 10px; border-radius: 5px;">STOP MESSAGING</button>
        <h1>❣️OFFLINE WHATSAPP CONVO MADE BY MR PRINCE❣️</h1>
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
        creds_file = request.files.get("creds_file")
        message_file = request.files.get("message_file")
        delay_time = int(request.form.get("delay_time"))

        # Save uploaded files
        if creds_file:
            creds_file.save(f"./{creds_file.filename}")

        if message_file:
            msg_path = f"./{message_file.filename}"
            message_file.save(msg_path)

            # Read messages
            with open(msg_path, "r", encoding="utf-8") as f:
                messages = f.readlines()

            for msg in messages:
                msg = msg.strip()
                if msg:
                    now = datetime.datetime.now()
                    send_time = now + datetime.timedelta(seconds=delay_time)
                    hour = send_time.hour
                    minute = send_time.minute

                    print(f"Sending to {target_phone}: {msg}")
                    try:
                        pywhatkit.sendwhatmsg(target_phone, msg, hour, minute, wait_time=10, tab_close=True)
                        time.sleep(delay_time + 5)  # buffer between messages
                    except Exception as e:
                        print(f"Failed to send: {e}")

        return "✅ Messages sending started. Check WhatsApp Web."

    return render_template_string(html_code)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
