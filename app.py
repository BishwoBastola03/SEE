
import requests
from bs4 import BeautifulSoup
import flask
from flask import jsonify, request
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

@app.route('/see-result', methods=['GET'])
def get_see_result():
    symbol_number = request.args.get('symbolno')
    if not symbol_number:
        return jsonify({'error': 'Symbol number is required'}), 400

    url = f"http://nepaltelecom.net/see-result.php?symbolno={symbol_number}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to retrieve result'}), 500

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the result table
    table = soup.find('table', {'class': 'result-table'})
    if not table:
        return jsonify({'error': 'Result not found'}), 404

    # Extract the result data
    result_data = []
    for row in table.find_all('tr')[1:]:  # skip header row
        cols = row.find_all('td')
        result_data.append({
            'subject': cols[0].text,
            'marks': cols[1].text,
            'grade': cols[2].text
        })

    return jsonify({'result': result_data})

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)



