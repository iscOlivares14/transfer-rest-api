## Contents

- [About the project](#About-the-project)
  - [Build with](#Build-with)
- [Getting Started](#Getting-Started)
  - [Prerequisites](#Prerequisites)
  - [Installation](#Installation)
- [Usage](#Usage)
- [Roadmap](#Roadmap)
- [Contributing](#Contributing)
  - [Development](#Development)
- [Contact](#Contact)
- [Acknowledgments](#Acknowledgments)

## About the project

This repository was part of an interview and consists on creating a money transfer service where users can :bowtie:

- create user accounts
- retrieve user details
- retrieve a users list
- add funds to an account
- send money to other users
- retrieve user transactions
- retrieve a feed of all transactions

functionalities are exposed via REST API using JSON, authentication is enabled for most of the endpoints using JWT (Flask-JWT) and implementing REST using MethodView similar to Django class-based views.

Tests are included in unittest format but run using pytest.

### Build with

Some tools used here:

- Make
- Docker
- Docker-compose
- Flask
  - Flask-JWT
  - Flask-Migrate
  - Flask-SQLAlchemy
- nginx
- uWSGI
- Postgres (dockerized)

## Getting Started

Now you will see what you need and how to run the project.

### Prerequisites

As everything is containerized the only requirement before run it is `Docker` the base images used for this are `ubuntu` based so `python` is covered there.

### Installation

Commands are provided by `Make` in order to facilitate writing them.

* Clone the repository to your local.

* Build the app image and create containers.
```bash
> make up
```

* Apply migrations.
```bash
> make run_migrations
```

* Visit [this link](http://localhost:5000/api/v1/test) and you should see "Project setup successfully!" in your default browser

* Run your tests.
```bash
> make up
```

NOTES

To connect to the `flask shell` you must set
- export LC_ALL=C.UTF-8
- export LANG=C.UTF-8
- export FLASK_APP='app:create_app("development")'

## Usage

To see a full description of the API visit [this doc](docs/api.md)

## Roadmap

The app is not fully completed there is some work to do, the following list shows it.

* Return balance as part of client details JSON response
* To avoid duplicated validations on the views moving them as validators in the model User
* Currencies could be changed to a model for keeping them inside DB and make them more manageable
* Each account should define its currency at creation time to be considered when transfers.
* Make it transactional
* Add a UUID to match related rows easily

## Contributing
-

### Development
-

## Contact
-

## Acknowledgments
-
