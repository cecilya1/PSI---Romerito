from flask import Flask, render_template, request, make_response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cores")
def cores():
    if 'cor' in request.args.values():
        cor = request.args.get('cor')
    else:
        cor = request.cookies.get('cor')

    response = make_response(render_template('cookies.html', cor=cor))
    response.set_cookie('cor', cor)
    return response
    # return render_template('cookies.html', cor=cor)