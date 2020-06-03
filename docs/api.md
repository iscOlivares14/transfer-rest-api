## Transfer Service API

REST API that can perform these functions:

- Create a user with a phone number and name
- Retrieve a user
- Retrieve all users
- Create a transaction with amount, currency, the user who sent it and the user who received it
- Retrieve a users transactions
- Retrieve a feed of all transactions


## API Definition
GET a single user
/users/<id>

### Error Responses

- No user with that ID - Http Status 404

### Successful response

```
{
    "id": 1,
    "phone_number": "+19344367546",
    "name": "Dave Simpson"
}
```
