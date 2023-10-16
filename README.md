# devgrid-challenge

### My Interpretation of the problem

Create an API that do the following:

POST - Receive an ID that will be used to monitor the progress of the request (async) later. This request should trigger a series of async calls to the external API to store data from all the cities in the given cities ID list.

GET - Get the same ID from before and return the progress of all the requests triggered in the previous request.

### Software Architecture & Design

Given that each request should trigger many requests to the external API, respecting the 60 cities per minute limit, my idea was to use a message system (kafka) to control that flow and prevent firing a lot of requests at the same time. The data will then be persisted in MySQL. I also used docker compose in order to manage all these services together.

### External API comments

After some study, I discovered some information about the extenal API:

- It is mentioned to use the `Call for several city IDs` endpoint. However, the [link](https://openweathermap.org/current#severalid) attached doesn't exist anymore (you can see that the anchor does not work). The endpoint is also not mentioned anywhere in the docs. I was only able to find it in a [stackoverflow answer](https://stackoverflow.com/a/47898838/10659353).
- This endpoint accepts at most 20 cities id per request.

### Producer architecture

The producer is a simple API built with fastAPI that will have the two mentioned endpoints. The first one will batch cities into lists of 20 cities and send to the queue. The second one will gather the data from the database and return both the data and the progress.

### Consumer architecture

The consumer will listen for the message batches and process them in such a way that they keep the ratio of 1 city per second, sleeping when needed and maximizing efficiency. After requesting data, it will store into database.

### SQL Alchemy

The project uses SQL Alchemy ORM. It is great to make queries in a standardized manner accross the app. It also helps to build tables whenever docker compose goes up. It should be mentioned that for bigger projects, migration tools, such as alembic, are needed.

### Dependency injection

One very relevant pattern that is being used in the code is dependency injection. It is important to isolate external APIs and Database calls from the code such that it is possible to inject fake services for testing, for example.

### Secret managment

Since this is a demo project, secret managment was not perfectly adressed, two `config.env.yml` files containing api keys and connection URIs are set. I'm committing the files to the repository in order to keep the schema for someone to reproduce without the need of communication with me, but in a real project this files should be keep apart from the repository.

### Testing

Tests (unit) are separated between producer tests and consumer tests.

#### Producer tests:

Consists of testing each endpoint.

- GET - Given that the mock service returns a specific data, ensures that the endpoint will return that data in json.
- POST - Given that function was called, ensure that the messages were sent.

#### Consumer tests

- Tests if it subscribes to the queue
- Tests if calls the api and saves the data in the database
- Test if it respects the 1 requests per second ratio of the external API.

### Running the code

First, configure your Open Weather API key inside `consumer/config.default.yml`. I provided the one I used (again, this is only for convenience, not a good practice).

After that it is just as simple as calling `docker-compose up`. Then, you can send the requests in localhost:8000:

- POST localhost:8000/collect/ (sending id in the body as the id to verify the request later)
- GET localhost:8000/get/?id=`<id>` (sending ID in query params)

It is also possible to connect to kafka on port 9094 and to mysql on port 3306.

Logs will be generated about requests, by the producer, and message processing, by the consumer.

### Running the tests

To run the tests, you must have python3 installed. To test each service, do:

```
cd <consumer/producer>
python3 -m pip install -r requirements.txt
python3 -m pytest
```

Then, repeat the process to the other.

### Final Considerations

This was a very fun project to develop and I think that the architecture is pretty solid and clean. Please feel free to reach me out if you have any questions, I'd love to discuss further.
