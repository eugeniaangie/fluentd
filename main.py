from flask import Flask, jsonify
from elasticsearch import Elasticsearch

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Inisialisasi koneksi ke Elasticsearch
es = Elasticsearch(['http://elasticsearch:9200'])  # Menggunakan host 'elasticsearch' yang diarahkan ke kontainer Elasticsearch di Docker Compose

# Rute untuk pencarian
@app.route('/search')
def search():
    try:
        # Membuat query untuk pencarian
        body = {
            "query": {
                "match_all": {}
            }
        }

        # Melakukan pencarian ke Elasticsearch untuk mendapatkan semua dokumen dari indeks 'fluentd-file'
        response = es.search(index='fluentd-file', body=body)

        # Mendapatkan hasil pencarian
        hits = response['hits']['hits']
        results = [{'id': hit['_id'], 'content': hit['_source']['content']} for hit in hits]

        # Mengembalikan hasil pencarian dalam format JSON
        return jsonify({'results': results})
    except Exception as e:
        # Jika terjadi kesalahan, kembalikan pesan error
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Menjalankan aplikasi Flask pada port 5000
    app.run(debug=True, host='0.0.0.0')  # Menggunakan host '0.0.0.0' agar aplikasi dapat diakses dari luar kontainer Docker
