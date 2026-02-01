# IfThenElsewhere - Counterfactual Scenario Generator

A web application that generates alternative scenarios and counterfactual thinking exercises. Explore "what if" situations and alternative realities through an intuitive web interface.

## Features

- 🌐 **Web Interface**: Clean, responsive design for easy interaction
- 🤖 **Counterfactual Generation**: AI-powered alternative scenario creation
- 🎯 **Multiple Scenarios**: Generate several alternative possibilities at once
- 📊 **Confidence Scoring**: Each scenario comes with a confidence rating
- 🏷️ **Keyword Extraction**: Automatic identification of key terms
- ⚡ **Real-time Processing**: Fast response times with loading indicators
- 📱 **Mobile Friendly**: Works seamlessly on all device sizes

## Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Kafkaroo/IfThenElsewhere.git
   cd IfThenElsewhere
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python server.py
   ```

4. **Open your browser and visit:**
   ```
   http://localhost:5000
   ```

## Usage

1. **Enter a Scenario**: Type any situation, statement, or "what if" question in the textarea
2. **Generate**: Click "Generate Counterfactual" or press Ctrl+Enter (Cmd+Enter on Mac)
3. **Explore Results**: Review the generated alternative scenarios with confidence ratings

### Example Inputs

- "The internet was never invented"
- "Social media became popular in the 1990s"
- "Electric cars were developed before gasoline cars"
- "Humans never learned to write"
- "Coffee was never discovered"

## API Endpoints

The server provides several REST API endpoints:

### `POST /api/generate`
Generate counterfactual scenarios from input text.

**Request Body:**
```json
{
  "input": "Your scenario or statement here"
}
```

**Response:**
```json
{
  "success": true,
  "scenarios": [
    {
      "id": 1,
      "scenario": "Generated counterfactual text...",
      "confidence": 0.85,
      "keywords": ["keyword1", "keyword2", "keyword3"]
    }
  ],
  "original_input": "Your original input",
  "processing_time": 0.5,
  "metadata": {
    "model_version": "1.0.0",
    "timestamp": 1640995200
  }
}
```

### `GET /api/health`
Health check endpoint.

### `GET /api/status`
Get server status and configuration information.

## Configuration

You can configure the server using environment variables:

- `PORT`: Server port (default: 5000)
- `DEBUG`: Enable debug mode (default: False)

Example:
```bash
PORT=8080 DEBUG=true python server.py
```

## Development

### Project Structure

```
IfThenElsewhere/
├── server.py          # Flask server with API endpoints
├── index.html         # Web interface
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

### Extending the Generator

The `CounterfactualGenerator` class in `server.py` contains the core logic for generating scenarios. To improve the generation quality:

1. **Replace the simple template system** with a more sophisticated NLP model
2. **Integrate with AI services** like OpenAI GPT, Google's PaLM, or Hugging Face models
3. **Add more sophisticated keyword extraction** using libraries like spaCy or NLTK
4. **Implement caching** for frequently requested scenarios
5. **Add user feedback mechanisms** to improve generation quality

### Example Integration with OpenAI

```python
import openai

class CounterfactualGenerator:
    def __init__(self):
        openai.api_key = "your-api-key-here"
    
    def generate(self, input_text):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Generate counterfactual scenarios..."},
                {"role": "user", "content": input_text}
            ]
        )
        # Process response...
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Roadmap

- [ ] Integration with advanced AI models (GPT-4, Claude, etc.)
- [ ] User authentication and scenario history
- [ ] Scenario sharing and collaboration features
- [ ] Advanced filtering and search capabilities
- [ ] Export functionality (PDF, JSON, etc.)
- [ ] Batch processing for multiple inputs
- [ ] Custom templates and scenario types
- [ ] Analytics and usage statistics

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/Kafkaroo/IfThenElsewhere/issues) page
2. Create a new issue with detailed information
3. Include steps to reproduce any bugs

## Acknowledgments

- Built with Flask and vanilla JavaScript for simplicity and performance
- Inspired by counterfactual thinking research in cognitive science
- UI design influenced by modern web application patterns

---

**IfThenElsewhere** - Explore infinite possibilities through counterfactual scenarios.