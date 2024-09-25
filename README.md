# 🏗️ Django Multi-Tenant Cookie Cutter with Sub-Domain Separation

[![License](https://img.shields.io/badge/license-MIT-blue)](https://opensource.org/license/mit/)
[![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue)](https://www.python.org/)


<picture width="500">
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/nawtybean/DjangoMultiTenant/blob/main/static/assets/DjangoMultiTenantWhite.png">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/nawtybean/DjangoMultiTenant/blob/main/static/assets/DjangoMultiTenant.png">
  <img alt="Shows The Logo depending on dark or light mode" src="https://github.com/nawtybean/DjangoMultiTenant/blob/main/static/assets/DjangoMultiTenantWhite.png">
</picture>



## Introduction

🔑 Project Overview
Building scalable, secure multi-tenant applications has never been easier! This cookie cutter project provides a powerful solution to managing multiple tenants using Django Admin, while leveraging Jazzmin for a modern and intuitive interface.

🛠️ Key Features
- Sub-domain based tenant separation so each client gets their own secure, isolated space, ensuring their data stays private and accessible only to them.
- Database-agnostic architecture which Works seamlessly with any database.
- Effortless CRUD operations
- Pre-styled with Jazzmin for a sleek, modern UI without the hassle of designing from scratch.

⚙️ Why Use This?

Juggling tenant isolation and management doesn't have to be a headache. This cookie cutter project simplifies the complexities of multi-tenancy, giving you the ability to focus on growth and innovation without sacrificing security or performance.

🚀 Get Started Fast
1. Fork the repo
2. Clone your fork
3. Create a branch for your changes

💡 Ideal For

- SaaS applications requiring secure client data isolation
- Teams needing a quick, efficient, and scalable solution for multi-tenant platforms


## Techstack

- ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
- ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
- ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
- Bootstrap 5
- HTML
- CSS
- Jazzmin

## Installation and Configuration

Let’s get started - Local development !
====================

Before we get started, it is important to note that this app is a Multi-Tenant app using ID's to seperate the tenants. The app uses subdomains i.e. yourcompany.DjangoMultiTenant.co.za to identify different tenants.

1\. Fork the Repo and Create Virtual Environment
=============================================

*   Fork the repo.

cd to DjangoMultiTenantPublic

*   Build virtual environment for the project

````python
python manage.py -m venv venv
````

this will create a virtual environment, now we need to activate it

On Windows

````
.\venv\bin\activate
````

On Linux

````
source venv/bin/Activate
````

Remember to create a new branch on your repo! Do not use master/main as this will cause issues later on for subsequent pull requests!


2\. Installing Requirements
=====================

After complete forking the repo, creating a venv and activating it, install the requirements.txt

````python
pip install -r requirements.txt
````

3\. Set hosts for local development
===================================
For local development, it is recommended to setup a psuedo domain (as this is a multi tenant app). Open your hosts file and add an entry that looks something like this: (There are a lot or resources online to add entries to your host file for your respective OS ). You can use any domain name you like.

````
127.0.0.1		acme.DjangoMultiTenant.co.za
````

4\. Database
================================

As this is this a cookie cutter project, we are using

![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)


5\. Set the Environment Variables
================================

Create a .env file in the root directory of DjangoMultiTenant, and set the following Variables

````python

# Dev
SECRET_KEY=< Your Secret Key Goes Here>

# Environment
DEVELOPMENT=True/False
````


6\. Starting your DjangoMultiTenant app
================================

The first step is to run migrations

````python
python manage.py migrate
````

Once migrations are successfull, there is a custom command under:


````
└── root
    └── system_management
        └── managment
            └── commands
                └── makesuperuser.py
````
You can double check and change the super user details in here.

Run this command using:

````
python manage.py makesuperuser
````

Then we start the app using the domain you specified

````
python manage.py runserver acme.djangomultitenant.co.za:8000
````

7\. Let’s get started - Deployment  !
=================================

Follow this guide to deloy the app on your own server

[Deploy to your own server](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04)


# Contributor Guide

Interested in contributing? Check out our
[CONTRIBUTING.md](https://github.com/nawtybean/DjangoMultiTenant/blob/main/CONTRIBUTING.md)
to find resources around contributing.

# Resources

- [Jazzmin](https://django-jazzmin.readthedocs.io/) - Welcome to Jazzmin, intended as a drop-in app to jazz up your django admin site, with plenty of things you can easily customise, including a built-in UI customizer.
- [Django](https://www.djangoproject.com/) - The webframework for perfectionists with deadlines.
