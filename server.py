print("SERVER FILE EXECUTED")
from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# Read the HTML file content
def get_html_content():
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # Fallback HTML if index.html doesn't exist
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>IfThenElsewhere</title>
        </head>
        <body>
            <h1>IfThenElsewhere</h1>
            <textarea id="input" placeholder="Enter your scenario..."></textarea>
            <button onclick="generateCounterfactual()">Generate Counterfactual</button>
            <div id="output"></div>
        </body>
        </html>
        """

@app.route('/')
def index():
    """Serve the main HTML page"""
    html_content = get_html_content()
    return render_template_string(html_content)

@app.route('/ask', methods=['POST'])
def ask():
    """Handle counterfactual generation requests"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        input_text = data['text'].strip()
        
        if not input_text:
            return jsonify({'error': 'Empty text provided'}), 400
        
        # Simple counterfactual generation (replace with your logic)
        response = generate_counterfactual(input_text)
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

def generate_counterfactual(text):
    return {
        "original": text,
        "mutations": [
            {
                "dimension": "taxpayer status",
                "counterfactual": "Assume taxpayer is foreign",
                "impact": "Source and withholding rules apply"
            },
            {
                "dimension": "entity classification",
                "counterfactual": "What if the entity were a partnership instead of a corporation?",
                "impact": "Subchapter K applies; pass-through taxation, allocation of income, and partner-level consequences become central."
            },
            {
                "dimension": "timing",
                "counterfactual": "Assume election is late",
                "impact": "Election likely invalid absent 9100 relief"
            }
        ]
    }


 
