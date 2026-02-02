from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

def get_html_content():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/')
def index():
    return render_template_string(get_html_content())

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()

    fact = data.get('fact', '').strip()
    analysis = data.get('analysis', '').strip()
    mutation = data.get('mutation', '').strip()

    if not fact or not analysis or not mutation:
        return jsonify({'error': 'Missing input'}), 400

    result = generate_counterfactual_analysis(fact, analysis, mutation)
    return jsonify({'result': result})

def generate_counterfactual_analysis(fact, analysis, mutation):
    """
    This is the only function you will ever replace with AI.
    """

    return f"""
ORIGINAL FACT:
{fact}

ORIGINAL ANALYSIS:
{analysis}

COUNTERFACTUAL ASSUMPTION:
{mutation}

REWRITTEN ANALYSIS:
[This is where Open Arena rewrites the analysis under the new assumption.]
"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
