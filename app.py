from flask import Flask, render_template, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/saham', methods=['POST'])
def get_saham():
    data = request.get_json()
    kode = data.get('kode')
    tgl_awal = data.get('tanggal_awal')
    tgl_akhir = data.get('tanggal_akhir')

    try:
        saham = yf.download(kode, start=tgl_awal, end=tgl_akhir)

        if saham.empty:
            return jsonify({'error': 'Data saham tidak ditemukan'}), 404

        tanggal = saham.index.strftime('%Y-%m-%d').tolist()
        harga = saham['Close'].fillna(0).values.tolist()

        return jsonify({'tanggal': tanggal, 'harga': harga})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
