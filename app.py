from datetime import datetime
from flask import Flask, app, render_template

from config import Config
from models import db  
from routes.main import main_bp



def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)
    app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///sharad-ranpise-foundation.db")
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    
    db.init_app(app)

   
    with app.app_context():
        db.create_all()

    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_globals():
        return {
            "current_year": datetime.now().year,
        }

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template("500.html"), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)