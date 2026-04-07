from flask import Flask, redirect, url_for
from blueprints.games import games_bp
from dotenv import load_dotenv 
import os
load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Necessário para usar o 'flash'


app.register_blueprint(games_bp)

@app.route("/")
def index():
    return redirect(url_for("games.listar_jogos"))


if __name__ == "__main__":
    app.run(debug=True)
