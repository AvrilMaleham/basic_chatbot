# basic_chatbot

To view this project locally:

### `git clone git@github.com:AvrilMaleham/basic_chatbot.git`

Clone the app into the directory of your choice.

### `python -m venv venv`

Create a virtual environment (optional but recommended).

### `source venv/bin/activate`

Activate the virtual environment (macOS).

### `pip install -r requirements.txt`

Install dependencies.

Create your own **.env** file, following the **.env-example**

### `python build_index.py`

Create vector store.

### `python test_vectorstore.py`

Verify the retrieval logic and embeddings by printing the top 3 chunks from the docs most relevant to the query.

### `streamlit run app.py`

Runs the app.

Open [http://localhost:8501/docs](http://localhost:8501/docs) to view the UI the browser.
