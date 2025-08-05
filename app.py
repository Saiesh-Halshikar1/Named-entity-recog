# app.py
from flask import Flask, request, jsonify
import spacy


try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("Downloading spaCy model 'en_core_web_sm'...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load('en_core_web_sm')

app = Flask(__name__)

@app.route('/ner', methods=['POST'])
def perform_ner():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "Text field is missing or empty"}), 400
        
    try:
        doc = nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start_char": ent.start_char,
                "end_char": ent.end_char
            })
        return jsonify({"entities": entities})

    except Exception as e:
        return jsonify({"error": f"An error occurred during NER processing: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
