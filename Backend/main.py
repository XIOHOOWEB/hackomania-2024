import kd
import ed
import sa
import ner
from flask import Flask, request, jsonify, render_template
from sa import analyze_text_corpus

from kw import poskeywords, negkeywords
from tc import posstatements, negstatements


app = Flask(__name__, template_folder='.')

poskeywords = [
    "happy", "classy", "affectionate", "admirable",
    "clever", "enthusiastic", "nice", "friendly",
    "lovely", "lively", "intelligent", "joyful",
    "optimistic", "satisfied", "sunny", "vibrant",
    "wonderful", "zealous", "zesty", "zippy",
    "zestful", "zest", "encourage", "Active",
    "motivate", "Activate", "energize", "amuse",
    "ecstatic", "polite", "generous", "best", "good",
    "breathtaking", "positive", "disciplined", "reliable",
    "Glad", "ideal", "Peaceful"
]

negkeywords = [
    "abysmal", "adverse", "alarming", "atrocious",
    "awful", "appalling", "bad", "creep", "lost"
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/detect_keywords', methods=['POST'])
def detect_keywords():
    data = request.get_json()
    text = data.get('text')
    keywords = data.get('keywords')

@app.route('/analyze_ner', methods=['POST'])
def analyze_ner_route():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({"error: Missing 'text' field in request body"}), 400

    text = data['text']
    result = ner.analyze_ner(text)
    return jsonify(text)

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    if 'text' not in data:
        return jsonify ({"error: Missing 'text' field in request body "}), 400
    text = data['text']
    return jsonify(sa.analyze_sentiment(text))

@app.route('/analyze_corpus_sentiments', methods=['POST'])
def analyze_corpus_sentiments():

    data = request.get_json()
    text_corpus = data.get('text_corpus', '')

    positive_sentiment_count = 0
    negative_sentiment_count = 0

    for word in text_corpus.split():
        if word.lower() in poskeywords:
            positive_sentiment_count += 1
        elif word.lower() in negkeywords:
            negative_sentiment_count += 1


    if positive_sentiment_count > negative_sentiment_count:
        overall_sentiment = "Positive"
    elif negative_sentiment_count > positive_sentiment_count:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"

    sentiment_analysis_results = {
        "positive_sentiment_count": positive_sentiment_count,
        "negative_sentiment_count": negative_sentiment_count,
        "overall_sentiment": overall_sentiment
    }

    return jsonify(sentiment_analysis_results), 200

@app.route('/analyze_corpus', methods=['POST'])
def analyze_corpus_route():
    combined_statements = {**sa.negstatements, **sa.posstatements}
    sentiment_scores = sa.analyze_corpus(combined_statements)
    return jsonify(sentiment_scores)

@app.route('/analyze_emotion', methods=['POST'])
def analyze_emotion():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({"error: Missing 'text' field in request body "}), 400
    text = data['text']
    return jsonify(ed.analyze_sentiment(text))

@app.route('/update_keywords', methods=['POST'])
def update_keywords():
    data = request.get_json()
    if not all(key in data for key in ['new_negkeywords', 'new_poskeywords', 'new_negstatements', 'new_posstatements']):
        return jsonify({"error. Missing one or more required fields"}), 400
    
    sa.negkeywords.extend(data['new_negkeywords'])
    sa.poskeywords.extend(data['new_poskeywords'])
    sa.negstatements.extend(data['new_negstatements'])
    sa.posstatements.extend(data['new_posstatements'])

    return jsonify(["message: keywords and statements updated successfully"])

if __name__ == '__main__':
    app.run(debug=True)
