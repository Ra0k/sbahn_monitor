from flask import Flask, jsonify
from mvv_reader import find_sbahn_station


app = Flask(__name__)

@app.route('/station/<station_name>/id', methods=["GET"])
def get_station_id(station_name):
    return jsonify({
        'station_name': station_name,
        'station_id': 12
    })

@app.route('/real_station/<station_name>/id', methods=["GET"])
def get_real_station_id(station_name):
    return jsonify(find_sbahn_station(station_name))


if __name__ == '__main__':
    app.run(debug=True)