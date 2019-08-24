from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')
    # lazy='dynamic' para que no traiga todos los items cada vez que la creo

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': list(map(lambda x: x.json(), self.items.all()))}
        # el lazy afecta al items, se convierte en un query

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def upsert(self):
        db.session.add(self)
        db.session.commit()
