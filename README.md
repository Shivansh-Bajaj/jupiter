# jupiter

## Steps:
1. Run API Server in Debug Mode:  
`$ gunicorn jupiter:__hug_wsgi__ --reload -b 127.0.0.1:8080`

2. Run Task Queue:  
`$ huey_consumer jupiter.huey`  
Raise error if child review count 0 for parents
