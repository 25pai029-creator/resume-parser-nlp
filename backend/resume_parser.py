from pdfminer.high_level import extract_text
from nlp_utils import preprocess, extract_entities, keyword_match

def parse_resume(file_path, job_desc):
    resume_text = extract_text(file_path)

    resume_tokens = preprocess(resume_text)
    job_tokens = preprocess(job_desc)

    skills, experience, roles = extract_entities(resume_text)
    score = keyword_match(resume_tokens, job_tokens)

    return {
        "skills": skills,
        "experience": experience,
        "roles": roles,
        "match_score": score
    }
