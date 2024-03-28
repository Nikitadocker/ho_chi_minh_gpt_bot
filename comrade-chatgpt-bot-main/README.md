# Danilevich



### Related tasks
- https://github.com/liquibase/liquibase/issues/5706

### TODO
- [ ] fix all versing before v6 with logging.info() and logging.error() - must be logger.info() and logger.error()
- [ ] update asyncio.sleep(5) to asyncio.sleep(1) in all places (in older versions)
- [ ] make sure include only necessary changes per PR (don't change formatting)

### Balance change SQL
```sql
insert into user_balances (user_id, balance, images_generated) VALUES (105013941, 10.0, 0)
```

### Add user to allowed
```bash
curl 'http://localhost:5005/allow' -v --location --data-raw 'user_id=6969'