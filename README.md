# Safechain

## Install and run project

pip install -r requirements.txt

## Run this project using

  python manage.py runserver
  
## Apis in this projects are:

  #### User listing apis
       http://localhost:8000/api/v1/users/
  ####  User signup api
       http://localhost:8000/api/v1/user/signup/

  ####  User update delete apis
       http://localhost:8000/api/v1/users/<id>  
       
  #### User profile listing
      http://localhost:8000/api/v1/list_profiles/<id>
  
  #### Show PDF api
      http://localhost:8000/api/v1/show_pdf/<id>    

### Configure database
    export DATABASE_URL=postgresql://safechain_user:@localhost:5432/safechain
    
### Create superuser
    python manage.py createsuperuser    
    
### Run test cases
    python manage.py run test
    
    You may need to give user create permission on database
        alter role safechain_user CREATEDB;
        