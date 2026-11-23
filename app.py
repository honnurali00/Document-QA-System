
from flask import Flask, render_template, request, jsonify
from main import read_document, process_question, evaluate_system

from contextlib import redirect_stdout
from io import StringIO

app = Flask(__name__)

# Load the document and create the Knowledge Base
knowledge_base = read_document("document.txt")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask_question():

    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "answer": "Please enter a question.",
            "reasoning": ""
        })

    # Capture the reasoning trace from the existing Python system
    output = StringIO()

    with redirect_stdout(output):
        answer = process_question(question, knowledge_base)

    reasoning = output.getvalue()

    return jsonify({
        "answer": answer,
        "reasoning": reasoning
    })


@app.route("/knowledge")
def get_knowledge():

    return jsonify(knowledge_base)


@app.route("/evaluate")
def evaluate():

    output = StringIO()

    with redirect_stdout(output):
        evaluate_system(knowledge_base)

    return jsonify({
        "results": output.getvalue()
    })


if __name__ == "__main__":
    app.run(debug=False)
