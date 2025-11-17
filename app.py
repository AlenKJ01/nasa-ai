from flask import Flask, render_template, request, jsonify
from utils.chat import answer_question
from utils.ingest import ingest
from utils.embed import save_embeddings_for_docs, load_index
import os
import google.genai

print("GENAI LOADED FROM:", google.genai.__file__)

app = Flask(__name__, static_folder="static")

def ensure_index():
    index, meta = load_index()
    if index is not None:
        print("[startup] FAISS index already exists. Skipping rebuild.")
        return

    print("[startup] No index found. Building now...")
    docs = ingest()
    save_embeddings_for_docs(docs)
    print("[startup] Index build complete. Ready for chat.")


# Run auto-index on server startup
ensure_index()


@app.route("/")
def index():
    return render_template("index.html")


# Removed the old /init_index route completely


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    q = data.get("question", "")
    if not q:
        return jsonify({"error": "No question provided"}), 400

    try:
        answer = answer_question(q)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
