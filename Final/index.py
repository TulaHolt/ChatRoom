from flask import render_template
from flask.views import MethodView
import gbmodel
import os
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']


class Index(MethodView):
    def get(self):
        model = gbmodel.get_model()
        entries = [dict(name=row[0], streetaddress=row[1], city=row[2], state=row[3], zipcode=row[4], date=row[5], note=row[6]) for row in model.select()]
        return render_template('index.html',entries=entries, client_secret=CLIENT_SECRET, client_id=CLIENT_ID)
