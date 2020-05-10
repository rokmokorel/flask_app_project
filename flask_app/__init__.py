from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)

app.config['SECRET_KEY'] = '1A37BbcCJh67'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gesla.sqlite3'
db = SQLAlchemy(app)


class Gesla(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uporabnik = db.Column(db.String(80), nullable=True)
    geslo = db.Column(db.String(15), nullable=False)

    def __init__(self, geslo, uporabnik=""):
        self.uporabnik = uporabnik
        self.geslo = geslo

    def __repr__(self):
        return '<Gesla novi key %s >' % self.geslo

@app.route('/zahtevaj_kljuc', methods = ['POST'])
def nov_kljuc():
    skrivni_kljuc = secrets.token_hex(15)
    usr = Gesla(skrivni_kljuc, "uporabnik")
    db.session.add(usr)
    db.session.commit()
    return str(usr)

@app.route('/preveri_kljuc', methods = ['POST'])
def preveri_kljuc():
    klic = request.headers['geslo']
    ujemanje = Gesla.query.filter_by(geslo=klic).first()
    if ujemanje is None:
        return "0"
    else:
        return "1"

# if __name__ == "__main__":
    # db.create_all()
    # app.run()