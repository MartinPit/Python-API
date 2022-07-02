# Post API

A simple REST API for managing posts.

## Running the app

It's probably best to run the app from a virtual python environment, so we need to crate and activate it:

Linux (Bash):

```bash
cd project_folder
virtualenv -p python3 venv
source venv/bin/activate
```

Windows (CMD):

```CMD
pip install virtualenv
cd project_folder
virtualenv -p python3 venv
.\venv\Scripts\activate
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