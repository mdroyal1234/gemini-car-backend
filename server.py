import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# 🔑 আপনার আসল Gemini API Key এখানে বসাবেন
GEMINI_API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY_HERE"
genai.configure(api_key=GEMINI_API_KEY)

# 🧠 এআই-কে গাড়ির ড্রাইভার হিসেবে লক করার কড়া সিস্টেম প্রম্পট
SYSTEM_INSTRUCTION = (
    "তুমি একটি রোবট কারের এআই ড্রাইভার। ইউজার বাংলায় যাই বলুক, তুমি তার অর্থ বুঝে গাড়ি নিয়ন্ত্রণ করবে। "
    "তোমার উত্তরে অবশ্যই প্রথম লাইনে শুধুমাত্র এই ৫টি ট্যাগ এর যেকোনো একটি থাকবে: [FORWARD], [BACKWARD], [LEFT], [RIGHT], [STOP]। "
    "এবং দ্বিতীয় লাইনে ইউজারকে বাংলায় একটি ছোট জবাব দেবে (কোনো ফালতু জ্ঞান ছাড়া)।"
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

@app.route('/command', methods=['POST'])
def process_command():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
            
        response = model.generate_content(user_message)
        ai_text = response.text.strip()
        return jsonify({"response": ai_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
