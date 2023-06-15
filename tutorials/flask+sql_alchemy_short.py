from flask import Flask, render_template_string, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' 

db.init_app(app)

class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search = db.Column(db.String(80), unique=True, nullable = False)

    def __init__(self, search):
        self.search = search

    

search_html = '''
<html>
    <head>
        <title>Search</title>
    </head>
    <body>
        <h1>Search</h1>
        <form action="/search" method="POST">
            <label for="search">Search:</label><br>
            <input type="text" id="search" name="search"><br>
            <input type="submit" value="Submit">
        </form>
        {% if success %}
            <p>{{ success }}</p>
        {% endif %}
    </body>
</html>
'''

@app.route('/')
@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        search = request.form['search']
        search = Search(search)
        db.session.add(search)
        db.session.commit()
        return render_template_string(search_html, success=f'Search {search} created!')
    return render_template_string(search_html)

list_html = '''
<html>
    <head>
        <title>Searches</title>
    </head>
    <body>
        <h1>Searches</h1>
        <ul>
            {% for search in searches %}
                <li>{{ search.search }}</li>
            {% endfor %}
        </ul>
    </body>
</html>
'''

@app.route('/list')
def list_searches():
    # only where python in string
    searches = db.session.execute(db.select(Search).where(Search.search.contains('python'))).scalars().all()
    #searches = db.session.execute(db.select(Search)).scalars().all()
    return render_template_string(list_html, searches=searches)


if __name__ == '__main__':
    #with app.app_context():
    #    db.create_all()
    app.run(debug=True, port=5001)

