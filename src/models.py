from datetime import datetime
from flask import g, request
import sqlite3
import config

def get_db():
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect(config.get_config().get('main', 'db_path'))
    return conn

def date():
    return datetime.now().strftime('%Y-%m-%d')

def get_all_employees():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employe")

    return Employe.get_list_from_db(cur.fetchall())

def get_employe(employe_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employe WHERE id = ?", (employe_id,))

    return Employe(cur.fetchone())

def get_all_fired_employees():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employe WHERE is_active = 0 ORDER BY firing_date DESC")

    return Employe.get_list_from_db(cur.fetchall())

def get_votes_for_employe_id(employe_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vote WHERE employe_id = ?", (employe_id,))

    return cur.fetchall()

def add_vote(employe, value):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO vote(employe_id, ip, vote) VALUES (?,?,?)", (employe.id,request.remote_addr, value))
    conn.commit()

# request.remote_addr
class Employe:

    def __init__(self, data):
        self.id = data[0]
        self.name = data[1]
        self.last_name = data[2]
        self.photo = data[4]
        self.is_active = data[5]
        self.newly_fired = False
        self.score = 0

        if self.is_active == 0:
            self.firing_date = datetime.strptime(data[6], '%Y-%m-%d %H:%M:%S')
            if int((datetime.now() - self.firing_date).total_seconds() / 86400) < 30:
                self.newly_fired = True

            self.compute_score()
        else:
            self.firing_date = None

    @staticmethod
    def get_list_from_db(listDB):
        employe_list = []
        for row in listDB:
            employe_list.append(Employe(data=row))

        return employe_list

    def compute_score(self):
        votes = get_votes_for_employe_id(self.id)
        total_score = 0
        for vote in votes:
            total_score += vote[3]

        self.score = total_score
        self.votes = votes

        return None

    def has_received_vote_from_current_ip(self):
        for vote in self.votes:
            if vote[2] == request.remote_addr:
                # We need to find a better solution to limit vote
                return False

        return False
