# addressbook-api-drf

API For simple AddressBook Application built with Python Django + Django Rest Framework + SQLite3.

#### Directions how to run:

1. Create/run the docker container (addressbook-api) 
and then run the DRF server at http://localhost:8888
```
docker-compose up -d
```

2. Run django migrate and run tests
```
make all
```

3. Run tests
```
make test
```

#### Test API using Swagger UI
1. Run the server using 
```
docker-compose up -d
```
2. Swagger UI are available at http://localhost:8888/swagger/
3. You can register a user using `account_users_create` API
4. Then login to get auth_token using `account_token_login_create` API, if the credential is valid you will get the auth_token for authorization 
``` 
//account_token_login_create response 
{
  "auth_token": "5cb401b5ea8316a20c24be01a1d438f981c1eaeb"
}
```
5. Copy the auth_token value then click the **Authorize** Button on the top right and set the access_token value there. Add "Token" prefix before the value
```
Token 5cb401b5ea8316a20c24be01a1d438f981c1eaeb
```

