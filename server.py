from flask import Flask, render_template_string, request, jsonify
import os
import anthropic

app = Flask(__name__)

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# Serve the HTML UI
def get_html_content():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route("/")
def index():
    return render_template_string(get_html_content())

# Main endpoint
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}

    fact = (data.get("fact") or "").strip()
    analysis = (data.get("analysis") or "").strip()
    mutation = (data.get("mutation") or "").strip()

    if not fact or not mutation:
        return jsonify({
            "error": "Missing input. Required fields: fact, mutation. Optional: analysis.",
            "received_keys": list(data.keys())
        }), 400

    result = generate_counterfactual_analysis(fact, analysis, mutation)
    return jsonify({"result": result})

# Core logic (Claude-powered)
def generate_counterfactual_analysis(fact, analysis, mutation):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "ERROR: ANTHROPIC_API_KEY is not set. Set it in PowerShell before running the server."
    
    system_prompt = (
        "You are a senior U.S. federal tax legal analyst.\n"
        "Rewrite the analysis under a counterfactual assumption.\n"
        "Do not summarize. Do not explain methodology.\n"
        "Produce only the rewritten analysis, in a professional legal tone.\n"
        "If the provided baseline analysis is empty or inadequate, infer a reasonable baseline analysis "
        "from the facts before rewriting under the counterfactual."
    )

    user_prompt = f"""ORIGINAL FACT
-------------
{fact}

ORIGINAL ANALYSIS
-----------------
{analysis if analysis else "[No baseline analysis provided. Infer a baseline analysis from the facts.]"} 

COUNTERFACTUAL ASSUMPTION
-------------------------
{mutation}

Task:
1) If needed, infer the baseline analysis from the facts.
2) Rewrite the analysis as if the counterfactual assumption were true.
Return only the rewritten analysis.
"""

    # Diagnostic output for API key sanity (truncated for safety)
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    print(f"Key present: {bool(key)}, length: {len(key)}")
    print(f"Key prefix: {key[:5]!r}")

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=3000,
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    # Robust extraction across SDK response shapes
    return "\n".join(
        block.text for block in getattr(message, "content", [])
        if getattr(block, "type", None) == "text" and getattr(block, "text", None)
    ).strip()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
