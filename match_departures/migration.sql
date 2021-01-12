-- copy missing data from departures into matched_departures and migrate table
-- rename table

BEGIN;

LOCK TABLE departures IN ACCESS EXCLUSIVE MODE;

CREATE TABLE departures_tmp AS 
SELECT  d.created_at,
 d.updated_at,
 d.station,
 d.departure_id,
 d.departure_time,
 d.passed_before,
 d.product,
 d.destination,
 d.delay,
 d.platform,
 d.cancelled,
 m.trip_id,
 m.trip_searched,
 m.trip_matched,
 m.line_id
FROM departures d
LEFT JOIN matched_departures m on m.departure_id = d.departure_id
WHERE m.departure_id IS NOT NULL
UNION
SELECT d.created_at,
 d.updated_at,
 d.station,
 d.departure_id,
 d.departure_time,
 d.passed_before,
 d.product,
 d.destination,
 d.delay,
 d.platform,
 d.cancelled,
 NULL AS trip_id,
 False AS trip_searched,
 False AS trip_matched,
 NULL AS line_id
FROM departures d
LEFT JOIN matched_departures m on m.departure_id = d.departure_id
WHERE m.departure_id IS NULL;

ALTER TABLE departures_tmp
   ALTER COLUMN trip_searched SET DEFAULT False
 , ALTER COLUMN trip_matched SET DEFAULT False
 , ALTER COLUMN trip_id SET DEFAULT NULL
 , ALTER COLUMN line_id SET DEFAULT NULL
 , ADD PRIMARY KEY (departure_id);

ALTER TABLE departures RENAME TO departures_backup;
ALTER TABLE departures_tmp RENAME TO departures;

COMMIT;
