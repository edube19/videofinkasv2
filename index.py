from app import app
from utils.db import db
from flask_cors import CORS

db.init_app(app)
with app.app_context():
    db.create_all()

CORS(app)
cors=CORS(app,resource={
    r"/*":{
        "origins":"*"
    }
})


if __name__ == "__main__":
    app.run(debug=True, port=4000, host="0.0.0.0")