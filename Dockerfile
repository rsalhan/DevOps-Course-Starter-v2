FROM python:latest

# UPDATE IMAGE/INSTALL POETRY **************************************************************
RUN apt-get update && pip install --upgrade pip && pip install poetry --no-cache-dir

# COPY APP CODE ****************************************************************************
WORKDIR /app
COPY . .
# COPY poetry.lock pyproject.toml . 

# INSTALL DEPENDENCIES INC. GUNICORN *******************************************************
RUN poetry install --only main 

# EXPOSE PORT ******************************************************************************
ENV WEBAPP_PORT=8000
EXPOSE ${WEBAPP_PORT}

# ENTRYPOINT/CMD ***************************************************************************
ENTRYPOINT ["poetry", "run", "gunicorn", "--bind", "0.0.0.0", "todo_app.app:create_app()"]

# ALSO WORKS
# CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0", "todo_app.app:create_app()"]
# CMD poetry run gunicorn "todo_app.app:create_app()" --bind "0.0.0.0"

#docker run -it --env-file .env -p 8000:8000 rsalhan/todo-app
