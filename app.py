from flask import Flask, render_template, request, jsonify, url_for
import psycopg2
import random

app = Flask(__name__)

# The port MUST be 6543 for the Shared Pooler
DB_URI = "postgresql://postgres.oqwjmftcltvzuvwpbfpv:Atharva%40123@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres?sslmode=require"

def test_insert():
    try:
        conn = psycopg2.connect(DB_URI)
        cur = conn.cursor()
        cur.execute("INSERT INTO public.news_history (content, verdict, confidence) VALUES ('hello', 'Fake', 90)")
        conn.commit()
        print("✅ INSERT WORKED")
    except Exception as e:
        print("❌ ERROR:", e)

test_insert()

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
    data = request.get_json(force=True)
    news_text = data.get('text', '')

    print("🔥 /analyze route hit")
    print("Incoming data:", data)

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
    "INSERT INTO public.news_history (content, verdict, confidence) VALUES (%s, %s, %s)",
    (news_text, verdict, confidence)
)
        conn.commit()
        cur.close()
        conn.close()
        db_status = "Saved to Cloud DB"
    except Exception as e:
        print("❌ DB ERROR:", e)
        db_status = f"DB Error: {e}"

    return jsonify({
        "is_fake": is_fake, 
        "confidence": confidence, 
        "db_status": db_status
    })

# def test_connection():
#     try:
#         conn = psycopg2.connect(DB_URI)
#         print("✅ DATABASE CONNECTED SUCCESSFULLY!")
#         conn.close()
#     except Exception as e:
#         print(f"❌ DATABASE CONNECTION FAILED: {e}")

# test_connection()

if __name__ == '__main__':
    app.run(debug=True)
