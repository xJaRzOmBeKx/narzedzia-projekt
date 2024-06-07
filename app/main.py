from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin-db:P@$t@db1@mysql:3306/test_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Historia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operacja = db.Column(db.String(255), nullable=False)
    wynik = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Historia {self.operacja}={self.wynik}>'

# Tworzenie bazy danych
with app.app_context():
    db.create_all()

@app.route('/dodaj', methods=['POST'])
def dodaj():
    dane = request.get_json()
    a = dane.get('a')
    b = dane.get('b')
    wynik = a + b
    zapis_do_bazy('dodawanie', f'{a} + {b}', str(wynik))
    return jsonify(wynik=wynik)

@app.route('/odejmij', methods=['POST'])
def odejmij():
    dane = request.get_json()
    a = dane.get('a')
    b = dane.get('b')
    wynik = a - b
    zapis_do_bazy('odejmowanie', f'{a} - {b}', str(wynik))
    return jsonify(wynik=wynik)

@app.route('/pomnoz', methods=['POST'])
def pomnoz():
    dane = request.get_json()
    a = dane.get('a')
    b = dane.get('b')
    wynik = a * b
    zapis_do_bazy('mnozenie', f'{a} * {b}', str(wynik))
    return jsonify(wynik=wynik)

@app.route('/podziel', methods=['POST'])
def podziel():
    dane = request.get_json()
    a = dane.get('a')
    b = dane.get('b')
    if b == 0:
        return jsonify(error='Dzielenie przez zero!'), 400
    wynik = a / b
    zapis_do_bazy('dzielenie', f'{a} / {b}', str(wynik))
    return jsonify(wynik=wynik)

@app.route('/historia', methods=['GET'])
def historia():
    historie = Historia.query.all()
    wyniki = []
    for h in historie:
        wyniki.append({
            'id': h.id,
            'operacja': h.operacja,
            'wynik': h.wynik
        })
    return jsonify(historia=wyniki)

def zapis_do_bazy(typ_operacji, operacja, wynik):
    nowa_historia = Historia(operacja=operacja, wynik=wynik)
    db.session.add(nowa_historia)
    db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
