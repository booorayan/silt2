# REST API 

### 1. Python service
Below is script.py which when running prints Hello Hello to the console every minute unless interrupted by pressing a key on the keyboard

    from time import sleep
    
    try:
        while True:
            print("Hello Hello")
            sleep(60)
    except KeyboardInterrupt as e:
        logging.info("Stopping...")
    
To run the above script as a python service edit the /etc/systemd/system/hello.service file

Run `sudo nano /etc/systemd/system/hello.service` and edit the file as below:

    [Unit]
    Description=Script for greeting 
    After=multi-user.target

    [Service]
    Type=simple
    ExecStart=/usr/bin/python /home/ubuntu/script.py
    
    [Install]
    Wantedby=multi-user.target
    
Activate the service with the following commands:

`sudo chmod 644 /etc/systemd/system/hello.service`

`chmod +x /home/ubuntu/script.py`

`sudo systemctl daemon-reload`

`sudo systemctl enable hello.service`

`sudo systemctl start hello.service`

### 2. DB Design
#### Customer
Table stores information about a customer(s) such as their name, email, code and phone number.
Table fields:
- ID: Unique identifier for the customer.
- Name: Name of customer
- Email: Customer email address
- Phone_Number: Customer phone number

#### Order
Table stores information about an order such as the item, customer, amount and time. Table fields:
- ID: Unique identifier for the order
- Customer: Name/id of customer who placed the order
- Item: Particular item(s) ordered by customer
- Amount: Price of the order

The Customer field in the Order table is a foreign key with the parent table being the Customer table. It creates a relationship between the Customer and Order tables where each order is associated with a particular customer.

### 3. Authentication and Authorization
Keycloak, an open-source platform, was employed to handle authentication and authorization with OpenID Connect. One can install it manually or run it on docker. A sample docker-compose file is available in the keycloak directory to help with running keycloak on docker.

On the keycloak server, create a realm and then create a client. Provide the following details to create a client:

    client_id: 'test'
    redirect uri: 'http://localhost:8000/oidc/callback/'

Create users on keycloak that will be used to login to the django app

To connect the django app to Keycloak, `mozilla-django-oidc` library was used. To install it in the project, run: `pip install mozilla-django-oidc`

Then add the following configs and variables in settings.py file:

    AUTHENTICATION_BACKENDS = (
    'mozilla_django_oidc.auth.OIDCAuthenticationBackend',
    )

    OIDC_RP_SIGN_ALGO=
    OIDC_OP_JWKS_ENDPOINT=
    OIDC_RP_CLIENT_ID=
    OIDC_RP_CLIENT_SECRET= 
    OIDC_OP_AUTHORIZATION_ENDPOINT=
    OIDC_OP_TOKEN_ENDPOINT=
    OIDC_OP_USER_ENDPOINT=
    OIDC_CALLBACK_PUBLIC_URI=


The variables above can be retrieved from realm settings in the Keycloak admin console.

### 4. Unit Tests & CI/CD Pipeline
Unit tests are defined in the app's tests.py file. The tests cover three cases: 
- when a customer is created
- when an order is created
- whether an sms alert is sent when an order is added

The `coverage` library was used for coverage checking during testing. To install it run `pip install coverage`

Run tests with coverage checking using the following command: `coverage run manage.py test`

The CI/CD pipeline is implemented using Github Actions. The pipeline file is located in the .github/workflows directory

The pipeline has three jobs: `test, build and deploy`

The `test` job runs the unit tests. The `build` job builds the docker image and pushes it to Docker Hub. The `deploy` job deploys the docker image on an EC2 instance provisioned on AWS.

The EC2 instance ip is 44.202.134.252. Test the endpoint: `curl -v http://44.202.134.252:8000/api/customers/`. You should get a `403 Forbidden` response

### 6. Test
To test the application locally, ensure you have the following:

- keycloak server(installed or docker)
- keycloak database(postgres/mysql)

Clone the repo, install project dependencies and run the server. 

API endpoints to test are: 

    http://localhost:8000/api/customers
    http://localhost:8000/api/customers/<int:pk>
    http://localhost:8000/api/orders
    http://localhost:8000/api/orders/<int:pk>

You should receive a `403 Forbidden` Response since the requests have not been authenticated.

To authenticate, access the url `http://localhost:8000/api/login` and login by providing the credentials of users created in keycloak

The keycloak server will handle the authentication and you should be able to access the resources at the api endpoints above. 

You can also run the app with docker-compose. To run docker-compose make the following changes to the settings.py file:

    DATABASES = {
     "default": {
         "ENGINE": 'django.db.backends.postgresql_psycopg2',
         "NAME": os.environ.get('PG_DB', 'postgres'),
         "USER": os.environ.get('PG_USER', 'postgres'),
         "PASSWORD": os.environ.get('PG_PASSWORD', 'postgres'),
         "HOST": os.environ.get('PG_HOST', 'localhost'),
         "PORT": os.environ.get('PG_PORT', '5432'),
         # "CONN_MAX_AGE": 60 * 5,
        },
     }
    
    
    CACHES = {
     'default': {
         'BACKEND': 'django_redis.cache.RedisCache',
         'LOCATION': 'redis://redis:6379/',
         'OPTIONS': {
             'CLIENT_CLASS': 'django_redis.client.DefaultClient'
             },
         }
     }
    
    
To start the app run, `docker-compose up -d`