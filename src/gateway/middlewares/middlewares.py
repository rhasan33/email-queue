import os
import base64
import binascii
import re
from aiohttp import web

WHITE_LIST = {
    "GET": [
        "/"
    ],
    "POST": [],
    "PUT": [],
    "PATCH": [],
    "DELETE": []
}

ALLOWED_APP = [
    "APP_BACKEND"
]

def response_body(msg, status):
    return {
        "success": status,
        "msg": msg
    }

def validate_email(email):
    chk_email = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)
    if chk_email:
        return "True"
    return "False"

def is_float(number):
    return isinstance(number, float)

@web.middleware
async def authentication(request, handler):
    if not request.path in WHITE_LIST[request.method]:
        auth_key = request.headers.get("Authorization", "")
        if not auth_key:
            return web.HTTPBadRequest(text="'Authorization' token is not provided.")
        try:
            decode = base64.b64decode(str(auth_key)).decode("utf-8").split(":")[0]
            if not decode in ALLOWED_APP:
                return web.HTTPUnauthorized(text="Invalid APP")
        except binascii.Error as err:
            return web.HTTPBadRequest(text="Cannot decode auth key. {}".format(err))
    resp = await handler(request)
    return resp
    

@web.middleware
async def validation(request, handler):
    body = await request.json()
    try:
        # delivery_fee validation
        if not is_float(body["delivery_fee"]):
            return web.HTTPUnprocessableEntity(text="key: 'delivery_fee' must be float.")
        
        # other keys
        body_keys = [key for key in ["order_number", "priority", "bcc"] if key not in body]
        if body_keys:
            return web.HTTPUnprocessableEntity(text="key(s): '{}' not provided".format(body_keys))

        # item key
        if not isinstance(body["items"], list):
            return web.HTTPUnprocessableEntity(text="key: 'items' must be a array.")
        for item in body.get("items"):
            item_keys = [key for key in ["name", "price", "discount"] if key not in item]
            if item_keys:
                return web.HTTPUnprocessableEntity(text="key(s): '{}' not provided".format(item_keys))
            if not is_float(item["discount"]) and not is_float(item["price"]):
                return web.HTTPBadRequest("item price and discount is float value.")
        
        # customer key
        customer_keys = [key for key in ["name", "email", "address", "msisdn"] if key not in body["customer"]]
        if customer_keys:
            return web.HTTPUnprocessableEntity(text="key(s): '{}' not provided for customer".format(customer_keys))

        # email validation
        customer_email = body["customer"]["email"]
        if validate_email(customer_email) == "False":
            return web.HTTPBadRequest(text="Customer email is not valid.")
        
        if body["bcc"]:
            invalid_bcc = [bcc for bcc in body["bcc"] if bcc not in validate_email(bcc)]
            if "False" in invalid_bcc:
                return web.HTTPBadRequest(text="bcc email: '{}' is not valid".format(invalid_bcc))
    except KeyError as err:
        return web.HTTPBadRequest(text="key: '{}' is mandatory".format(err))
    resp = await handler(request)
    return resp

@web.middleware
async def response_handler(request, handler):
    resp = await handler(request)
    if resp.status in [406, 401, 404, 400, 422, 409, 405, 201]:
        return web.json_response(response_body(str(resp.text), False), status=resp.status)
    if int(resp.status) == 201:
        return web.json_response(response_body(str(resp.text), True), status=resp.status)
    return resp
