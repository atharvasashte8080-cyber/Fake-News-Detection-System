from flask import Flask, render_template, request, jsonify
import psycopg2
import random

app = Flask(__name__)

DB_URI = "your_supabase_connection_uri_here"

@app.route('/')
def index():
    return render_template('index.html') # This is your Login page now

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    news_text = data.get('text')

    # 1. Simple ML Logic (Placeholder)
    is_fake = "slapped" in news_text.lower() or random.random() < 0.5
    confidence = random.randint(75, 98)

    # 2. Save to PostgreSQL (Supabase)
    conn = psycopg2.connect(DB_URI)
    cur = conn.cursor()
    cur.execute("INSERT INTO news_history (content, verdict, confidence) VALUES (%s, %s, %s)", 
                (news_text, "Fake" if is_fake else "Real", confidence))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"is_fake": is_fake, "confidence": confidence})

if __name__ == '__main__':
    app.run(debug=True)
