# SegFault
`19 Seoultech Computer Engineering Capstone Project (1), (2)

SegFault is an SNS web service for developers.


## Getting Started
Introductions for setting up development environment for co-workers.

! Make sure that secret files won't be included in repository !

### Prequisites
* Git
* Docker

### Installation
Run following commands on project root directory after extracting git repository.
```
// create and run container
> docker-compose up -d --build

// create superuser for django admin
> docker-compose exec -it daphne python manage.py createsuperuser

// show last 10 real-time logs from django server
> docker-compose logs -ft --tail 10 daphne
```

## Development
If you are successfully running containers, you can check the site by

### Servers
* daphne: localhost:8000

emails will be sent to console for debugging. check it at log/daphne.log

### URLs
* Django Admin: /admin
* Browsable API: /api

### Model Factories for Tests
```
// enter django container (daphne or uwsgi, using uwsgi here)
> docker-compose exec uwsgi bash

// run django shell
# python manage.py shell

// python console
>>> from core.factories import *

// to use factory, call {Model}Factory(). for example:
>>> FragmentFactory()
<Fragment: Fragment 391>

/*
and you can also assign value what you want.
fields not specified will be random or default value.
*/
>>> fragment = FragmentFactory(title='Factory-boy')
>>> print(fragment.title, fragment.content[:30], fragment.tags)
Factory-boy e0kY6Mc3OcWBxdHXw5HkJQUTKsNymi ['qiuK5yAa']
```

### Secrets
All secrets will be handled by secret.json, which is not included in repo.<br/>
and also supports environment variables as secret config for PaaS like heroku.

### TODO
Free note here. but just your parts.

* Backend
  * Write various tests for server application
  * FCM supports

* Frontend
  * NOTHING YET
