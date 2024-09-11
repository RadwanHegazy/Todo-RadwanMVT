# This is a Very Simple ORM for managing the databases without writing an SQL Query.




### getting started with the ORM

**This ORM only supported sqlite3 and mysql**

run on your cmd or terminal
```
git clone https://github.com/RadwanHegazy/RadwanORM
```
```
cd RadwanORM
```
```
pip install -r requirments.txt
```

**create a python file and open it on your editor and follow the instructions for test the orm**

## For Connect With Sqlite3
```python
from orm import RadwanORM, Fields

# initalized the sqlite3 db

# initalized the configuration of the db
config = {
    "NAME" : "my_db.sqlite3" # my database name
}

db = RadwanORM()
db = db.connect(
    dbtype='sqlite3', # set the db type
    config=config # set the db configuration
)
```

## For Connect With MySql
### Note :
For connect with mysql you should install the mysql in your device -- [Watch for install MySQl in windows 10](https://www.youtube.com/watch?v=BxdSUGBs0gM)

Then change the dbtype to mysql and change the config dict , then code must be like :
```python
from orm import RadwanORM, Fields

# initalized the mysql db

# initalized the configuration of the db
config = {
    "NAME":"YOUR-DB-NAME",
    "HOST":"YOUR-HOST",
    "PASSWORD":"YOUR-PASSWORD",
    "USER":"YOUR-USER",
}

db = RadwanORM()
db = db.connect(
    dbtype='mysql', # set the db type
    config=config # set the db configuration
)
```


----
### Create The Custom Tables With Their Fields.

```python
# set the tables of the db and its fields
class User :
    full_name = Fields.String(max_len=100)
    email = Fields.String(max_len=100)
    age = Fields.Integer()
    date_of_birth = Fields.Date()
    has_car = Fields.Bool(default=False)

class Car:
    car_name = Fields.String(max_len=100)
    car_type = Fields.String(max_len=50)
    owner = Fields.ForigenKey(User,on_delete=Fields.OnDelete.CASCADE)

```

---
### Write The Tables in the db

```python
# create the table in the db
db.create_table(User) # write User table in db
db.create_table(Car) # write Car table in db
```

---
### CRUD Operations

### First:
Create the manager to manage our table in db.

```python
user = db.manage(User)
car = db.manage(Car)
```

### Secend:
Going To Create The CRUD Operations !!!

```python
# Create / inseart
user.insert(
    full_name = "Radwan Gaber",
    email = 'radwangaber22@gmail.com',
    age = 18,
    date_of_birth = '2005-05-05',
    has_car = False,
)

car.insert(
    car_name = "test car name",
    car_type = 'any car type',
    owner = (User,1) 
)


# Read all rows  
users = user.all()
print(users)

# Read One row
user_radwan = user.get(User_id=1)
print(user_radwan)

# Update row
user.update_by_id(id=1,fields=('has_car',True))

# Delete row
user.delete(User_id=1)

```


---

### [ NOTE ] : i created this orm  for fun :)  
