# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Trello: obtain API key + token

Create Trello account - https://trello.com/signup

Generate API key and token - https://trello.com/power-ups/admin/

Select 'New' button which will take you to the following URL - https://trello.com/power-ups/admin/new

Populate the on-screen form with details, please note Iframe connector URL is not required for API/Token access.

Add your newly acquired API key and token variables to `.env` file.

Add the requests library to your list of poetry dependencies in pyproject.toml by running ## Trello: obtain API key + token.

Also add your board ID and list IDs (for ToDo, Doing + Done) to the `.env` file.

## Unit Tests

Please familiarise yourself with `view_model.py` before reviewing contents of `test_view_model.py`.


## Integration Tests

Please also review `app.py` as well as `test_app.py` which will pull your test environment variables from `env.test.py`.


## Executing Unit/Integration Test

Please execute `poetry run pytest` from a terminal ensuring you at the correct path/level.


## Run Ansible Playbook

Navigate to relevant folder on the the controller and run `ansible-playbook ansible-playbook.yml -i ansible-inventory`.


## Start the App

If all the previous Ansible tasks ran successfully, you should be able to manually start up the app and visit the site in your browser:

* Connect to the host/managed node
* Navigate to the project folder by running cd /opt/todoapp
* Run `poetry run flask run --host 0.0.0.0`
* Open up a browser on your own computer and navigate to http://host.ip.address:5000/ (e.g. http://3.77.132.88:5000/)


## View Logs for Systemd Task

To view the logs for your systemd task, SSH onto the managed node and run `journalctl -u todoapp`.


## Build Dev/Prod Containers

The following commands can be run to build Production and Development containers for the ToDo App:

* `docker build --target production --tag rsalhan/todo-app:prod .`
* `docker build --target development --tag rsalhan/todo-app:dev .`


## Run Dev/Prod Containers

Once built, the containers can be run using the following:

* `docker run -it --env-file .env -p 8000:8000 rsalhan/todo-app:prod`
* `docker run -it --env-file ./.env -p 5000:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app rsalhan/todo-app:dev`


## Accessing Docker/Containerised ToDo App

Depending on whether you wish to access the Prod or Dev version, navigate to the relevant URL below on your local machine:

* Production URL: http://localhost:8000/
* Development URL: http://127.0.0.1:5000/
