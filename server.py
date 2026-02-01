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
        
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

def generate_counterfactual(text):
    """
    Generate a counterfactual response based on input text.
    Replace this with your actual counterfactual generation logic.
    """
    # Simple template-based response for demonstration
    if "if" in text.lower():
        return f"Considering your scenario: '{text}', here are some alternative possibilities:\n\n" \
               f"• What if the opposite were true?\n" \
               f"• How might things be different under other conditions?\n" \
               f"• Consider the chain of events that would need to change.\n\n" \
               f"This is a placeholder response. Implement your counterfactual logic here."
    else:
        return f"Based on '{text}', let me explore some counterfactual scenarios:\n\n" \
               f"• If {text} had not happened, then...\n" \
               f"• Imagine if the circumstances were different...\n" \
               f"• In an alternative timeline where this wasn't the case...\n\n" \
               f"This is a placeholder response. Implement your counterfactual logic here."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)