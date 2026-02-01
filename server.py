#!/usr/bin/env python3
"""
Flask server for IfThenElsewhere - Counterfactual Scenario Generator
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import logging
import time
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
PORT = int(os.environ.get('PORT', 5000))
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

class CounterfactualGenerator:
    """
    Simple counterfactual scenario generator.
    Replace this with your actual AI/ML model or logic.
    """
    
    def __init__(self):
        self.templates = [
            "If {original} had not happened, then {alternative} might have occurred instead.",
            "Imagine if {original} were different - perhaps {alternative} would be the case.",
            "In an alternate reality where {original} is false, we might see {alternative}.",
            "What if {original} never existed? Then {alternative} could be possible.",
            "Consider the scenario where {original} is reversed - {alternative} becomes likely."
        ]
        
        self.alternatives = [
            "technology would have developed differently",
            "society would be organized in another way",
            "different cultural norms would emerge",
            "alternative solutions would be discovered",
            "unexpected opportunities would arise",
            "different relationships would form",
            "new perspectives would be valued",
            "alternative paths would be taken"
        ]
    
    def generate(self, input_text):
        """
        Generate counterfactual scenarios based on input text.
        
        Args:
            input_text (str): The original scenario or statement
            
        Returns:
            dict: Generated counterfactual scenarios and metadata
        """
        try:
            # Simulate processing time
            time.sleep(0.5)
            
            # Simple keyword extraction (replace with NLP)
            keywords = self._extract_keywords(input_text)
            
            # Generate multiple counterfactuals
            scenarios = []
            for i in range(3):  # Generate 3 scenarios
                template = random.choice(self.templates)
                alternative = random.choice(self.alternatives)
                
                scenario = template.format(
                    original=input_text.strip(),
                    alternative=alternative
                )
                scenarios.append({
                    'id': i + 1,
                    'scenario': scenario,
                    'confidence': round(random.uniform(0.7, 0.95), 2),
                    'keywords': keywords[:3]  # Top 3 keywords
                })
            
            return {
                'success': True,
                'scenarios': scenarios,
                'original_input': input_text,
                'processing_time': 0.5,
                'metadata': {
                    'model_version': '1.0.0',
                    'timestamp': time.time()
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating counterfactuals: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'scenarios': []
            }
    
    def _extract_keywords(self, text):
        """Simple keyword extraction (replace with proper NLP)"""
        # Remove common words and extract meaningful terms
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
        
        words = text.lower().replace('.', '').replace(',', '').split()
        keywords = [word for word in words if len(word) > 3 and word not in common_words]
        
        return keywords[:5]  # Return top 5 keywords

# Initialize the generator
generator = CounterfactualGenerator()

@app.route('/')
def index():
    """Serve the main HTML interface"""
    try:
        # Read the index.html file
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        # Fallback HTML if index.html doesn't exist
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>IfThenElsewhere - Server Running</title>
        </head>
        <body>
            <h1>IfThenElsewhere Server is Running!</h1>
            <p>The server is active, but index.html was not found.</p>
            <p>Please ensure index.html is in the same directory as server.py</p>
        </body>
        </html>
        """

@app.route('/api/generate', methods=['POST'])
def generate_counterfactual():
    """
    API endpoint to generate counterfactual scenarios
    
    Expected JSON payload:
    {
        "input": "Your scenario or statement here"
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'input' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: input'
            }), 400
        
        input_text = data['input'].strip()
        
        if not input_text:
            return jsonify({
                'success': False,
                'error': 'Input text cannot be empty'
            }), 400
        
        if len(input_text) > 1000:
            return jsonify({
                'success': False,
                'error': 'Input text too long (max 1000 characters)'
            }), 400
        
        # Generate counterfactual scenarios
        logger.info(f"Generating counterfactuals for input: {input_text[:50]}...")
        result = generator.generate(input_text)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in generate_counterfactual endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'IfThenElsewhere',
        'version': '1.0.0',
        'timestamp': time.time()
    })

@app.route('/api/status', methods=['GET'])
def status():
    """Get server status and statistics"""
    return jsonify({
        'service': 'IfThenElsewhere Counterfactual Generator',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            '/': 'Main interface',
            '/api/generate': 'Generate counterfactuals (POST)',
            '/api/health': 'Health check (GET)',
            '/api/status': 'Server status (GET)'
        },
        'generator_info': {
            'model_version': '1.0.0',
            'supported_languages': ['English'],
            'max_input_length': 1000
        }
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    logger.info("Starting IfThenElsewhere server...")
    logger.info(f"Server will run on port {PORT}")
    logger.info(f"Debug mode: {DEBUG}")
    
    # Print available endpoints
    print("\n" + "="*50)
    print("IfThenElsewhere - Counterfactual Generator Server")
    print("="*50)
    print(f"🌐 Main Interface: http://localhost:{PORT}/")
    print(f"🔧 API Generate: http://localhost:{PORT}/api/generate (POST)")
    print(f"💚 Health Check: http://localhost:{PORT}/api/health")
    print(f"📊 Status: http://localhost:{PORT}/api/status")
    print("="*50 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=DEBUG
    )