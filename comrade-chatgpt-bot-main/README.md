# Danilevich

### Balance change SQL
```sql
insert into user_balances (user_id, balance, images_generated) VALUES (105013941, 10.0, 0)
```

### Add user to allowed
```bash
curl 'http://localhost:5005/allow' -v --location --data-raw 'user_id=524046168'

curl 'http://localhost:5005/allow' -v --location --data-raw 'user_id=524046168'