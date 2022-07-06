import os
from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from werkzeug.utils import secure_filename
from gcloud import storage
import pandas


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


users = []
users.append(User(id=1, username='pratik', password='pratik95'))
users.append(User(id=2, username='shival', password='alpha123'))
users.append(User(id=3, username='riya', password='riya01'))

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['inputFile']
        df = pandas.read_csv(request.files.get('inputFile'))
        if secure_filename(file.filename) != '':
            # filename = secure_filename(file.filename)
            # file.save(secure_filename(file.filename))
            print(type(secure_filename(file.filename)))
            client = storage.Client()
            bucket = client.get_bucket('ad_data_raw')
            bucket.blob("webpage/" + secure_filename(file.filename)).upload_from_string(df.to_csv(), 'text/csv')
            # blob = bucket.blob("webpage/" + secure_filename(file.filename))
            # blob.upload_from_filename(secure_filename(file.filename))
            return render_template('thank_you.html')
        else:
            return render_template('profile.html')



    return render_template('profile.html')


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)), host='0.0.0.0', debug=True)
