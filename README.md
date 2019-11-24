# github-repo-aggregator
Collects repositories from GitHub

## Requirements
- docker
- docker-compose
- httpie

## Configuration
First, you need to initialize a database:
```
make initdb
```
Run application:
```
make dev
```

## Usage
Store repositories of a given author from GitHub to the database:
```python
http post http://localhost:8000/api/v1/repositories/ username=<username>
```
List all repositories from the database:
```python
http http://localhost:8000/api/v1/repositories/
```
Get repository by id:
```python
http http://localhost:8000/api/v1/repositories/<id>/
```

## Example
```json
$ http http://localhost:8000/api/v1/repositories/1/
HTTP/1.1 200 OK
Content-Length: 200
Content-Type: application/json
Date: Sun, 24 Nov 2019 16:49:07 GMT
Server: WSGIServer/0.2 CPython/3.8.0
X-Frame-Options: SAMEORIGIN

{
    "created_at": "2019-11-14T18:40:22Z",
    "description": "Let's Build A Web Server",
    "html_url": "https://github.com/sofiy/lsbaws",
    "name": "lsbaws",
    "private": false,
    "username": "sofiy",
    "watchers": 0
}
```
