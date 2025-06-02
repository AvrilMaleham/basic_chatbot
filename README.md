# basic_chatbot

To view this project locally:

### `git clone git@github.com:AvrilMaleham/basic_chatbot.git`

Clone the app into the directory of your choice.

Create your own **.env** file, following the **.env-example**

Make sure **Docker** is installed locally.

### `docker-compose up --build`

Will build the app as 4 microservices: UI, API, vector store, and a service to build the vector store.

Open [http://localhost:8000/docs](http://localhost:8000/docs) to view the Swagger in the browser.

Open [http://localhost:8501](http://localhost:8501) to view the UI in the browser.

docker compose run --rm dbmate new <table_name>
docker exec -it basic_chatbot-db-1 psql -U postgres -d chatbotdb
