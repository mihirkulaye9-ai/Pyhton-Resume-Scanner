#def scan_resume(resume):
 ##  data = resumeparse.read_file(resume)
   # for i, j in data.items():
    #    print(f"{i}:>>{j}")
#
#resume_path = r"C:\Users\Shivani\Downloads\Resume.pdf.pdf"
#scan_resume(resume_path)
# Make sure spaCy model is installed once:
# python -m spacy download en_core_web_sm
import re
import os
import fitz  # PyMuPDF
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"⚠️ File not found: {pdf_path}")
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

# Function to parse resume
def parse_resume(resume_path):
    text = extract_text_from_pdf(resume_path)
    doc = nlp(text)

    # Extract name (first PERSON entity)
    name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    # Extract email
    email = re.search(r"[\w\.-]+@[\w\.-]+", text)
    email = email.group(0) if email else None

    # Extract phone number
    phone = re.search(r"\+?\d[\d\s-]{8,}\d", text)
    phone = phone.group(0) if phone else None

    # Extract education
    education = []
    for keyword in ["B.Tech", "B.E", "Bachelor of Engineering", "M.Tech", "M.E", "B.Sc", "M.Sc", "PhD"]:
        if keyword.lower() in text.lower():
            education.append(keyword)

    # Extract skills
    skill_keywords = ["Python", "Java", "C++", "SQL", "Machine Learning",
                      "Data Science", "NLP", "Deep Learning", "Excel", "Power BI"]
    skills = [skill for skill in skill_keywords if skill.lower() in text.lower()]

    return {
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Education": education,
        "Skills": skills
    }

# ------------------- RUN -------------------
resume_path = r"C:\Users\Shivani\Downloads\Resume_Mihir_Kulaye_2024 (1).pdf"  # <-- update exact filename
try:
    data = parse_resume(resume_path)
    for k, v in data.items():
        print(f"{k}: >> {v}")
except FileNotFoundError as e:
    print(e)
    print("👉 Please check the file name and make sure it’s in the Downloads folder.")
