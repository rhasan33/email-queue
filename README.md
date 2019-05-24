# Email Queue

## Installation
You need to have docker and docker-compose

## Run

`docker-compose up`

## Endpoint

URL: `http://localhost:8000/send-email`
body: 
```
{
	"email": "rhasan.amiya@gmail.com",
	"subject": "Test subject",
	"body": "Sample body\n try again",
	"priority": "high"
}
```

## Broker Administartor

URL: `http://localhost:8031`

Username: `myuser`

Password: `mypass`