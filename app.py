import os
from flask import Flask
from flask_jwt import JWT
from flask_restful import Api
from resources.item import ItemList, Item
from security import authenticate, identity
from resources.user import UserRegister
from resources.store import Store, StoreList

# configuracion
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') #el segundo es el valor por defecto
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'pato'
api = Api(app)

jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)

# Recursos
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
