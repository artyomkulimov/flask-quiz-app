from website import db, app
import os

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=os.getenv("PORT", default=5000))