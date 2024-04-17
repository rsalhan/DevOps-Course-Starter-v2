# BASE IMAGE
FROM python:3.11.3 as base

# UPDATE IMAGE/UPGRADE PIP/INSTALL POETRY
RUN apt-get update && pip install --upgrade pip && pip install poetry --no-cache-dir

# COPY APP CODE
WORKDIR /app
COPY . .

# INSTALL DEPENDENCIES INC. GUNICORN
RUN poetry install --only main 

# PROD CONTAINER==========================================================================
FROM base as production

# PROD - EXPOSE PORT 
ENV WEBAPP_PORT=8000
EXPOSE ${WEBAPP_PORT}

# PROD - ENTRYPOINT/CMD
ENTRYPOINT ["poetry", "run", "gunicorn", "--bind", "0.0.0.0", "todo_app.app:create_app()"]

# ALSO WORKS
# CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0", "todo_app.app:create_app()"]
# CMD poetry run gunicorn "todo_app.app:create_app()" --bind "0.0.0.0"


# DEV CONTAINER===========================================================================
FROM base as development

# DEV - EXPOSE PORT 
ENV WEBAPP_PORT=5000
EXPOSE ${WEBAPP_PORT}

# DEV - ENTRYPOINT/CMD
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]

# TEST CONTAINER==========================================================================
FROM base as test

# TEST - ENTRYPOINT/CMD
ENTRYPOINT ["poetry", "run", "pytest"]