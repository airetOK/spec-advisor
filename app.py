from flask import Flask
from specialized_scheduler import SpecializedScheduler
from db.specialized_repository import SpecializedRepository
import json
import sqlite3

app = Flask(__name__)
scheduler = SpecializedScheduler()
repository = SpecializedRepository()
scheduler.run()

def get_db_connection():
    conn = sqlite3.connect('db/specialized.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/bikes')
def bikes():
    return repository.select(get_db_connection(), 'bikes')


@app.route('/sales')
def sales():
    return repository.select(get_db_connection(), 'sales')


@app.route('/shoes')
def shoes():
    return repository.select(get_db_connection(), 'shoes')


@app.route('/helmets')
def helmets():
    return repository.select(get_db_connection(), 'helmets')


@app.route('/pedals')
def pedals():
    return repository.select(get_db_connection(), 'pedals')


@app.route('/wheels')
def wheels():
    return repository.select(get_db_connection(), 'wheels')


if __name__ == '__main__':
    app.run()
