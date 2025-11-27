from flask import Flask, request, jsonify
from llama_cpp import Llama

app = Flask(__name__)

model = Llama(
    model_path="/models/model.gguf",
    n_ctx=4096,
    n_threads=4
)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")

    out = model.create_chat_completion(
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.7
    )

    return jsonify({"text": out["choices"][0]["message"]["content"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
