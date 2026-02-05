from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import re
import os
import nltk

# ================= NLTK FIX FOR RENDER =================
NLTK_DATA_DIR = os.path.join(os.getcwd(), "nltk_data")
os.makedirs(NLTK_DATA_DIR, exist_ok=True)
nltk.data.path.append(NLTK_DATA_DIR)

nltk.download("stopwords", download_dir=NLTK_DATA_DIR, quiet=True)
nltk.download("wordnet", download_dir=NLTK_DATA_DIR, quiet=True)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.metrics.distance import edit_distance

# ================= APP INIT =================
app = Flask(__name__)
CORS(app)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

# ================= SPELLING CORRECTION =================
def correct_spelling(word, vocab):
    if word in vocab:
        return word
    distances = [(edit_distance(word, w), w) for w in vocab]
    return min(distances, key=lambda x: x[0])[1] if distances else word

# ================= TEXT CLEANING =================
def clean_text_for_skills(text):
    text = re.sub(r"[^a-zA-Z ]", " ", text)
    words = text.lower().split()
    words = [w for w in words if w not in stop_words]
    return set(words)

# ================= EXPERIENCE EXTRACTION =================
def extract_experience(text):
    pattern = re.findall(r'(\d+(\.\d+)?\+?)\s*(years|year|yrs|yr)', text.lower())
    return list(set([p[0] + " years" for p in pattern]))

# ================= ROLE EXTRACTION =================
def extract_roles(text):
    roles = {
        "data scientist": ["data", "scientist"],
        "machine learning engineer": ["machine", "learning"],
        "full stack developer": ["full", "stack"],
        "python developer": ["python", "developer"],
        "ai engineer": ["ai", "engineer"],
        "web developer": ["web", "developer"]
    }

    text = re.sub(r"[^a-zA-Z ]", " ", text.lower())
    words = set(text.split())

    found = []
    for role, keys in roles.items():
        if all(k in words for k in keys):
            found.append(role)
    return found

# ================= API =================
@app.route("/parse", methods=["POST"])
def parse_resume():
    file = request.files.get("resume")
    job_desc = request.form.get("job_description", "")

    if not file:
        return jsonify({"error": "Resume file required"}), 400

    resume_text = ""

    if file.filename.endswith(".txt"):
        resume_text = file.read().decode("utf-8", errors="ignore")

    elif file.filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            resume_text += page.extract_text() or ""

    resume_words = clean_text_for_skills(resume_text)
    job_words = clean_text_for_skills(job_desc)

    matched_skills = list(resume_words & job_words)
    missing_skills = list(job_words - resume_words)

    score = 0
    if len(job_words) > 0:
        score = round((len(matched_skills) / len(job_words)) * 100)

    if score >= 60:
        status = "Strongly Recommended"
    elif score >= 40:
        status = "Recommended"
    else:
        status = "Not Recommended"

    return jsonify({
        "score": score,
        "status": status,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "roles": extract_roles(resume_text),
        "experience": extract_experience(resume_text)
    })

# ================= HEALTH CHECK =================
@app.route("/")
def home():
    return jsonify({"message": "Resume Parser API is running"})
