from fabric import task


@task
def runserver(
    c, host='0.0.0.0', port='8000',
    env_file='.local.env'
):
    c.run(f'poetry run uvicorn main:app --host {host} --port {port} --reload '
          f'--env-file {env_file}')

@task
def make_migrations(
    c, migration='user_init'
):
    c.run(f'alembic revision --autogenerate -m "{migration}"')

@task
def migrate(c):
    c.run(f'alembic upgrade head')
