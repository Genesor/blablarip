#!/usr/bin/env python

from PyBambooHR import PyBambooHR
from fabric.tasks import execute
from datetime import datetime, timedelta
import argparse
import sqlite3
import config
import pprint


config = config.get_config()
bamboo = PyBambooHR(subdomain='blablacar', api_key=config.get('main', 'bamboo_api'))

def get_db():
    conn = sqlite3.connect(config.get('main', 'db_path'))
    return conn

def init_employes():
    employees = bamboo.get_employee_directory()
    conn = get_db()

    counter = 0;
    for employe in employees:
      cur = conn.cursor()
      cur.execute("SELECT * FROM employe WHERE id = "+employe['id'])

      if cur.fetchone() == None:
        counter =+ 1
        conn.execute('INSERT INTO employe(id, first_name, last_name, job_title, photo, is_active) VALUES (?,?,?,?,?,1)', (employe['id'], employe['firstName'], employe['lastName'], employe['jobTitle'], employe['photoUrl']))

    conn.commit()
    print str(counter)+" employess added"
    conn.close()

def get_recently_deleted():
    twoweeks = datetime.now() - timedelta(days=15)
    changes = bamboo.get_employee_changes(twoweeks, 'deleted')
    conn = get_db()

    counter = 0;
    for deleted in changes:
      cur = conn.cursor()
      cur.execute("SELECT * FROM employe WHERE id = ?", (str(deleted['userId']),))

      if cur.fetchone() != None:
        counter =+ 1
        conn.execute('UPDATE employe SET is_active = 0, firing_date = ? WHERE id = ?', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(deleted['userId'])))

    conn.commit()
    print str(counter)+" employess missing"
    conn.close()

def update_photos():
    employees = bamboo.get_employee(41066)
    conn = get_db()

    pprint.pprint(employees);


    # for employe in employees:
    #   cur = conn.cursor()
    #   cur.execute("SELECT * FROM employe WHERE id = "+employe['id'])

    #   if cur.fetchone() != None:
    #     conn.execute('UPDATE employe SET photo = ? WHERE id = ?', (employe['photoUrl'], employe['id'],))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('task', help='[init,deleted,hired]')
    args = parser.parse_args()

    if args.task == 'init':
        execute(init_employes)
    elif args.task == 'deleted':
        execute(get_recently_deleted)
    elif args.task == 'hired':
        execute(init_employes)
    elif args.task == 'photo':
        execute(update_photos)

    else:
        print "Unknown task %s" % args.task
        parser.print_help()