
from core import *
from core.Models import *
from flask import Flask, abort, request,jsonify
import requests
from core.Models import app
import csv
import pandas as pd






@app.route('/orders', methods=['GET'])
def get_all_orders():
    all_commande = commande.query.all()
    return jsonify(cmds_schema.dump(all_commande))



@app.route('/flow/orders_to_csv',methods=['Post'])
def addOrders():
    
    url = 'https://4ebb0152-1174-42f0-ba9b-4d6a69cf93be.mock.pstmn.io/orders'
    headers = {'x-api-key': 'PMAK-62642462da39cd50e9ab4ea7-815e244f4fdea2d2075d8966cac3b7f10b'}
    res=requests.get(url, headers=headers)
    x=res.json()
    fcsv=[]
    # the structure of the json data 
    x['results'][0]['Amount']=171
    x['results'][1] #second json in the result 
    x['results'][1]['SalesOrderLines']['results'][0] #first json orderline in the second order
    
   
    for z in x:
        for i in range(len(x[z])):
            for m in (x[z][i]['SalesOrderLines']['results']):
                        
                        existing_item = article.query.filter(article.Item == m.get('Item')).one_or_none()
                        if existing_item is None:
                            #print(m.get('ItemDescription'))
                            itemobj=article()
                            itemobj.Item=m.get('Item')
                            itemobj.ItemDescription=m.get('ItemDescription')
                            itemobj.UnitCode=m.get('UnitCode')
                            itemobj.Discount=m.get('Discount')
                            itemobj.UnitPrice=m.get('UnitPrice')
                            itemobj.Description=m.get('Description')
                            itemobj.UnitDescription=m.get('UnitDescription')
                          
                            
                            
                            
                            
    commandes = []
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
        for key,value in comande.get('SalesOrderLines').items():
                print("here", key )
                for item in value:
                    existing_item = article.query.filter(article.Item == item.get('Item')).one_or_none()
                    print(existing_item)
                    if existing_item is not None:
                    #print(" second for",item.get('Amount'))
                        itemcobj=articleCo()
                        itemcobj.Amount=item.get('Amount')
                        itemcobj.Quantity=item.get('Quantity')
                        itemcobj.VATAmount=item.get('VATAmount')
                        itemcobj.VATPercentage=item.get('VATPercentage')
                        itemcobj.order_id=comande.get('OrderID')
                        itemcobj.item_id=item.get('Item')
                        db.session.add(itemcobj)
                db.session.commit()
        with open("nouvelles commandes.csv", 'w') as csvfile:
                wr = csv.writer(csvfile, delimiter=' ')
                wr.writerow(["champ","description"])
                for key, value in comande.items():
                    wr.writerow([key, value])    
    
    return "done"
                
 



'''add the new contact from the flow '''
@app.route('/addcontacts',methods=['Post'])
def addContact():
        url='https://4ebb0152-1174-42f0-ba9b-4d6a69cf93be.mock.pstmn.io/contacts'
        headers={'x-api-key':'PMAK-62642462da39cd50e9ab4ea7-815e244f4fdea2d2075d8966cac3b7f10b'}
        res=requests.get(url,headers=headers)
        x=res.json()
        lc=[]
        #print(x)
        for z in x:
            for i in range(len(x[z])):
                    #print(" here data "+x[z][i]['ID'] )    
                    obj=contact(x[z][i]['ID'],x[z][i]['AccountName'],x[z][i]['AddressLine1'],x[z][i]['AddressLine2'],x[z][i]['City'],x[z][i]['ContactName'],x[z][i]['Country'],x[z][i]['ZipCode'])   
                    existing_contact = contact.query.filter(contact.ID == obj.ID).one_or_none()
                    if existing_contact is None:
                         print(" this person added")
                         lc.append(obj)
                         
                    else:
                         print(f"Person with last name already exists")
                       
        db.session.add_all(lc)
        
        db.session.commit()
        print("done") 
        return  contact_schemas.jsonify([objc for objc in lc])         
                    
        
@app.route('/contacts', methods=['GET'])                    
def getContact():
    all_contact = contact.query.all()
    return jsonify(contact_schemas.dump(all_contact))


    
@app.route('/contacts/<string:id>/', methods=['GET'])   
def getContactbyId(id):
    contact_ID=contact.query.get(id)
    return jsonify(contact_schema.dump(contact_ID))
    
