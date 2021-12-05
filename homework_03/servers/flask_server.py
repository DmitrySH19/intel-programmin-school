from flask import Flask, request, jsonify
import logging
CPU_BOUND = None

app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/post', methods=['POST'])
def request_test():
    if CPU_BOUND:
        return jsonify("num", CPU_BOUND(int(request.json["num"])))
    else:
        return jsonify("num", int(request.json["num"]))



@app.route("/")
def main_page():
    return "<p>Welcome to Flask!</p>"

def run_flask_server(cpu_bound = None):
    global CPU_BOUND
    CPU_BOUND = cpu_bound
    app.run(host='127.0.0.1', port=8090)
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.logger.disabled = True
    print(f'Flask server start',
          f'Waiting new connection...')


def main():
    run_flask_server()

if __name__ == '__main__':
    main()