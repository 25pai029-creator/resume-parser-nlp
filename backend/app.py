from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import re
import os
import nltk

# ---------------- NLTK RENDER FIX ----------------
# Create local nltk_data directory (Render-safe)
NLTK_DATA_DIR = os.path.join(os.getcwd(), "nltk_data")
os.makedirs(NLTK_DATA_DIR, exist_ok=True)

nltk.data.path.append(NLTK_DATA_DIR)

# Download required NLTK resources
nltk.download("stopwords", download_dir=NLTK_DATA_DIR, quiet=True)
nltk.download("wordnet", download_dir=NLTK_DATA_DIR, quiet=True)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.metrics.distance import edit_distance

# ---------------- APP INIT ----------------
app = Flask(__name__)
CORS(app)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

# ---------------- SPELLING CORRECTION ----------------
def correct_spelling(word, vocab):
    if word in vocab:
        return word
    return min(vocab, key=lambda v: edit_distance(word, v))

# ---------------- TEXT CLEANING ----------------
def clean_text(text, vocab=None):
    text = re.sub(r"[^a-zA-Z ]", " ", text)
    words = text.lower().split()
    words = [w for w in words if w not in stop_words]

    if vocab:
        words = [correct_spelling(w, vocab) for w in words]

    words = [lemmatizer.lemmatize(w) for w in words]
    words = [stemmer.stem(w) for w in words]

    return set(words)

def clean_text_for_skills(text):
    text = re.sub(r"[^a-zA-Z ]", " ", text)
    words = text.lower().split()
    words = [w for w in words if w not in stop_words]
    return set(words)

# ---------------- EXPERIENCE EXTRACTION ----------------
def extract_experience(text):
    experience_patterns = re.findall(
        r'(\d+(\.\d+)?\+?)\s*(years|year|yrs|yr)',
        text.lower()
    )
    experiences = [exp[0] + " years" for exp in experience_patterns]
    return list(set(experiences))

# ---------------- ROLE EXTRACTION ----------------
def extract_roles(text):
    roles = {
        "data scientist": ["data", "scientist"],
        "software engineer": ["software", "engineer"],
        "machine learning engineer": ["machine", "learning", "engineer"],
        "ml engineer": ["ml", "engineer"],
        "backend developer": ["backend", "developer"],
        "frontend developer": ["frontend", "developer"],
        "full stack developer": ["full", "stack", "developer"],
        "python developer": ["python", "developer"],
        "ai engineer": ["ai", "engineer"],
        "web developer": ["web", "developer"]
    }

    text = re.sub(r"[^a-zA-Z ]", " ", text.lower())
    words = set(text.split())

    found_roles = []
    for role, keywords in roles.items():
        if all(k in words for k in keywords):
            found_roles.append(role)

    return found_roles

# ---------------- API ROUTE ----------------
@app.route("/parse", methods=["POST"])
def parse_resume():
    file = request.files.get("resume")
    job_desc = request.form.get("job_description", "")

    resume_text = ""

    if file and file.filename.endswith(".txt"):
        resume_text = file.read().decode("utf-8", errors="ignore")

    elif file and file.filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            resume_text += page.extract_text() or ""

    resume_words = clean_text_for_skills(resume_text)
    job_words = clean_text_for_skills(job_desc)

    matched_skills = list(resume_words & job_words)
    missing_skills = list(job_words - resume_words)

    extracted_roles = extract_roles(resume_text)
    extracted_experience = extract_experience(resume_text)

    if len(job_words) == 0:
        score = 0
    else:
        score = round((len(matched_skills) / len(job_words)) * 100)

    if score >= 60:
        hiring_status = "Strongly Recommended"
    elif score >= 40:
        hiring_status = "Recommended"
    else:
        hiring_status = "Not Recommended"

    return jsonify({
        "match_score": score,
        "hiring_decision": hiring_status,
        "matched_skills": matched_skills[:10],
        "missing_skills": missing_skills[:10],
        "extracted_roles": extracted_roles,
        "experience": extracted_experience
    })

# ---------------- HEALTH CHECK ----------------
@app.route("/")
def home():
    return jsonify({"message": "Resume Parser API is running"})

# ---------------- LOCAL RUN (Windows) ----------------
if __name__ == "__main__":
    app.run(debug=True)
