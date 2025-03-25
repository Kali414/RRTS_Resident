from app import app
from app.auth import auth

app.register_blueprint(auth,url_prefix="/auth")

if(__name__=="__main__"):
    app.run(debug=True)