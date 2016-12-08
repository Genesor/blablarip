from models import get_all_employees, get_all_fired_employees, get_employe, add_vote
from flask import Flask, request, session, redirect, url_for, render_template, flash, g
import pprint
import os

application = Flask(__name__)

@application.route('/')
def index():
    empl = get_all_fired_employees()

    return render_template('index.html', employees=empl)

@application.route('/vote/<int:employe_id>')
def vote(employe_id):
    vote_value = int(request.args.get('value'))
    employe = get_employe(employe_id)

    if ((vote_value == 1 or vote_value == -1)
        and employe.is_active == 0
        and employe.has_received_vote_from_current_ip() == False):
      add_vote(employe, vote_value)

    return redirect(url_for('index'))

@application.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)