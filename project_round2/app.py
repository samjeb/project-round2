from flask import Flask
from config import Config
from models import db
from routes.auth import auth_bp
from routes.organisation import organisation_bp
from routes.members import members_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


app.register_blueprint(auth_bp)
app.register_blueprint(organisation_bp)
app.register_blueprint(members_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)


