# sary-restaurant-reservation-app
This project consists of 3 apps as following
# 1. Employees manager
### APIs:
>- [x] Add employee (given employee_id, employee_name, employee_password, employee_role)
>- [x] Delete employee (giver employee_id)
>- [x] Get all employees
# 2. Tables manager
### APIs:
>- [x] Add table (given table_id, seats_number)
>- [x] Delete table (given table_id)
>- [x] Get all tables
# 3. Reservations manager
### APIs:
>- [x] Get Available timeslots for each table(given seats_number)
>- [x] Reserve a timeslot (given start_time, end_time, table_id)  
>- [x] Get today's reservations
>- [x] Get all reservations
>- [x] Delete reservation (givem reservation_id)


# Not Finished yet
1. Authentication wasn't added but i can take some time to study about it and apply it if i still have time 
2. Testing wasn't perfect, i just used some test date and tested some corner cases but i havn't provided dedicated APIs for testing 

# Notes
- Algorithm: I prefer to discuss my algorithms over writing notes but if you want it i can put some extra time writing each API's algorithm and how i approached the problem 
- Postman Collection/Environment are included with name "sary-restaurant-reservation-app.postman_collection".
- I had some health issues so technically i have started working on the task on Saturday 26-03-2023 so i ran out of time and almost worked 2 days on the task
- I'm using Django (V 4.1.2) and PostgreSQL (V 15.2)