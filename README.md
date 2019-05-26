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