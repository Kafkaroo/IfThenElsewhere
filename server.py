from flask import Flask, render_template_string, request, jsonify
import os
import anthropic

app = Flask(__name__)

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# Serve the HTML UI
def get_html_content():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/')
def index():
    return render_template_string(get_html_content())

# Main endpoint
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

# Core logic (now Claude-powered)
def generate_counterfactual_analysis(fact, analysis, mutation):
    message = client.messages.create(...)
    print(message)
    print(message.model_dump())
   
    system_prompt = """
You are a senior legal analyst.
Your task is to rewrite the legal analysis under a counterfactual assumption.
Do not summarize. Do not explain methodology.
Produce only the rewritten analysis.
Maintain professional legal tone and structure.
"""

    user_prompt = f"""
ORIGINAL FACT
-------------
{fact}

ORIGINAL ANALYSIS
-----------------
{analysis}

COUNTERFACTUAL ASSUMPTION
-------------------------
{mutation}

Rewrite the analysis as if the counterfactual assumption were true.
"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=3000,
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return "\n".join(
    block.text for block in message.content
    if getattr(block, "type", None) == "text"
)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
