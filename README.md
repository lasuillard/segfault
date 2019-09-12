# SegFault
`19 Seoultech Computer Engineering Capstone Project (1), (2)

SegFault is an SNS web service for developers.


## Getting Started
Introductions for setting up development environment for co-workers.

Make sure that secret files won't be included in repository.

### Prequisites
* Git
* Docker

### Installation
Run following commands on project root directory after extracting git repository.
```
# create and run container
> docker-compose up -d --build

# create superuser for django admin
> docker container ls 
> docker exec -it <container> python manage.py createsuperuser

# show all logs from django server
> docker-compose logs -ft server
```

## Development
If you are successfully running containers, you can check the site by

### Servers
* uWSGI: localhost:8000
* daphne: localhost:8443
* Nginx: localhost:80 (or just localhost)

for development, i recommend using just Nginx gateway.

### URLs
* Django Admin: /admin
* Browsable API: /api

### TODO
Free note here. but just your parts.

* Backend
  * Handle secrets in separated file: secret.json, and automate it.
  * Syncrhonize dev database via remotely or dumps.

* Frontend
  *
