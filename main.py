# from fasthttppy import FastHttp, MakeResponse, Request

# # Import lain yang diperlukan
# from elasticsearch import AsyncElasticsearch
# import json

# # Inisialisasi koneksi ke Elasticsearch
# es = AsyncElasticsearch(['http://localhost:9200'])

# # Fungsi untuk menangani request pencarian
# async def handle_search(request: Request) -> MakeResponse:
#     query = request.query.get('fl')

#     # Jika query tidak ada, kembalikan pesan error
#     if not query:
#         return MakeResponse(json.dumps({'error': 'Parameter is required'}).encode(), content_type='application/json', status=400)

#     try:
#         body = {
#             'query': {
#                 'match': {
#                     'content': query
#                 }
#             }
#         }

#         # Melakukan pencarian ke Elasticsearch
#         response = await es.search(index='fluentd-file', body=body)

#         # Mendapatkan hasil pencarian
#         hits = response['hits']['hits']
#         results = [{'id': hit['_id'], 'content': hit['_source']['content']} for hit in hits]

#         # Mengembalikan hasil pencarian dalam format JSON
#         return MakeResponse(json.dumps({'results': results}).encode(), content_type='application/json')
#     except Exception as e:
#         # Jika terjadi kesalahan, kembalikan pesan error
#         return MakeResponse(json.dumps({'error': str(e)}).encode(), content_type='application/json', status=500)

# # Inisialisasi aplikasi FastHttp
# app = FastHttp()
# app.route('/search', methods=['GET'])(handle_search)

# # Menjalankan aplikasi pada port 8080
# if __name__ == '__main__':
#     app.run(port=8080)


# from flask import Flask, request, jsonify
# from elasticsearch import Elasticsearch

# # Inisialisasi aplikasi Flask
# app = Flask(__name__)

# # Inisialisasi koneksi ke Elasticsearch
# es = Elasticsearch(['http://localhost:9200'])

# # Rute untuk pencarian
# @app.route('/search')
# def search():
#     # Mendapatkan query pencarian dari parameter 'q' dalam URL
#     query = request.args.get('param')

#     # Jika query tidak ada, kembalikan pesan error
#     if not query:
#         return jsonify({'error': 'Parameter is required'}), 400

#     # Membuat query untuk pencarian
#     body = {
#         'query': {
#             'match': {
#                 'content': query
#             }
#         }
#     }

#     try:
#         # Melakukan pencarian ke Elasticsearch
#         response = es.search(index='fluentd-file', body=body)

#         # Mendapatkan hasil pencarian
#         hits = response['hits']['hits']
#         results = [{'id': hit['_id'], 'content': hit['_source']['content']} for hit in hits]

#         # Mengembalikan hasil pencarian dalam format JSON
#         return jsonify({'results': results})
#     except Exception as e:
#         # Jika terjadi kesalahan, kembalikan pesan error
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     # Menjalankan aplikasi Flask pada port 5000
#     app.run(debug=True)

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
