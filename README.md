# Project to learn pyramid and mongodb


## Running the application

### In order to run the application follow the steps below

* Create a mongo database and set the uri on the file development.ini
    ```ini
    mongo_uri = mongodb://<usr>:<pwd>@<host>:<port>/<database>
    ```
* Setup the application with pip
    ```sh
    pip install -e .
    ```
* Run the pyramid server 
    ```sh
    pserve development.ini
    ```
