# content-management-system

### Systems Analysis and Design Group Project - Summer 2022

#### Instructions to connect the project to postgresql database

1. clone the project

1. install requirements using
`
$ pip install -r requirements.txt
`
1. install postgresql

1. create a database named "Content_Management_db"

1. change the USER and PASSWORD in `setting.py`

1. run the below commands

    `>> python manage.py makemigrations`
    
    `>> python manage.py migrate `
