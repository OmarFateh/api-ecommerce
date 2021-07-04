# API Ecommerce
> An ecommerce API made with django framework and django API rest framework.

## Table of contents
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)
* [TODO](#TODO)

## Technologies
* Python 3.9
* Django 2.2.19
* Django Rest Framework 3.12.2

## Setup
The first thing to do is to clone the repository:  
`$ git clone https://github.com/OmarFateh/api-ecommerce.git`  
Setup project environment with virtualenv and pip.  
`$ virtualenv project-env`  
Activate the virtual environment  
`$ source project-env/Scripts/activate`  
Install all dependencies  
`$ pip install -r requirements.txt`  
Run the server  
`py manage.py runserver`

## Features
* Authentication: Registeration, login, logout, change and reset password.
* Products are displayed based on their categories and child categories and so on.
 * An authenticated user can add product to his a wishlist.
* An authenticated user can purchase a product and add/update/delete a review.
* A user gets a confirmation email after purchasing a product.


## TODO
* Implement Product comparison
