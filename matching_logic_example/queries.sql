
select product, destination, station_name, min(departure_time) as first_departure
from departures
join stations on station_id = station 
where departure_time::date = date '2020-12-06'
group by product, destination, station_name
order by product, destination, first_departure asc
limit 10;

select product, destination, station_name, departure_time
from departures
join stations on station_id = station 
where departure_time::timestamp > timestamp '2020-12-07 04:00:00'
AND destination = 'Flughafen München'
AND product = 'SBAHN:S1'
ORDER BY departure_time asc
LIMIT 10;

select min(departure_time), max(departure_time)
from departures;


select product, destination, station_name, departure_time
from departures
join stations on station_id = station 
where destination = 'Flughafen München'
AND product = 'SBAHN:S1'
AND station_name = 'Isartor'
ORDER BY departure_time asc
LIMIT 10;

select distinct(station_name)
from departures
join stations on station_id = station 
where destination = 'Flughafen München'
AND product = 'SBAHN:S1';


select product, destination, station_name, departure_time
from departures
join stations as s on s.station_id = station 
join lines as l on l.station_id = station
where destination = 'Flughafen München'
AND product = 'SBAHN:S1'
AND station_name = 'Isartor'
ORDER BY departure_time asc
LIMIT 10;

 de:09174:6820
 de:09173:4750
 de:09188:5450
 de:09162:1300
 de:09188:5370
 de:09162:10
 de:09162:720
 de:09177:3290
 de:09162:1100
 de:09175:4010

select product, destination, station_name, departure_time, l.start, l.end
from departures
join stations as s on s.station_id = station 
join lines as l on l.station_id = station
where destination = 'Flughafen München'
AND line = 'S1a'
ORDER BY departure_time asc
LIMIT 10;



SELECT * 
FROM lines AS l
WHERE SUBSTRING(l.line,1,2) = 'S1'
AND (l.start = 'Flughafen München' OR l.end = 'Flughafen München');



select departure_id, line, destination, station_name, departure_time, start, end order, 
from departures 
join stations on station_id = station 
where departure_time::timestamp > timestamp '2020-12-07 04:00:00'
AND departure_time::timestamp < timestamp '2020-12-08 08:00:00' 
AND destination = 'Flughafen München' 
AND product = 'SBAHN:S1' 
ORDER BY departure_time asc


select d.departure_id, s.line, d.destination, s.station_id, s.station_name, d.departure_time, s.start, s.end,  s.order, d.delay
from departures as d, (
    select station_name, l.station_id, l.line, l.start, l.end, l.order
    from lines as l, stations as s
    where s.station_id = l.station_id) as s
where d.station = s.station_id
AND SUBSTRING(d.product, 7,2) = SUBSTRING(s.line, 1,2)
AND (d.destination = s.start OR d.destination = s.end)
;
