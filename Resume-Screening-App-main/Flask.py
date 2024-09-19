from flask import Flask, request, jsonify
import spacy
import docx2txt
import PyPDF2

app = Flask(__name__)
nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfFileReader(pdf_file)
    text = ''
    for page_num in range(reader.numPages):
        page = reader.getPage(page_num)
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_file):
    return docx2txt.process(docx_file)

@app.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files['resume']
    
    # Check file type and extract text accordingly
    if file.filename.endswith('.pdf'):
        resume_text = extract_text_from_pdf(file)
    elif file.filename.endswith('.docx'):
        resume_text = extract_text_from_docx(file)
    else:
        return jsonify({'result': 'Invalid file type. Please upload PDF or DOCX.'})

    # Process text using NLP
    doc = nlp(resume_text)
    
    # Example: Extract basic entities like skills or experience
    skills = []
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PERSON', 'DATE', 'GPE']:
            skills.append(ent.text)

    result = f"Skills/Experience extracted: {', '.join(skills)}"
    
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
