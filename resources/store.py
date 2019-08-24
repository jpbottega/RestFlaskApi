from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument('name', type=str, required=True, help="This field cannot be left blank")
    # parser.add_argument('items', type=list, required=False, help="")

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {"message": "Store was not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "Store with name {} already exists".format(name)}, 400
        # data = Store.RequestParser.parse_args()
        new_store = StoreModel(name)
        try:
            new_store.upsert()
        except:
            return {"message": "An error occurred while creating the store"}, 500
        return new_store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "Store was deleted"}, 200
        return {"message": "Store does not exist"}, 400


class StoreList(Resource):
    def get(self):
        return {"stores": list(map(lambda x: x.json(), StoreModel.query.all()))}