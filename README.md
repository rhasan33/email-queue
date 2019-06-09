# Email Queue

## Installation
You need to have docker and docker-compose

1. rename `docker-compose.yml.sample` to `docker-compose.yml`
2. change value for the following envs:
	- FROM_EMAIL= your email address
	- EMAIL_PASS= your email password
	- SMTP_USER=your-smtp-user
	- SMTP_PASS=your-email-password
	- SMTP_HOST=smtp.host.com
	- SMTP_PORT= your email host's port
	- FROM_NAME= your name
3. remember to remove all `.pkl` file from `src/worker/fonts` folder if needed to run on different environment.

## Run

`docker-compose up`

## Endpoint

URL: `http://localhost:8000/api/send-invoice`
body: 
```
{
	"customer": {
		"name": "Rakib Hasan Amiya",
		"email": "rakib@telenorhealth.com",
		"address": "56, North Dhanmondi, Kalabagan, Dhaka - 1205",
		"msisdn": "+8801701227013"
	},
	"items": [
		{
            "name": "Diabeties Medicine",
            "price": 6522.50,
            "discount": 200.0
        },
        {
            "name": "Diabetes Machine",
            "price": 1200.00,
            "discount": 1200.00
        }
	],
	"delivery_fee": 60.0,
	"order_number": "Order-2781-2019",
	"priority": "high"
}
```
response: 
```
{
    "msg": "successfully queued"
}
```

## Broker Administartor

URL: `http://localhost:8031`

Username: `myuser`

Password: `mypass`

## ToDo

- Need to add more error handlers 
- Write tests