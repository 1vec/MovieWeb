from flask import Flask, Response, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/box-office')
def box():
    return render_template('box-office.html')

@app.route('/rating')
def rating():
    return render_template('rating.html')

@app.route('/resource', methods=['POST'])
def hello():
    print(request.get_json())
    data = count_type()
    return Response(json.dumps(data))

if __name__ == '__main__':
    app.run()
