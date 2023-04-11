from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, text, Table, Column, Integer, String, MetaData, select

engine = create_engine(
    "postgresql://fatepoints_user:1hMhUuirSk8HY9bvZogU2zr5Ooj8jiCc@dpg-cgidpr9r8t1g7lorckig-a.ohio-postgres.render.com/fatepoints")

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
    c_builder = '<div class="container text-center">'
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            c_builder += '<div class = "row"><div class = "col">'
            c_builder += f"<h1>{row.charactername}</h1>"
            c_builder += '</div></div>'
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
