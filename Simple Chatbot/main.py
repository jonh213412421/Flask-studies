from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Lista que guarda as mensagens
messages = []

@app.route("/", methods=["GET", "POST"])
def index():
    # if post, ou seja, se for enviado pelo chat...
    if request.method == "POST":
        # Pega a mensagem
        message = request.form["message"]
        # estrutura para responder de acordo com o input. Coração
        if message == "tenho uma dúvida":
            messages.append(message)
            messages.append("pode perguntar")
        else:
            messages.append(message)
            messages.append("a única opção possível é 'tenho uma dúvida'")
        # envia as mensagens para a página
        return jsonify({"status": "Message added", "messages": messages})
    # caso contrário, renderiza a página
    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
