from transformers import pipeline

nlp = pipeline("question-generation")

def generate_questions(text):
    return nlp(text)
