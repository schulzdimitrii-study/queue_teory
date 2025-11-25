from flask import Blueprint, jsonify, request

from models.queue_factory import QueueFactory

queues_bp = Blueprint("queues", __name__)


@queues_bp.route("/queues", methods=["GET"])
def queues():
    return "Queues Route"


@queues_bp.route("/api/models", methods=["GET"])
def get_models():
    """Lista modelos disponíveis"""
    return jsonify({"models": QueueFactory.get_available_models()})


@queues_bp.route("/api/calculate", methods=["POST"])
def calculate():
    """Endpoint para calcular métricas de fila"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Nenhum dado fornecido"}), 400

        model_type = data.get("model_type")
        if not model_type:
            return jsonify({"error": "model_type é obrigatório"}), 400

        model_info = QueueFactory.get_model_info(model_type)

        params = {}

        # Parâmetros comuns - sempre obrigatórios
        params["lamb"] = float(data.get("lamb", 0))
        params["mu"] = float(data.get("mu", 0))

        # Parâmetros específicos por modelo - apenas se listados nos params
        if "s" in model_info.get("params", []):
            params["s"] = int(data.get("s", 1))

        if "k" in model_info.get("params", []):
            params["k"] = int(data.get("k", 0))

        if "n" in model_info.get("params", []):
            params["n"] = int(data.get("n", 0))

        if "N" in model_info.get("params", []):
            params["N"] = int(data.get("N", 0))

        if "r" in model_info.get("params", []):
            params["r"] = int(data.get("r", 0))

        if "t" in model_info.get("params", []):
            params["t"] = float(data.get("t", 0))

        # Parâmetros especiais para modelos com prioridades
        if "lamb_list" in model_info.get("params", []):
            lamb_list = data.get("lamb_list", [])
            if isinstance(lamb_list, str):
                # Parse string como lista: "1,2,3" -> [1.0, 2.0, 3.0]
                lamb_list = [
                    float(x.strip()) for x in lamb_list.split(",") if x.strip()
                ]
            params["lamb_list"] = lamb_list

        # Criar fila e calcular métricas
        queue = QueueFactory.create_queue(model_type, **params)
        metrics = queue.calculate_metrics()

        # Serializar métricas
        serialized_metrics = _serialize_metrics(metrics)

        return (
            jsonify(
                {
                    "success": True,
                    "model": model_type,
                    "model_name": model_info.get("name", model_type),
                    "metrics": serialized_metrics,
                }
            ),
            200,
        )

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Erro interno: {str(e)}"}), 500


def _serialize_metrics(metrics: dict) -> dict:
    """Converte valores não-serializáveis para JSON"""
    serialized = {}
    for key, value in metrics.items():
        if value == float("inf"):
            serialized[key] = "infinity"
        elif value == float("-inf"):
            serialized[key] = "-infinity"
        elif isinstance(value, float):
            serialized[key] = round(value, 6)
        else:
            serialized[key] = value
    return serialized
