from django.shortcuts import HttpResponse

import requests
import json
import os


# STORE CREDENTIALS 
STORE_HASH = os.environ.get('STORE_HASH')
XAUTH_TOKEN = os.environ.get('XAUTH_TOKEN')
CONTENT_TYPE = os.environ.get('CONTENT_TYPE')
ACCEPT_TYPE = os.environ.get('ACCEPT_TYPE')





#CUSTOMER CREDENTIALS
emailOfCustomer = "faz12221277@gmail.com"
passwordOfCustomer = "muhammedfazil123#"




CART_ID = "13590f26-ab54-400e-b4f5-426f286539c0"



#--------------------\------------------------------------------------------------------------------------
#<1> CREATEING CUSTOMER IN BC USING DUMMY DATA
# CREATING ACCOUNT IN BC USING THE DATA GETTING FROM AEM 


def createCustomerBc(request):
    url = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/customers"

    payload = [
        {
            "email": emailOfCustomer,
            "first_name": "muhammed",
            "last_name": "fazil",
            "company": "abc",
            "phone": "8590892011",
            "notes": "note1",
            "tax_exempt_category": "string",
            "customer_group_id": 0,
            "addresses": [
                {
                    "address1": "Addr 1",
                    "address2": "",
                    "address_type": "residential",
                    "city": "San Francisco",
                    "company": "History",
                    "country_code": "US",
                    "first_name": "Ronald",
                    "last_name": "Swimmer",
                    "phone": "707070707",
                    "postal_code": "33333",
                    "state_or_province": "California",
                    "form_fields": [
                        {
                            "name": "test",
                            "value": "test"
                        }
                    ]
                }
            ],
            "authentication": {
                "force_password_reset": True,
                "new_password": passwordOfCustomer
            },
            "accepts_product_review_abandoned_cart_emails": True,
            "store_credit_amounts": [{"amount": 43.15}],
            "origin_channel_id": 1,
            "channel_ids": [1],
            "form_fields": [
                {
                    "name": "form name",
                    "value": "form value"
                }
            ]
        }
    ]

    headers = {"Content-Type":  CONTENT_TYPE,"X-Auth-Token":XAUTH_TOKEN}

    response = requests.request("POST", url, json=payload, headers=headers)
    res = response.text
    print('Customer created in bc',)
    print('Response data type',type(res))

    #converted string to json 
    json_object = json.loads(res)
    customer_id = json_object['data'][0]['addresses'][0]['customer_id']

    print('customer id:',type(customer_id))
    print('CUSTOMER CREATED IN BIGCOMMERCE',customer_id)

    return HttpResponse(customer_id)





#--------------------------------------------------------------------------------------------------------
#Validate a customer credentials
#If only valid credentials it shows valid "true" otherwise "false"
#Refer https://developer.bigcommerce.com/api-reference/3d731215a3dcb-validate-a-customer-credentials

def validateCustomerBc(request):
    url = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/customers/validate-credentials"

    payload = {"email": emailOfCustomer,"password": passwordOfCustomer,"channel_id": 1}


    headers = {"Content-Type":  CONTENT_TYPE,"X-Auth-Token":XAUTH_TOKEN}

    response = requests.request("POST", url, json=payload, headers=headers)

    # store the response to variable
    resData = response.text
    print(type(resData))
    print('data',resData)

    return HttpResponse(resData)
    
 
  



# #CREATE CART IN BIGCOMMERCE 
def createCartInBc(request):
    url = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/carts"

    customer_id = 17238
    product_id = 479
    quantity = 10
    list_price = 10
    name = "calendar"


    payload = {
        "customer_id": customer_id,
        "line_items": [
            {
                "quantity": quantity,
                "product_id": product_id,
                "list_price": list_price,
                "name": name
            }
        ],
        "channel_id": 1,
        # "currency": {"code": "USD"},
        # "locale": "en-US" 
    }
    
    headers = {"Content-Type": CONTENT_TYPE,"Accept": ACCEPT_TYPE,"X-Auth-Token": XAUTH_TOKEN}

    response = requests.request("POST", url, json=payload, headers=headers)

    print('CART CREATED IN BIGCOMMERCE:',response.text)

    return HttpResponse(response)



#Creates a Cart,Chekout Redirect URL

def createCartRedirectUrl(request):
    url = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/carts/{CART_ID}/redirect_urls"

    headers = {"Content-Type": CONTENT_TYPE,"Accept": ACCEPT_TYPE,"X-Auth-Token": XAUTH_TOKEN}

    response = requests.request("POST", url, headers=headers)

    print(response.text)
    
    return HttpResponse(response)


























