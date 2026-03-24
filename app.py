from flask import Flask, render_template, request, jsonify, url_for
import psycopg2
import random

app = Flask(__name__)

DB_URI = "postgresql://postgres:atharva%40123@db.oqwjmftcltvzuvwpbfpv.supabase.co:5432/postgres"

@app.route('/')
def login():
    return render_template('index.html') # This is your Login page

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    news_text = data.get('text')

    # 1. ML Logic Simulation (You can replace this with your actual model later)
    red_flags = ["slapped", "conspiracy", "secret", "exposed", "modi"]
    is_fake = any(word in news_text.lower() for word in red_flags) or random.random() < 0.5
    confidence = random.randint(78, 98)
    verdict = "Fake" if is_fake else "Real"

    # 2. Save to Supabase PostgreSQL
    try:
        conn = psycopg2.connect(DB_URI)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO news_history (content, verdict, confidence) VALUES (%s, %s, %s)",
            (news_text, verdict, confidence)
        )
        conn.commit()
        cur.close()
        conn.close()
        db_status = "Saved to Cloud DB"
    except Exception as e:
        db_status = f"DB Error: {e}"

    return jsonify({
        "is_fake": is_fake, 
        "confidence": confidence, 
        "db_status": db_status
    })

if __name__ == '__main__':
    app.run(debug=True)
