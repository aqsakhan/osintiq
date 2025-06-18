from flask import Flask, request, jsonify
from flask_cors import CORS

from core.alert_parser import extract_alert_entities
from core.dispatcher import dispatch_modules

app = Flask(__name__)
CORS(app)

@app.route('/test/dispatch', methods=['POST'])
def test_dispatch():
    alert = request.get_json()
    parsed_alert = extract_alert_entities(alert)
    result = dispatch_modules(parsed_alert)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5050, debug=True)
