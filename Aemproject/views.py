from django.shortcuts import HttpResponse
from urllib.parse import urlparse, parse_qs

import requests
import json
import os


from django.shortcuts import render

from django.shortcuts import redirect


# STORE CREDENTIALS 
STORE_HASH = os.environ.get('STORE_HASH')
XAUTH_TOKEN = os.environ.get('XAUTH_TOKEN')
CONTENT_TYPE = os.environ.get('CONTENT_TYPE')

# Headers
headers = {"Content-Type":  CONTENT_TYPE,"X-Auth-Token":XAUTH_TOKEN}



# Aem frontend page
def enrollcourse(request):
    return render(request,'aemfront.html')


     
def enroll(request):
    if(request.method != "GET"):
        return "HO HTTP mehtod not allowed"
    else:
        # get the email,password,course sku or id from request    
        email = request.GET.get('email')
        password = request.GET.get('pass')
        productsku = request.GET.get('productsku')
        fname = request.GET.get('fname')
        lname = request.GET.get('lname')
          


        # login or register the customer and get the customer id
        customer_id = getBcCustomerId(email,password,fname,lname)
        print('customer id is000222',customer_id)
        

        #getting product id useing product sku
        productId = getProductIdUsingSku(productsku)
        
        # create cart for the customer 
        cartId = createCartForCustomerId(customer_id,productId)


        # redirect to bigcommerce checkout page with the above created cart
        redirectUrl = createCartRedirectUrl(cartId)

        return redirect(redirectUrl['checkout_url'])



# ##################################################################


def getBcCustomerId(email,password,firstname,lastname):
    
    url = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/customers"

    querystring = {"email:in":email}

    response = requests.request("GET", url, headers=headers, params=querystring)

    res = response.text

    json_object = json.loads(res)

     
    data = json_object['data']


    # if the data does not exists then create customer else validate the customer

    if data == []:
        print('no customer id found')
        #Createing new customer if data is not found
        return createNewCustomerInBc(email,password,firstname,lastname)
    else:
        if validateCustomerInBc(email,password):
            return json_object['data'][0]['id']
        else:
            return None



def validateCustomerInBc(email,password):
    url = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/customers/validate-credentials"

    payload = {
        "email": email,
        "password": password,
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    res = response.text
   
    json_object = json.loads(res)


    isValid = json_object['is_valid']

    return isValid
    






# Register customer in bigcommerce with email and password getting from aem 
# Function Prams : customer details in request email,pass,productsku
# Function Returns : the response as customer created or customer already exists
# product id,quantity,listprice,customerid,name passing to cartcreate function for createing cart

def createNewCustomerInBc(email,password,firstname,lastname):
    
    url = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/customers"
    payload = [
        {
            "email": email,
            "first_name": firstname,
            "last_name": lastname,
            "authentication": {
                "force_password_reset": False,
                "new_password": password
            },
        }
    ]
    response = requests.request("POST", url, json=payload, headers=headers)
    res = response.text
    json_object = json.loads(res)  #converted string to json 
    print('response data555',type(json_object))
    customer_id = json_object['data'][0]['id'] #getting customer id
    print(customer_id,type(customer_id))
    return customer_id
# ##################################################################







# finding product id using product sku 
# return: product id to createcartinbc(request) for create cart

def getProductIdUsingSku(productsku):
    url = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/catalog/products"

    payload = {"sku":productsku}

    response = requests.request("GET", url, headers=headers, params=payload)

    res = response.text

    json_object = json.loads(res)

    product_id = json_object['data'][0]['id']

    print('product id is:',product_id)

    return product_id







#CREATE CART IN BIGCOMMERCE 
def createCartForCustomerId(customer_id,productId):
  
    url = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/carts"

    payload = {
        "customer_id": customer_id,
        "line_items": [
            {
                "quantity": 1,
                "product_id": productId
            }
        ],
    }
  
    response = requests.request("POST", url, json=payload, headers=headers)
    cartDetails = response.text
    json_object = json.loads(cartDetails)
    cartId = json_object['data']['id']
    print('cart created',cartId)
    return  cartId

















#https://developer.bigcommerce.com/api-reference/ffd397374d154-add-cart-line-items
#ADD LINE ITEMS TO THE CART
# ADD PRODUCT TO THE CART CREATED
def addProductToCart(cartId,productSku):   
    productId = getProductIdUsingSku(productSku)
    url = f"https://api.bigcommerce.com/stores/b5ajmj9rbq/v3/carts/{cartId}/items"
    payload = {
        "line_items": [
            {
                "quantity": 1,
                "product_id": productId,
            }
        ],
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    res = response.text
    print('the response is:',res)
    return cartId








#Creates a Cart,Chekout Redirect URL
def createCartRedirectUrl(cartId):

    url = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/carts/{cartId}/redirect_urls"
    
    response = requests.request("POST", url, headers=headers)
    
    res = response.text
    
    print('the response data 3',res)
    
    json_object = json.loads(res)     # Converting string to json
    
    cart_url = json_object['data']['cart_url']
    
    checkout_url = json_object['data']['checkout_url']
    
    # emdedchekout_url = json_object['data']['embedded_checkout_url']
    
    redirectUrl = {'cart_url':cart_url,'checkout_url':checkout_url}
    
    print(redirectUrl)
    
    # print('cart url',cart_url)
    # print('checkout url',checkout_url)
    # print('emdedchekout url',emdedchekout_url)




    return redirectUrl












    














        
