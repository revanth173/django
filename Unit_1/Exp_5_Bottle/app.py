from bottle import route, run
@route('/')
def index(): return '<b>Hello Bottle Framework</b>'
run(host='localhost', port=8000, debug=True)