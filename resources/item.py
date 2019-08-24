from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id")

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message": "Failed while searching the database"}, 500
        if item:
            return item.json(), 200
        return {"message": 'item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item value with name '{}' already exists".format(name)}, 400
        json_payload = Item.parser.parse_args()
        item = ItemModel(name, json_payload['price'], json_payload['store_id'])
        try:
            item.upsert()
        except:
            return {"message": "An error occurred inserting the item"}, 500
        return item.json(), 201

    def delete(self, name):
        try:
            item = ItemModel.find_by_name(name)
            if item:
                item.delete_from_db()
        except:
            return {'message': "Error occurred while deleting the item"}, 500
        return {'message': "item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            try:
                item = ItemModel(name, data['price'], data['store_id'])
            except:
                return {"message": "An error occurred while inserting the item"}, 500
        else:
            try:
                item.price = data['price']
                item.store_id = data['store_id']
            except:
                return {"message": "An error occurred while updating the item"}, 500
        item.upsert()
        return item.json(), 200


class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all() ))
