from flask import Flask, render_template, url_for

app = Flask(__name__)
app.add_url_rule('/', endpoint='home')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/box-office')
def box_office():
    return render_template('box-office.html')


@app.route('/rating')
def rating():
    return render_template('rating.html')


if __name__ == '__main__':
    app.run()
