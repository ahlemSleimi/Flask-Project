from flask import Flask,request,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from core import app
from flask_marshmallow import Marshmallow






# configure the SQLAlchemy connection

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)

'''all the classes related to the application with many to many relatioship between item and orders'''

'''class contact'''
class contact(db.Model):
    __tablename__ = "contact"
    
    ID=db.Column(db.String(50), primary_key=True, nullable=False)
    AccountName=db.Column(db.String(50))
    AddressLine1=db.Column(db.String(50))
    AddressLine2=db.Column(db.String(50))
    City=db.Column(db.String(50))
    ContactName=db.Column(db.String(50))
    Country=db.Column(db.String(2))
    ZipCode=db.Column(db.Integer)
    commandes = db.relationship('commande', backref='contact')

    
    def __init__(self, id,accountN, adressl1,adressl2,city,contactName, country, zipcode):
        self.ID = id
        self.AccountName=accountN
        self.AddressLine1=adressl1
        self.AddressLine2=adressl2
        self.City=city
        self.ContactName=contactName
        self.Country=country
        self.ZipCode=zipcode



    
    
'''association class between commande and article '''    
class articleCo(db.Model):
    __tablename__ = "article_co"
    
    id=db.Column(db.Integer,autoincrement=True , primary_key=True, nullable=False)
    Quantity=db.Column('Quantity',db.Integer)
    Amount=db.Column('Amount',db.Float)
    VATAmount=db.Column('VATAmount',db.Float)
    VATPercentage=db.Column('VATPercentage',db.Float)
    item_id=db.Column('item_id',db.String(50), db.ForeignKey("item.Item"))
    order_id=db.Column('order_id',db.String(50), db.ForeignKey("order.OrderID"))    
    def __init__(self) -> None:

            self.Quantity=None
            self.Amount=None
            self.VATAmount=None
            self.VATPercentage=None
            self.item_id=None
            self.order_id=None
            
        

    
    

'''the class describing the items available '''
class article(db.Model):
    __tablename__ = "item"
    
    Item=db.Column(db.String(50), primary_key=True, nullable=False)
    ItemDescription	=db.Column(db.String(50))
    Description=db.Column(db.String(50))
    Discount=db.Column(db.Double)
    UnitCode=db.Column(db.String(50))
    UnitDescription=db.Column(db.String(50))
    UnitPrice=db.Column(db.Float)
    
    #commandes = db.relationship(commande, secondary="article_co",backref='item.Item')
    #orders= db.relationship('commande' ,backref=db.backref('items'),lazy='dynamic')

'''class describe the orders'''
class commande(db.Model):
    
    __tablename__ = "order"
    
    OrderID=db.Column(db.String(50), primary_key=True, nullable=False)
    OrderNumber=db.Column(db.Integer,unique = True , nullable=False)
    Currency=db.Column(db.String(3))			
    Amount=db.Column(db.Float)
    DeliverTo=db.Column(db.String(50), db.ForeignKey('contact.ID'))
    
    articles = db.relationship( 'article' , secondary='article_co', backref='commande')
    
    
   





'''the mapping btween the database and the provided classes'''
class contactSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = contact
        load_instance = True
        sqla_session = db.session

contact_schema = contactSchema
contact_schemas = contactSchema(many=True)

class commandeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = commande
        load_instance = True
        sqla_session = db.session

cmd_schema = commandeSchema
cmds_schema = commandeSchema(many=True)

class articleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = article
        load_instance = True
        sqla_session = db.session

artl_schema = articleSchema
artls_schema = articleSchema(many=True)

class articleCoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = articleCo
        load_instance = True
        sqla_session = db.session

artlco_schema = articleSchema
artlcos_schema = articleSchema(many=True)





               




'''application context to run the flask app'''
try:
     with app.app_context():
        db.create_all()
        db.session.commit()
except:
        print('"tables exist"' )