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

plus_button = """
<button class="btn btn-primary">
   +
</button>
"""

minus_button = """
<button class="btn btn-danger">
   -
</button>
"""

delete_button = """
<button class="btn btn-secondary">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
      <path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5ZM11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H2.506a.58.58 0 0 0-.01 0H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1h-.995a.59.59 0 0 0-.01 0H11Zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5h9.916Zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47ZM8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5Z"/>
    </svg>
</button>
"""

@app.route('/')
def index():
    stmt = select(characters)
    with engine.connect() as conn:
        if conn.execute(stmt).first() is None:
            c_builder = '<h1>No characters</h1>'
        else:
            c_builder = '<div class="container-left text-left">'
            for row in conn.execute(stmt):
                c_builder += "<div class = \"row\">"
                c_builder += f"<div class = \"col\"><h1>{row.charactername}</h1>{delete_button}</div>"
                c_builder += f"<div class=\"col\"><h3>Heroic Points</h3><br />{row.heroicpoints}{plus_button}{minus_button}</div>"
                c_builder += f"<div class=\"col\"><h3>Villain Points</h3><br />{row.villianpoints}{plus_button}{minus_button}</div>"
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
