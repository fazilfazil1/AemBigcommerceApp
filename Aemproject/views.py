from django.shortcuts import HttpResponse
import requests
import json


# Store Credentials
STORE_HASH = "b5ajmj9rbq"


# Customer credentials
emailOfCustomer = "tes6611@gmail.com"
passwordOfCustomer = "muhammedfazil123#"



#--------------------------------------------------------------------------------------------------------
# CREATEING CUSTOMER IN BC WITH DUMMY DATA


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

    headers = {"Content-Type": "application/json","X-Auth-Token": "redptv84kmlgfed97l7jroa0mdknfgc"}

    response = requests.request("POST", url, json=payload, headers=headers)
    res = response.text
    print('Customer created in bc',)
    print('Response data type',type(res))

    #converted string to json 
    json_object = json.loads(res)
    customer_id = json_object['data'][0]['addresses'][0]['customer_id']
    print('customer id:',type(customer_id))
    return customer_id




#--------------------------------------------------------------------------------------------------------
#Validate a customer credentials
#If only valid credentials it shows valid "true" otherwise "false"
#Refer https://developer.bigcommerce.com/api-reference/3d731215a3dcb-validate-a-customer-credentials
def validateCustomerBc(request):
    url = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/customers/validate-credentials"

    payload = {
        "email": emailOfCustomer,
        "password": passwordOfCustomer,
        "channel_id": 1
    }

    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": "redptv84kmlgfed97l7jroa0mdknfgc"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    # store the response to variable
    resData = response.text
    print(type(resData))
    print('data',resData)
    return HttpResponse(resData)
    

  



# #CREATE CART IN BIGCOMMERCE 
def createCartInBc(request):
    url = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/carts"

    id = f'{createCustomerBc(request)}'
    print('second function',id)

    payload = {
        "customer_id": 17134,
        "line_items": [
            {
                "quantity": 2,
                "product_id": 481,
                "list_price": 5,
                "name": "calendar"
            }
        ],
        "channel_id": 1,
        # "currency": {"code": "USD"},
        # "locale": "en-US" 
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Auth-Token": "redptv84kmlgfed97l7jroa0mdknfgc"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)

    return HttpResponse(response)



#Creates a Cart redirect URL 
def createCartRedirectUrl(request):
    url = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/carts/{CART_ID}/redirect_urls"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Auth-Token": "redptv84kmlgfed97l7jroa0mdknfgc"
    }

    response = requests.request("POST", url, headers=headers)

    print(response.text)
    
    return HttpResponse('create cart redirect url')









#Create an order in bigcommerce using cart id
def createOrderBc(request):
    url = "https://api.bigcommerce.com/stores/{STORE_HASH}/v3/checkouts/{CART_ID}/orders"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Auth-Token": "redptv84kmlgfed97l7jroa0mdknfgc"
    }

    response = requests.request("POST", url, headers=headers)

    print(response.text)

    return HttpResponse(response)






