from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Cocktail, cocktail_schema, cocktails_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee4444': 'haw4444'}

@api.route('/cocktails', methods = ['POST'])
@token_required
def create_cocktail(current_user_token):
    cocktailname = request.json['cocktailname']
    alcohol = request.json['alcohol']
    garnish = request.json['garnish']
    calories = request.json['calories']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    cocktail = Cocktail(cocktailname, alcohol, garnish, calories, user_token = user_token )

    db.session.add(cocktail)
    db.session.commit()

    response = cocktail_schema.dump(cocktail)
    return jsonify(response)

@api.route('/cocktails', methods = ['GET'])
@token_required
def get_cocktail(current_user_token):
    a_user = current_user_token.token
    cocktails = Cocktail.query.filter_by(user_token = a_user).all()
    response = cocktails_schema.dump(cocktails)
    return jsonify(response)

@api.route('/cocktails/<id>', methods = ['GET'])
@token_required
def get_contact_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        cocktail = Cocktail.query.get(id)
        response = cocktail_schema.dump(cocktail)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401


@api.route('/cocktails/<id>', methods = ['POST','PUT'])
@token_required
def update_cocktail(current_user_token,id):
    cocktail = Cocktail.query.get(id) 
    cocktail.cocktailname = request.json['cocktailname']
    cocktail.alcohol = request.json['alcohol']
    cocktail.garnish = request.json['garnish']
    cocktail.calories = request.json['calories']
    cocktail.user_token = current_user_token.token

    db.session.commit()
    response = cocktail_schema.dump(cocktail)
    return jsonify(response)


# DELETE car ENDPOINT
@api.route('/cocktails/<id>', methods = ['DELETE'])
@token_required
def delete_cocktail(current_user_token, id):
    cocktail = Cocktail.query.get(id)
    db.session.delete(cocktail)
    db.session.commit()
    response = cocktail_schema.dump(cocktail)
    return jsonify(response)