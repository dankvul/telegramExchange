from .extensions import db
import time
import requests


class Rates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_request_time = db.Column(db.Integer, default=int(time.time()))
    base = db.Column(db.String, default='USD')
    rates = db.Column(db.JSON)


def update_rates() -> str:
    last_rate = Rates.query.order_by(Rates.last_request_time.desc()).first()
    if last_rate is None:
        req = requests.get(url='https://api.exchangeratesapi.io/latest?base=USD')
        new_rate = Rates(rates=req.json())
        db.session.add(new_rate)
        db.session.commit()
        return 'New rate has been added'

    last_update_time = last_rate.last_request_time // 60
    current_time = int(time.time()) // 60
    if current_time - last_update_time <= 10:
        return 'Current rate is up-to-date'
    req = requests.get(url='https://api.exchangeratesapi.io/latest?base=USD')
    last_rate.rates = req.json()
    db.session.commit()
    return 'Rate has been updated'


def current_rates() -> dict:
    cur = Rates.query.first()
    return cur.rates['rates']
