use aerolineas;

bulk insert dbo.aerolinea
from 'C:\Users\HP Pavilion\Desktop\analisis 3\aviones_dataset_pro.csv'
with
(
    format = 'csv',
    fieldterminator = ',',
    rowterminator = '\n',
    firstrow = 2
);

select * from aerolinea;

-- limpiar datos nulos en la columna delay_minutes
update aerolinea
set delay_minutes = 0
where delay_minutes is null;
-- verificar que no haya datos nulos
select * from aerolinea
where delay_minutes is null;

-- seleccionar los vuelos con destino a 'CDMX'
 select * from aerolinea
 where destination = 'CDMX';

 -- seleccionar la aerolinea mas spopular (segun numero de vuelos)
 select airline, count(*) as numero_de_vuelos
 from aerolinea
 group by airline
 order by numero_de_vuelos desc;

 -- seleccionar la aerolinea menos popular (segun numero de vuelos)
 select airline, count(*) as numero_de_vuelos
 from aerolinea
 group by airline
 order by numero_de_vuelos asc;

 -- seleccionar el destino mas visitado
  select destination, count(*) as numero_de_vuelos
  from aerolinea
  group by destination
  order by numero_de_vuelos desc;

  --seleccionar el boleto mas caro y el mas barato
  select min(ticket_price) as boleto_mas_barato, max(ticket_price) as boleto_mas_caro
  from aerolinea;

  -- Top 10 rutas con mayor retraso promedio
  select origin, destination, avg(delay_minutes) as retraso_promedio
  from aerolinea
  group by origin, destination
  order by retraso_promedio desc
  offset 0 rows fetch next 10 rows only;

  -- Aerolíneas con mayor tasa de cancelación
  select airline, 
         sum(case when status = 'Cancelled' then 1 else 0 end) * 100.0 / count(*) as tasa_cancelacion
         from aerolinea
         group by airline
         order by tasa_cancelacion desc;

-- Comparación de desempeño entre tipos de avión
 select aircraft_type, 
        avg(delay_minutes) as retraso_promedio
        from aerolinea
        group by aircraft_type
        order by retraso_promedio asc;

-- total del numero de aviones por tipo de aeronave
 select aircraft_type, count(*) as numero_de_aviones
 from aerolinea
 group by aircraft_type
 order by numero_de_aviones desc;

 --seleccionar todos los vuelos con retraso mayor a 30 minutos
 select * from aerolinea
 where delay_minutes > 30;

 --ingresos totales
 select sum(ticket_price) as ingresos_totales
 from aerolinea;

 -- total de vuelos cancelados
  select count(*) as total_vuelos_cancelados
  from aerolinea
  where status = 'Cancelled'; 
  --ingresos perdidos por vuelos cancelados
  select sum(ticket_price) as ingresos_perdidos
  from aerolinea
  where status = 'Cancelled';

  -- estimacion de costos perdidos por retrasos (mayor a 30 minutos)
  select sum(delay_minutes * 10) as costos_perdidos_por_retrasos
  from aerolinea
  where delay_minutes > 30;

  -- costos acumulados por cancelaciones y retrasos
  select 
    (select sum(ticket_price) from aerolinea where status = 'Cancelled') +
    (select sum(delay_minutes * 10) from aerolinea where delay_minutes > 30) 
    as costos_acumulados_por_cancelaciones_y_retrasos;

 --seleccionar los vuelos con mayor retraso  
 select * from aerolinea 
 where delay_minutes = (select max(delay_minutes) from aerolinea);