# Post API

A simple REST API for managing posts.

## Running the app

It's probably best to run the app from a virtual python environment, so we need to crate, activate it and set the location of the flask app:

Linux (Bash):

```bash
virtualenv -p python3 venv
source venv/bin/activate
export FLASK_APP=app/app
```

Windows (CMD):

```CMD
pip install virtualenv
virtualenv -p python3 venv
.\venv\Scripts\activate
set FLASK_APP=app/app
```

After that, we need to install all the dependencies necessary for the app to run:

```bash
pip install -r requirements.txt
```

Next, we initialize the database:

```bash
python -m flask initdb
```

Finally, we run the app:

```bash
python -m flask run
```