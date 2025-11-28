from flask import Flask, request, jsonify
from llama_cpp import Llama
import logging

app = Flask(__name__)

# Logging básico pra facilitar debug
logging.basicConfig(level=logging.INFO)
logger = app.logger

# Carregamento do modelo
try:
    logger.info("Carregando modelo...")
    model = Llama(
        model_path="/models/model.gguf",
        n_ctx=4096,
        n_threads=4,
        chat_format="qwen2"   # MUITO IMPORTANTE PARA MODELOS QWEN
    )
    logger.info("Modelo carregado com sucesso!")
except Exception as e:
    logger.error(f"Erro ao carregar modelo: {e}")
    model = None


@app.route("/health", methods=["GET"])
def health():
    """Healthcheck simples para Docker Swarm."""
    if model is None:
        return jsonify({"status": "error", "message": "modelo não carregado"}), 500
    return jsonify({"status": "ok"}), 200


@app.route("/generate", methods=["POST"])
def generate():
    if model is None:
        return jsonify({"error": "modelo não carregado"}), 500

    data = request.json or {}
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "prompt vazio"}), 400

    try:
        logger.info(f"Gerando resposta para: {prompt[:40]}...")

        result = model.create_chat_completion(
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )

        text = result["choices"][0]["message"]["content"]

        return jsonify({"text": text})

    except Exception as e:
        logger.error(f"Erro ao gerar resposta: {e}")
        return jsonify({"error": "erro interno"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
