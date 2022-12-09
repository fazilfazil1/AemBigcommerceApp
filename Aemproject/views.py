from django.shortcuts import HttpResponse

import requests
import json
import os



# STORE CREDENTIALS 
STORE_HASH = os.environ.get('STORE_HASH')
XAUTH_TOKEN = os.environ.get('XAUTH_TOKEN')
CONTENT_TYPE = os.environ.get('CONTENT_TYPE')





#CUSTOMER CREDENTIALS
emailOfCustomer = "fazil@gmail.com"
passwordOfCustomer = "faz@1234522"





''' CREATEING  CUSTOMER IN BIGCOMMERCE WITH THE DATA GETTING FROM AEM   '''


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


    #converted string to json 
    json_object = json.loads(res)


    customer_id = json_object['data'][0]['addresses'][0]['customer_id']


    # PRODUCT DETAILS FOR CREATING CART IN BIGCOMMERCE 
    product_id = 482
    quantity = 10
    list_price = 12
    name = 'calender'
    
    customerData = {
          'customer_id':customer_id,
          'product_id':product_id,
          'quantity':quantity,
          'list_price':list_price,
          'name':name
    }

    return customerData



# GET PRODUCT DETAILS THROUGH API FOR CREATEING CART 
def getProductDetails(request):
    print('getting product details')
    return HttpResponse('product details')











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
   
    customerProductData = createCustomerBc(request)


    customerId = customerProductData['customer_id']
    product_id = customerProductData['product_id']
    quantity = customerProductData['quantity']
    list_price = customerProductData['list_price']
    name = customerProductData['name']
    

    channel_id = 1


    payload = {
        "customer_id": customerId,
        "line_items": [
            {
                "quantity": quantity,
                "product_id": product_id,
                "list_price": list_price,
                "name": name
            }
        ],
        "channel_id": channel_id,
        # "currency": {"code": "USD"},
        # "locale": "en-US" 
    }
    
    headers = {"Content-Type": CONTENT_TYPE,"Accept": 'application/json',"X-Auth-Token": XAUTH_TOKEN}

    response = requests.request("POST", url, json=payload, headers=headers)

    cartDetails = response.text
    
    json_object = json.loads(cartDetails)

    cartId = json_object['data']['id']

    return cartId

   



#Creates a Cart,Chekout Redirect URL
def createCartRedirectUrl(request):

    cart_Id = createCartInBc(request)

    print('third function getting cartid',cart_Id)
    
    url = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/carts/{cart_Id}/redirect_urls"

    headers = {"Content-Type": CONTENT_TYPE,"Accept": 'application/json',"X-Auth-Token": XAUTH_TOKEN}

    response = requests.request("POST", url, headers=headers)

    print(response.text)
    
    return HttpResponse(response)


























