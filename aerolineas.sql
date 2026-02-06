create database aerolineas;
use aerolineas;

create table aerolinea(
 flight_id VARCHAR(10) PRIMARY KEY,
 airline VARCHAR(50),
 origin VARCHAR(10),
 destination VARCHAR(10),
 departure_time TIME,
 arrival_time TIME,
 delay_minutes INT,
 status VARCHAR(20),
 ticket_price DECIMAL(10,2),
 aircraft_type VARCHAR(20)
);

select * from aerolinea;