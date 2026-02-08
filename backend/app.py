from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import PyPDF2
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.metrics.distance import edit_distance
from nltk.corpus import wordnet

# Make sure nltk resources are available
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

# ---------------- SPELLING CORRECTION ----------------
def correct_spelling(word, vocab):
    if word in vocab:
        return word
    return min(vocab, key=lambda v: edit_distance(word, v))

# ---------------- TEXT CLEANING ----------------
BASE_VOCAB = {
    "devlop", "developer", "development",
    "python", "java", "javascript",
    "backend", "frontend", "fullstack",
    "engineer", "engineering",
    "system", "software", "web"
}
#BASE_VOCAB = set(job_description.lower().split()) | set(resume_text.lower().split())




def clean_text_for_skills(text):
    text = re.sub(r"[^a-zA-Z ]", " ", text)
    words = text.lower().split()

    cleaned_words = []
    for w in words:
        if w not in stop_words:
            stem = stemmer.stem(w)
            lemma = lemmatizer.lemmatize(w, wordnet.VERB)
            corrected = correct_spelling(lemma, BASE_VOCAB)
            cleaned_words.append(corrected)
            cleaned_words.append(stem)

    return set(cleaned_words)

    """


def clean_text_for_skills(text):
    text = re.sub(r"[^a-zA-Z ]", " ", text)
    words = text.lower().split()

    cleaned_words = set()

    for w in words:
        if w in stop_words:
            continue

        # 1️⃣ Lemmatize as NOUN (systems → system)
        lemma_noun = lemmatizer.lemmatize(w, wordnet.NOUN)

        # 2️⃣ Lemmatize as VERB (developing → develop)
        lemma_verb = lemmatizer.lemmatize(lemma_noun, wordnet.VERB)

        # 3️⃣ Spelling correction
        corrected = correct_spelling(lemma_verb, BASE_VOCAB)

        # 4️⃣ Stemming (sir ne bola hoy etle)
        stem = stemmer.stem(corrected)

        # Store all useful forms
        cleaned_words.add(corrected)
        cleaned_words.add(stem)

    return cleaned_words
"""




# ---------------- EXPERIENCE EXTRACTION ----------------
def extract_experience(text):
    experience_patterns = re.findall(
        r'(\d+(\.\d+)?\+?)\s*(years|year|yrs|yr)',
        text.lower()
    )

    experiences = []
    for exp in experience_patterns:
        experiences.append(exp[0] + " years")

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
        "web developer": ["web", "developer"],
        "ai developer": ["ai", "developer"]
    }

    text = re.sub(r"[^a-zA-Z ]", " ", text.lower())
    words = set(text.split())

    found_roles = []
    for role, keywords in roles.items():
        if all(k in words for k in keywords):
            found_roles.append(role)

    return found_roles

# ---------------- ROUTES ----------------
@app.get("/")
def home():
    return {"message": "Resume Parser API is running"}

@app.post("/parse")
async def parse_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    resume_text = ""

    # Read TXT
    if resume.filename.endswith(".txt"):
        resume_text = (await resume.read()).decode("utf-8")

    # Read PDF
    elif resume.filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(resume.file)
        for page in reader.pages:
            resume_text += page.extract_text() or ""

    resume_words = clean_text_for_skills(resume_text)
    job_words = clean_text_for_skills(job_description)

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

    return JSONResponse({
        "match_score": score,
        "hiring_decision": hiring_status,
        "matched_skills": matched_skills[:10],
        "missing_skills": missing_skills[:10],
        "extracted_roles": extracted_roles,
        "experience": extracted_experience
    })