from flask import Flask, render_template, request
from flask_cors import CORS

from routes.queues import queues_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"

# Habilitar CORS para permitir testes externos
CORS(app)

app.register_blueprint(queues_bp)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        model = request.form.get("model")
        lamb = request.form.get("arrival_rate")
        mu = request.form.get("service_rate")
        servers = request.form.get("servers")
        capacity = request.form.get("capacity")

        # Aqui futuramente chamaremos o QueueService para calcular
        # Ex: result = QueueService.calculate(...)

        return f"Modelo escolhido: {model}, λ={lamb}, μ={mu}, s={servers}, K={capacity}"

    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
