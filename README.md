# SegFault
`19 Seoultech Computer Engineering Capstone Project (1), (2)

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
> docker container ls 
> docker exec -it <container_id or container_name> python manage.py createsuperuser

// show all logs from django server
> docker-compose logs -ft server
```
