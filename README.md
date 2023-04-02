## Backend for online store

**Python Project Description:**

An example of a backend system for online store as React App > 
[frontend](https://github.com/6048566/pasv-online-store-front) 

_The project is in progress_



**Technologies and Tools:** 

Python, Django framework, PyCharm, Docker


**Project Description**

A fully functional API backend (database, application logic, and APIs) is built with Django and using Django-Rest-Framework for serving endpoints. 

The application is also Dockerized and uses a practical Postgresql database for secure and fast data storage and retrival.
All the API endpoints are accessible from a browser like Chrome.

The project includes Unit tests for API endpoints and logic. For testing views directly using a request factory, the force_authenticate() method is used.

**Features:**
- Versatile product categories
- Products for each category
- Details for each product
- Create/Read/Update/Delete/Search products
- Add to Cart, Checkout and Finalize order
- Creating and managing customer account

**Getting Started**

1. Start with installing Python. 

2. Clone project. 

3. Create a virtual environment:

```bash
python -m venv env
```

4. Install Django:

```bash
pip install django
```

5. Install the required dependencies:  

```bash
pip install -r requirements.txt
```

6. Create database from models:  

```bash
python3 manage.py makemigrations
```

```bash
python3 manage.py migrate
```

7. Run server:

```bash
python3 manage.py runserver
```

8. Run tests:

```bash
python .\manage.py test
```
