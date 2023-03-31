from core import *
from core.Models import *
from flask import Flask, abort, request,jsonify
import requests
#from core.Models import app
from core import app
import csv





''' this medhod to get all orders from database'''
@app.route('/orders', methods=['GET'])
def get_all_orders():
    all_commande = commande.query.all()
    return jsonify(cmds_schema.dump(all_commande))



'''add the new contact from the flow '''
@app.route('/addcontacts',methods=['Post'])
def addContact():
        urlc='https://4ebb0152-1174-42f0-ba9b-4d6a69cf93be.mock.pstmn.io/contacts'
        headers={'x-api-key':'PMAK-62642462da39cd50e9ab4ea7-815e244f4fdea2d2075d8966cac3b7f10b'}
        resc=requests.get(urlc,headers=headers)
        contacts=resc.json()
        for i in contacts['results']:   
            existing_contact = contact.query.filter(contact.ID == i.get('ID')).one_or_none()
            if existing_contact is None:
                obj=contact(i.get('ID'),i.get('AccountName'),i.get('AddressLine1'),i.get('AddressLine2'),i.get('City'),i.get('ContactName'),i.get('Country'),i.get('ZipCode'))   
                print(" this person added")
                db.session.add(obj)
            db.session.commit()   
        return  "done"    
  




'''this endpoint is to store items and orders into the database and tranforme it to csv file however the forme of the csv is not the right one''' 
@app.route('/flow/orders_to_csv',methods=['Post'])
def addOrders():
    m=addContact()
    print("contact ",m)
    url = 'https://4ebb0152-1174-42f0-ba9b-4d6a69cf93be.mock.pstmn.io/orders'
    headers = {'x-api-key': 'PMAK-62642462da39cd50e9ab4ea7-815e244f4fdea2d2075d8966cac3b7f10b'}
    res=requests.get(url, headers=headers)
    x=res.json()
    
    # # the structure of the json data 
    # x['results'][0]['Amount']=171
    # x['results'][1] #second json in the result 
    # x['results'][1]['SalesOrderLines']['results'][0] #first json orderline in the second order
                            
    with open("nouvelles commandes.csv", 'w') as csvfile:
        wr = csv.writer(csvfile, delimiter=' ')
        wr.writerow(["champ","description"])
        for comande in x['results']:
            
            commd = commande.query.filter(commande.OrderID==comande.get('OrderID')).one_or_none()
            if commd is None:
                orderobj=commande()
                orderobj.Amount=comande.get('Amount')
                orderobj.OrderID=comande.get('OrderID')
                orderobj.OrderNumber=comande.get('OrderNumber')
                orderobj.Currency=comande.get('Currency')
                orderobj.DeliverTo=comande.get('DeliverTo')
            
                db.session.add(orderobj)
            db.session.commit()
            
            wr.writerow(['order',comande.get('OrderID')])
            existing_contact=contact.query.filter_by(ID=comande.get('DeliverTo')).first()
            
            wr.writerow(['delivery_name',existing_contact.ContactName])
            wr.writerow(['delivery_address',existing_contact.AddressLine1])
            wr.writerow(['delivery_country',existing_contact.Country])
            wr.writerow(['delivery_city',existing_contact.City])
            wr.writerow(['delivery_zipcode',existing_contact.ZipCode])
            wr.writerow(['items_count ', len(comande.get('SalesOrderLines')['results'] )])
            ind=1
            
            for key in comande.get('SalesOrderLines')['results']:
                        existing_item = article.query.filter(article.Item == key.get('Item')).one_or_none()
                        
                        if existing_item is None:
                            #print(m.get('ItemDescription'))
                            itemobj=article()
                            itemobj.Item=key.get('Item')
                            itemobj.ItemDescription=key.get('ItemDescription')
                            itemobj.UnitCode=key.get('UnitCode')
                            itemobj.Discount=key.get('Discount')
                            itemobj.UnitPrice=key.get('UnitPrice')
                            itemobj.Description=key.get('Description')
                            itemobj.UnitDescription=key.get('UnitDescription')
                            db.session.add(itemobj)
                        db.session.commit()
                            
                            
                        
                        itemcobj=articleCo()
                        itemcobj.Amount=key.get('Amount')
                        itemcobj.Quantity=key.get('Quantity')
                        itemcobj.VATAmount=key.get('VATAmount')
                        itemcobj.VATPercentage=key.get('VATPercentage')
                        itemcobj.order_id=comande.get('OrderID')
                        itemcobj.item_id=key.get('Item')
                        db.session.add(itemcobj)
                        db.session.commit()
                        
                        wr.writerow(['item_index', ind]) 
                        wr.writerow(['item_id',key.get('Item')]) 
                        wr.writerow(['item_quantity',key.get('Quantity')]) 
                        wr.writerow(['line_price_excl_vat',key.get('Amount')]) 
                        wr.writerow(['line_price_incl_vat',key.get('VATAmount')+key.get('Amount')]) 
                        ind+=1
                    
            
            
    return "done"


 
def analytics():
     pass
 
          
 


                  
'''get all the contacts in the database  '''       
@app.route('/contacts', methods=['GET'])                    
def getContact():
    all_contact = contact.query.all()
    return jsonify(contact_schemas.dump(all_contact))


# '''get contact by id '''
# @app.route('/contactID/<string:id>')   
# def getContactbyId(id: str):
#     contact_ID= contact.query.filter_by(ID=id).first()
#     return jsonify(contact_schema.dump(contact_ID))

    





# @app.route('/csv')  
# def csvfile():
#     url = 'https://4ebb0152-1174-42f0-ba9b-4d6a69cf93be.mock.pstmn.io/orders'
#     headers = {'x-api-key': 'PMAK-62642462da39cd50e9ab4ea7-815e244f4fdea2d2075d8966cac3b7f10b'}
#     res=requests.get(url, headers=headers)
#     s=res.json()
    
#     # with open("nouvelles commandes.csv", 'w') as csvfile:
#     #     wr = csv.writer(csvfile, delimiter=' ')
#     #     wr.writerow(["champ","description"])
#     #for cmd in s['results']:
#             #wr.writerow(['order',cmd.get('OrderID')])
            
            
            
#             # wr.writerow(['delivery_name',existing_contact.ContactName])
#             # wr.writerow(['delivery_address',existing_contact.AddressLine1])
#             # wr.writerow(['delivery_country',existing_contact.Country])
#             # wr.writerow(['delivery_city',existing_contact.City])
#             # wr.writerow(['delivery_zipcode',existing_contact.ZipCode])
#             # wr.writerow(['items_count ', len(cmd.get('SalesOrderLines')['results'] )])
#             # ind=1
#             # for key in cmd.get('SalesOrderLines')['results']:
                
#             #     wr.writerow(['item_index', ind]) 
#             #     wr.writerow(['item_id',key.get('Item')]) 
#             #     wr.writerow(['item_quantity',key.get('Quantity')]) 
#             #     wr.writerow(['line_price_excl_vat',key.get('Amount')]) 
#             #     wr.writerow(['line_price_incl_vat',key.get('VATAmount')+key.get('Amount')]) 
#             #     ind+=1
               
                         
                        

                                        
