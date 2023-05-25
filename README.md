# Dealer and Retailer Management System

A system for collect product and deliver to shop

# Requirements

- Python 3.10
- virtualenv or your favourite Python environment tool

# Get Started

- Read this README
- Checkout the develop branch
- Install Python and create or use a Python Environment with Python Version listed in requirements
- Activate Python3.10 environment
- Install the local requirements

```
1. git clone https://github.com/SabbirHosen/dealer_solution_django.git
2. cd dealer_solution_django/
3. python3.10 -m venv env
    # or you can use any virtualenv tool to make an env
4. source env/bin/activate
5. pip install -r requirements/develop.txt
6. cp .env.example .env
    # edit .env file all varibale as your system (e.g. DB_NAME, DB_USER etc.)
7. python manage.py migrate
8. python manage.py runserver
```


# Branching Model

Push your commits regularly to the new created feature-branch and when you are done with your ticket, please create a
PullRequest.

- feature/Feature-Title
- develop
- release-#.#.#
- hotfix-#.#.#
- main


# Environments

- local: http://127.0.0.1:8000


