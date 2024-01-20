from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import RegisteredUsersSerializer
from .models import RegisteredUsers
import jwt
import datetime
import urllib.request, urllib.parse, urllib.error
import json
import ssl
import numpy as np
import joblib
import sqlite3 as sql
import pandas as pd
import time
#import random

class SignUpView(APIView) :
    def post(self,request) :

        #Storing newly registered user details into the database
        SIRILZR = RegisteredUsersSerializer(data=request.data)
        SIRILZR.is_valid(raise_exception=True)
        SIRILZR.save()

        #Returnig response
        response = {
            "Name" : SIRILZR.data['name'] ,
            "Message" : "Account created successfully"
        }

        return Response(response)

class SignInView(APIView) :
    def post(self,request) :

        #retrieving user details(emai,password) from login request
        user_email=request.data['email']
        user_pwd=request.data['password']

        current_user=RegisteredUsers.objects.filter(email=user_email).first()

        #Checking if email is registerd 
        if current_user is None :
            raise AuthenticationFailed('User not found')

        #Checking if password is correct
        if not current_user.check_password(user_pwd) :
            raise AuthenticationFailed('Incorrect password!!!')

        
        #Creating the token
        payload_data={
            'id' : current_user.id,
            'name' : current_user.name,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            'iat' : datetime.datetime.utcnow() 
        }

        jwt_token = jwt.encode(payload_data,'secret',algorithm='HS256')

        #Returning response
        return Response({'Token' : jwt_token})

class TokenExpiredView(APIView) :
    def post(self,request) :

        #Checking if token is expired
        try :
            token=request.data['Token']
            actual_data=jwt.decode(token,'secret',algorithms=['HS256'])
            
            return Response({"expired" : "False"})
        
        except :
            return Response({"expired" : "True"}) 

class BiddingView(APIView) :
    def post(self,request) :
        api_key = False
        # If you have a Google Places API key, enter it here
        # api_key = 'AIzaSy___IDByT70'

        if api_key is False:
            api_key = 42
            serviceurl = "http://py4e-data.dr-chuck.net/json?"
        else :
            serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

        # Additional detail for urllib
        # http.client.HTTPConnection.debuglevel = 1

        # Ignore SSL certificate errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        address=request.data['road']
        address = address.strip()

        parms = dict()
        parms["address"] = address
        if api_key is not False: parms['key'] = api_key
        url = serviceurl + urllib.parse.urlencode(parms)

        #print('Retrieving', url)
        uh = urllib.request.urlopen(url, context=ctx)
        data = uh.read().decode()
        #print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))

        try:
            js = json.loads(data)
        except:
            pass
            #print(data)  # We print in case unicode causes an error
            
        if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') :
            print('==== Failure To Retrieve ====')
            #print(data)
            #print('Final Data=', data)


        # HERE WE GOT that has the 'js' that do contain the latitude and longitude.
        location=js['results'][0]['geometry']['location']
        print('\n\n','-'*50, '\nLocation= ', location)
        latlng=np.array([[location['lat']], [location['lng']]]).transpose()

        # NOW UNPICKLE THE THE STANDARD_SCALER AND KNN MODEL TO PREDICT THE CLUSTER CENTRE. 
        st_x=joblib.load('C:\\Users\\User\\Desktop\\Final Year Project\\API\\Server\\ML Model\\fitted_Standard_Scaler.pkl')
        classifier=joblib.load('C:\\Users\\User\\Desktop\\Final Year Project\\API\\Server\\ML Model\\knn_model.pkl')

        #feature Scaling  
        latlng=st_x.transform(latlng)

        cluster_predicted=classifier.predict(latlng)
        #print('predicted cluster =',cluster_predicted)

        #return Response({"Cluster":cluster_predicted})

        db=sql.connect('C:\\Users\\User\\Desktop\\Final Year Project\\API\\Server\\ML Model\\Project_databases.db')
        cur=db.cursor()

        level=cluster_predicted[0]

        cur.execute('''
            SELECT serial_number, state_name, facility_name FROM contractor_database WHERE clusters=%d
            '''%level)
        result=cur.fetchall()

        serial_no=[row[0] for row in result]
        result=[list(tup[1:]) for tup in result]

        result=pd.DataFrame(result, columns=['state_name', 'name'], index=serial_no)

        Threshold=100000
        result['bid']=np.NAN
        result['time']=np.NAN


        ###############################################################################
        #ALLOW BIDDING HERE
        ###############################################################################

        # TEMP CODE
        import random
        some_people_bid=random.randrange(20, len(result))
        print('people bidded=',some_people_bid)
        randomlist = random.sample(serial_no, some_people_bid)
        #print(randomlist)
        for cid in randomlist:
            bid=random.randrange(10000,10000000)
            if bid<Threshold:
                #print(bid, "has Bid too small")
                pass
            else:
                result.loc[cid, 'bid']=bid
                result.loc[cid, 'time']=time.time()

        min_bid=np.nanmin(result.loc[:, 'bid'])
        #print('min bid done=',min_bid)

        final=result[result['bid']==min_bid]
        min_time=np.min(final.loc[: ,'time'])
        final=final[final['time']==min_time]

        #print('The contractor allowed to bid has details:\n'+str(final))
        #print('The contractor index is:',final.index[0])

       
        #for key in final :
        #    contractor_details[key]=final[key][0]
        
        #contractor_details={"Minimal Bid" : min_bid , "Details" : final}

        contractor_details={}

        for i,j in final.items() :
            contractor_details[i]=j.to_numpy()[0]

        #sending response
        return Response(contractor_details)

