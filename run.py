#from core.Controller import  *
from flask import Flask, request
import requests
from core import *
from core.Controller import *



'''the server should be run from this class '''
if __name__ == '__main__': 
    
    
    '''application context to run the flask app'''
    try:
        with app.app_context():
            db.create_all()
            db.session.commit()
    except Exception as e  :print(e)
    
    app.run(debug=True)
    
    