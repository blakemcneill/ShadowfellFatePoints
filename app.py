from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, text, Table, Column, Integer, String, MetaData, select
from os import getenv

engine = create_engine(getenv("db"))

metadata_obj = MetaData()

characters = Table(
    "characters",
    metadata_obj,
    Column("characterid", Integer, primary_key=True),
    Column("charactername", String),
    Column("heroicpoints", Integer),
    Column("villianpoints", Integer),
    Column("neutralpoints", Integer)
)

app = Flask(__name__)


@app.route('/')
def index():
    stmt = select(characters)
    with engine.connect() as conn:
        if conn.execute(stmt).first() is None:
            c_builder = '<h1>No characters</h1>'
        else:
            c_builder = '<div class="container text-left">'
            for row in conn.execute(stmt):
                c_builder += "<div class = \"row\">"
                c_builder += f"<div class = \"col\"><h1>{row.charactername}</h1></div>"
                c_builder += f"<div class=\"col\"><h3>Heroic Points</h3><br /><p>{row.heroicpoints}</p></div>"
                c_builder += f"<div class=\"col\"><h3>Neutral Points</h3><br /><p>{row.neutralpoints}</p></div>"
                c_builder += f"<div class=\"col\"><h3>Villian Points</h3><br /><p>{row.villianpoints}</p></div>"
                c_builder += '</div>'
            c_builder += "</div>"
    return render_template('index.html', character_display=c_builder)


@app.route('/addcharacter', methods=["POST", "GET"])
def addcharacter():
    if request.method == "POST":
        character_name = (request.form['characterName'])
        with engine.connect() as conn:
            conn.execute(text(
                f"INSERT INTO characters (charactername, heroicpoints, villianpoints, neutralpoints) VALUES ('{character_name}',0,0,0)"))
            conn.commit()
        return redirect(url_for('index'))
    else:
        return render_template('addcharacter.html')
