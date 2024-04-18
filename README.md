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

Please note: the loop back address referenced in the above URL is another way of routing traffic to loop back to the local host.


## Build/Run Docker Test Image + Unit/Integration Tests

The following commands can be used to build and run the Docker Test Image whilst also running the Unit and Integration tests:

* `docker build --target test --tag my-test-image .`
* `docker run my-test-image`


## Deployment - Step 1: Put Container Image on Docker Hub registry

Authenticate with Azure CLI:

* `az login --use-device-code`

Log into DockerHub locally and then authenticate using Docker username/password when prompted:

* `docker login`

Build the image:

* `docker build --target production --tag <DH_user_name>/<image_name>:<tag> docker login .`

Push the image whilst substituting in your own personal values:

* `docker push <DH_user_name>/<image_name>:<tag>`


## Deployment - Step 2: Create a Web App

The following commands will be need to be completed in sequence...

Create an App Service Plan:

* `az appservice plan create --resource-group <resource_group_name> -n <appservice_plan_name> --sku B1 --is-linux`

Create the Web App:

* `az webapp create --resource-group <resource_group_name> --plan <appservice_plan_name> --name <webapp_name> --deployment-container-image-name docker.io/<dockerhub_username>/<container-image-name>:latest`

Note: your <webapp_name> needs to be globally unique, and will form part of the URL of your deployed app: https://<webapp_name>.azurewebsites.net.


## Deployment - Step 3: Set up environment variables

Environment variables also need to be added, this can be done manually in Azure Portal or via CLI.

Portal - navigate to the following sections and add all the env variables:

* Settings -> Configuration
* Add all environment variables as "New application setting"

CLI - enter them individually using the following command, ensuring you pass across your RG name and Web App name, the following are a few examples:
* `az webapp config appsettings set -g <resource_group_name> -n <webapp_name> --settings FLASK_APP=todo_app/app.`
* `az webapp config appsettings set -g <resource_group_name> -n <webapp_name> --settings FLASK_DEBUG=true`
* `az webapp config appsettings set -g <resource_group_name> -n <webapp_name> --settings SECRET_KEY=secret-key`
* `az webapp config appsettings set -g <resource_group_name> -n <webapp_name> --settings BASE_URL=https://api.trello.com/1/`

Please note: there is also a third option you can pass in a JSON file containing all variables by using --settings @foo.json


## Deployment - Step 4: Confirm the live site works

* Browse to http://<webapp_name>.azurewebsites.net/ and confirm no functionality has been lost.
* See if the image has successfully been pulled from the Deployment Center’s “Logs” tab
* See if the application “Log Stream” (not the “Logs”) shows any hints on what might be going wrong


## Deployment - Step 5: Update the container

Find your webhook URL:
* This can located under Deployment Center on the app service’s page in the Azure portal.

Test your webhook:
* Take the webhook provided by the previous step, add in a backslash to escape the $, and run: curl -dH -X POST "`<webhook>`"
* eg: `curl -dH -X POST "https://\$<deployment_username>:<deployment_password>@<webapp_name>.scm.azurewebsites.net/docker/hook"`
* This should return a link to a log-stream relating to the re-pulling of the image and restarting the app.

Please note: The webhook URL contains a dollar sign which should be escaped (`\$`) to prevent it being interpreted as an attempt to reference an environment variable.

## Accessing Deployed App

The deployed app can be accessed via the following URL:
* https://RS-M8-ToDoApp.azurewebsites.net/


## GitHub Actions

Your GitHub Actions workflow now has a deployment section, which:
* Pushes a production image to Docker Hub
* Doesn’t reveal any secret values
* Only deploys if your tests pass and can be configured to only run for updates to the main branch
* Releases the latest image to Azure

Whenever your application is committed, it will also be tested, to view the results navigate to:

* https://github.com/GitHubAccount/repo/actions

Please substitute in your own GitHub account and repository name into the above URL to access the relevant GitHub Actions section.


## MongoDB - create database

Create an Azure CosmosDB database to go alongside our existing App Service, this can be done via the Portal or using CLI.

Portal
* New -> CosmosDB Database
* Select “Azure Cosmos DB API for MongoDB”
* Choose “Serverless” for Capacity mode
* You can also configure secure firewall connections, but for now you should permit access from “All Networks” to enable easier testing of the integration with the app.

CLI
* Create new CosmosDB account: `az cosmosdb create --name <cosmos_account_name> --resource-group <resource_group_name> --kind MongoDB --capabilities EnableServerless --server-version 3.6`
* Create new MongoDB database under that account: `az cosmosdb mongodb database create --account-name <cosmos_account_name> --name <database_name> --resource-group <resource_group_name>`

Please note: it may take a few mins for your cluster to spin up, you'll need to wait for it to finish deploying.


## MongoDB - install PyMongo

Python support for MongoDB comes in the form of PyMongo - this project dependency can be added via the below:

* `poetry add pymongo`

Once installed you should be able to interact with MongoDB from the Python shell in VS Code:
* Open the VS Code terminal.
* Type `poetry run python` to open the Python shell
* Type `import pymongo`

If at this point you do not receive an error then you have successfully installed PyMongo.

## MongoDB - connecting to CosmosDB

First copy the PRIMARY CONNECTION STRING for your CosmosDB cluster, available under Settings -> Connection String from your CosmosDB account page in the Azure portal, or via the CLI: 
* `az cosmosdb keys list -n <cosmos_account_name> -g <resource_group_name> --type connection-strings`

## MongoDB - replacing Trello

You should be able to copy the data access code you’ve written for Trello and rewrite it to target MongoDB instead. You will need an environment variable for the connection string, and we suggest adding one for the database name as well.

View model tests should not need any changes, but here is some advice on updating the integration.

## MongoDB - Integration tests

You will need to update how the integration tests are providing fake data, this can be done using the mongomock library:

* `poetry add mongomock`

You can use it to provide a fake Mongo database. First, set the connection string environment variable in .env.test equal to mongodb://fakemongo.com. Next, update your test setup as follows:

    import mongomock

    @pytest.fixture
    def client():
        file_path = find_dotenv('.env.test')
        load_dotenv(file_path, override=True)

        with mongomock.patch(servers=(('fakemongo.com', 27017),)):
            test_app = app.create_app()
            with test_app.test_client() as client:
                yield client

Your integration test can now use `pymongo.MongoClient` to connect and insert dummy data as if it were interacting with a real database. Delete any code related to mocking `requests.get`.

## MongoDB - update CI/CD

Once you’ve finished the code changes you’ll need to check your CI/CD pipeline and deployed application both work. 

At the very least, you need to `provide your App Service with any new environment variables` required to connect to CosmosDB.

## MongoDB - final checks

Finally please ensure:
* your local build still works
* CI/CD pipeline is still showing as green in GitHub Actions
* the Prod deployed Azuer environment is still avaliable

