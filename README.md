# SF_Project_Consultation
SkillFactory PromoIT learning project

## Starting 

### Backend starting:  
cd backend  
python -m venv venv  
.\venv\Scripts\activate  
pip install -r requirements.txt  
python manage.py runserver

## Testing
run command:  
python manage.py test  

## Accounts for testing: 
Password for every login = username + 'psw'  
For example, "client1"/"client1psw"  

### Superuser
admin (password: admin)  

### Clients  
client1  
client2  
  
### Specialists
spec1  
spec2  
  
### Admins 
admin1
admin2

### Admin  
admin
password: admin

## Swagger  
OpenAPI scheme can be found on:  
http://localhost:8000/swagger  

## Superadmin  
http://localhost:8000/admin/  

## New users
New users can be created from  
http://localhost:8000/admin/  
