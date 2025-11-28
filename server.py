from flask import Flask, request, jsonify
from llama_cpp import Llama
import logging
import time

app = Flask(__name__)

# Logging mais explícito (melhor pra debug no EasyPanel)
logging.basicConfig(level=logging.INFO)
logger = app.logger

# ================================
#   CARREGAMENTO DO MODELO
# ================================
try:
    logger.info("Iniciando carregamento do modelo Qwen2.5…")

    model = Llama(
        model_path="/opt/easypanel/models/llm/model.gguf",
        chat_format="qwen2.5",         # ✔ FORMATO CORRETO PARA QWEN 2.5
        n_ctx=4096,
        n_threads=4,
        verbose=False
    )

    logger.info("Modelo carregado com sucesso! 🎉")

except Exception as e:
    logger.error(f"Falha ao carregar modelo: {e}")
    model = None


# ================================
#   HEALTHCHECK
# ================================
@app.route("/health", methods=["GET"])
def health():
    if model is None:
        return jsonify({"status": "error", "message": "modelo não carregado"}), 500
    return jsonify({"status": "ok"}), 200


# ================================
#   ENDPOINT /generate
# ================================
@app.route("/generate", methods=["POST"])
def generate():
    if model is None:
        return jsonify({"error": "modelo não carregado"}), 500

    data = request.json or {}
    prompt = data.get("prompt")
    max_tokens = data.get("max_tokens", 256)
    temperature = data.get("temperature", 0.7)

    if not prompt:
        return jsonify({"error": "prompt vazio"}), 400

    try:
        logger.info(f"Gerando resposta… prompt='{prompt[:60]}…'")

        start = time.time()

        completion = model.create_chat_completion(
            messages=[
                {"role": "system", "content": "Você é um assistente útil e direto."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=0.9
        )

        end = time.time()
        logger.info(f"Resposta gerada em {round(end - start, 2)} segundos.")

        response_text = completion["choices"][0]["message"]["content"]

        return jsonify({
            "text": response_text,
            "usage": completion.get("usage", {}),
            "raw": completion
        })

    except Exception as e:
        logger.error(f"Erro ao gerar resposta: {e}")
        return jsonify({"error": "erro interno"}), 500


if __name__ == "__main__":
    # Roda para fora do Docker/Swarm
    app.run(host="0.0.0.0", port=8000)
