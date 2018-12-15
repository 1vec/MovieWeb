from flask import Flask, Response, render_template, request
import json


app = Flask(__name__)

@app.route('/')
def res():
    return render_template('form.html')

@app.route('/resource', methods=['POST'])
def hello():
    print(request.get_json())
    data = {'恐怖片': 10, '喜剧片': 20, '动作片': 100}
    return Response(json.dumps(data))

if __name__ == '__main__':
    app.run()
