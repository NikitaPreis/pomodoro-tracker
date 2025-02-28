from fabric import task


@task
def runserver(
    c, host='0.0.0.0', port='8000',
    env_file='.env'
):
    c.run(f'poetry run uvicorn app.main:app --host {host} --port {port} --reload '
          f'--env-file {env_file}')

@task
def makemigrations(
    c, migration='user_init'
):
    c.run(f'alembic revision --autogenerate -m "{migration}"')

@task
def migrate(c):
    c.run(f'alembic upgrade head')
