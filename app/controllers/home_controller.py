from flask import jsonify, request
from app.config.config import db

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
    query = articles_ref.limit(size).offset((page - 1) * size)
    results = query.stream()

    # list untuk menyimpan data article 
    article_data = []
    for result in results:
        article_info = result.to_dict()
        article_data.append(article_info)

    #return response
    response = {"meta": page,"articles": article_data }
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

    # return response 
    response = {"services": services_data}
    return jsonify(response), 200