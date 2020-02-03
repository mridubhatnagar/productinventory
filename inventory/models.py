from datetime import datetime
from inventory import db



class Product(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(200), nullable=False, unique=True)
    product_movement = db.relationship('ProductMovement', backref='product', lazy=True)

    def __repr__(self):
        return "{}".format(self.id)

class Location(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(200), nullable=False, unique=True)

    def __repr__(self):
        return "{}".format(self.id)

class ProductMovement(db.Model):

    __tablename__ = 'product_movement'
    
    id=db.Column(db.Integer(), primary_key=True)
    product_id = db.Column(db.Integer(), db.ForeignKey('product.id'), nullable=False)
    
    from_location_id = db.Column(db.Integer(), db.ForeignKey('location.id'), nullable=True)
    to_location_id  = db.Column(db.Integer(), db.ForeignKey('location.id'), nullable=True)
    
    from_location = db.relationship('Location', foreign_keys=[from_location_id])
    to_location = db.relationship('Location', foreign_keys=[to_location_id])


    quantity = db.Column(db.Integer)

    def __repr__(self):
        return "{}".format(self.id)
    