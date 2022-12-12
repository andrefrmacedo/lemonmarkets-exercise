# How to run the project
* `docker-compose up` to get the project up and running
* `docker-compose exec api python -m alembic -c alembic.ini upgrade head` to run database migrations
* Endpoint is available at `http://localhost:8000/orders`

# Assumptions & Decisions
* For this exercise, I assumed that no extra validations needed to be done, other than the ones already present in the pydantic models.  
* I used `alembic` to handle database migrations.  
* I used `SQLAlchemy` to handle database queries.  
* When the API receives a `create_order` request, it opens a transaction, created the order in the database, and sends the request to `place_order` in the stock exchange:
    * If `place_order` is successful, it commits the order created in the database and the API returns a `201` response.
    * if `place_order` is not successful, the transaction is rolled back. The order is not created in the database and the API returns a `500` response.
* For the testing, the `place_order` step gets mocked to replicate making an external call to the stock exchange.
* To keep the code relatively well organised, a `services` module was created, where the business logic operations should live
* The database setup and connection is located inside the `db` module
* A GitHub actions workflow is also present, to run tests

# Possible future improvements
* Add proper logging to all operations
* Add CI/CD configuration for deployments

# Changes if high volume of async updates received
If the system starts receiving a big number of async updates, a message queue can be created. The queue should be FIFO, to guarantee the message order.  
The order updates would be added to the queue, to be processed later, when a consumer is available.  
After the update is processed, the system can send the result back through the socket.  
