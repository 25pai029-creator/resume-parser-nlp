import nltk
import spacy
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from Levenshtein import distance

nltk.download('punkt')
nltk.download('stopwords')

nlp = spacy.load("en_core_web_sm")
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def preprocess(text):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    stemmed = [stemmer.stem(t) for t in tokens]
    return stemmed

def extract_entities(text):
    doc = nlp(text)
    skills = []
    experience = []
    roles = []

    for ent in doc.ents:
        if ent.label_ == "ORG":
            roles.append(ent.text)
        if ent.label_ == "DATE":
            experience.append(ent.text)

    return list(set(skills)), list(set(experience)), list(set(roles))

def keyword_match(resume_tokens, job_tokens):
    matches = set(resume_tokens).intersection(set(job_tokens))
    return len(matches)
