from flask import jsonify, request
from app.config.config import db
import math

def get_banner():
    # Query ke Firestore untuk mendapatkan data banner
    banners_ref = db.collection('banners')
    results = banners_ref.stream()

    # list untuk menyimpan data banner
    banners_data = []

    for result in results:
        banner_data = result.to_dict()
        banners_data.append(banner_data)

    # return response json  
    response = {"banners": banners_data}
    return jsonify(response), 200

def articles():
    # query Parameters untuk pagination 
    size = request.args.get('size', type=int)
    page = request.args.get('page', type=int)

    # query ke firestore untuk mendapatkan data article
    articles_ref = db.collection('articles')

    # Hitung total data
    total_data = len(list(articles_ref.stream()))

    # Hitung total halaman
    total_pages = math.ceil(total_data / size)

    # Query untuk halaman tertentu
    query = articles_ref.limit(size).offset((page - 1) * size)
    results = query.stream()

    # list untuk menyimpan data article 
    article_data = []
    for result in results:
        article_info = result.to_dict()
        article_data.append(article_info)

    #return response
    response = {
        "meta": {
            "total_data": total_data,
            "total_pages": total_pages,
            "current_page": page,
            "data_per_page": size
        },
        "articles": article_data
    }

    return jsonify(response), 200

def detail_article(article_id):
    #query firestore untuk mendapatkan detail article berdasarkan 'service_id'
    detail_article_ref = db.collection('articles').document(article_id)
    detail_result = detail_article_ref.get().to_dict()

    # Exclude key yang tidak perlu untuk respons
    excluded_fields = ['article_id']

    # return response
    response = {key: value for key, value in detail_result.items() if key not in excluded_fields}
    return jsonify(response), 200

def services():

    # query ke firestore untuk mendapatkan data services yang akan ditampilkan di home page mobile app
    services_ref = db.collection('home_services')
    results = services_ref.stream()

    # list untuk menyimpan data 'home_services'
    services_data = []
    for result in results:
        service_info = result.to_dict()
        services_data.append(service_info)
    
    # Menghilangkan kunci "id" dari setiap elemen dalam services_data
    services_data_without_id = [{k: v for k, v in service.items() if k != 'id'} for service in services_data]

    # return response 
    response = {"services": services_data_without_id}
    return jsonify(response), 200
