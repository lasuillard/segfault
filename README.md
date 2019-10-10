# SegFault
`19 Seoultech Computer Engineering Capstone Project (1), (2)

SegFault is an SNS web service for developers.


## Getting Started
Introductions for setting up development environment for co-workers.

### Prequisites
* Git
* Docker

### Installation
Run following commands on project root directory after extracting git repository.
```
// create and run container
> docker-compose up -d --build

// create superuser for django admin
> docker-compose exec django python manage.py createsuperuser
```

## Development
If you are successfully running containers, you can check the site by below

### Servers
* django: localhost:8000

Type following commands to monitor what server do

```
docker-compose logs -ft --tail 10 django
```

it is useful because emails for user verification will be sent to console. 
### URLs
* Django Admin: /admin
* Browsable API: /api
* Dev-only Echo API: /api/debug/echo

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

// to create multiple instances, use {Model}Factory.create_batch(args, size=n)
```

### Secrets
All secrets will be handled by secret.json, which is not included in repo.<br/>
and also supports environment variables as secret config for PaaS like heroku.

### TODO
Free note here. but just your parts.

* Backend
  * Helping frontend works

* Frontend
  * NOTHING YET
