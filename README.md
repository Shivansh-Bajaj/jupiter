# jupiter

## Running API Server in Debug Mode:
`$ gunicorn jupiter:__hug_wsgi__ --reload -b 127.0.0.1:8080`

## Running Task Runner:
`$ huey_consumer jupiter.huey`  
Raise error if child review count 0 for parents
