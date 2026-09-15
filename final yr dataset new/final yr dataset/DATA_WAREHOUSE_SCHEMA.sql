
CREATE TABLE IF NOT EXISTS dim_bus (
    bus_id VARCHAR(50) PRIMARY KEY,
    registration_number VARCHAR(50) NOT NULL UNIQUE,
    bus_type VARCHAR(100) NOT NULL,
    operator VARCHAR(50) DEFAULT 'BMTC',
    capacity INT NOT NULL,
    seating_capacity INT NOT NULL,
    standing_capacity INT NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    accessibility BOOLEAN DEFAULT TRUE,
    ac_available BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'ACTIVE'
);


CREATE TABLE IF NOT EXISTS dim_stop (
    stop_id VARCHAR(50) PRIMARY KEY,
    stop_name VARCHAR(150) NOT NULL,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    area VARCHAR(100),
    zone VARCHAR(50),
    landmark VARCHAR(150),
    shelter_available BOOLEAN DEFAULT TRUE,
    accessibility BOOLEAN DEFAULT TRUE,
    active_status VARCHAR(20) DEFAULT 'ACTIVE'
);


CREATE TABLE IF NOT EXISTS dim_calendar (
    date DATE PRIMARY KEY,
    day_of_week VARCHAR(15) NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    is_holiday BOOLEAN NOT NULL,
    holiday_name VARCHAR(100) DEFAULT 'None',
    holiday_type VARCHAR(50) NOT NULL,
    is_working_day BOOLEAN NOT NULL
);


CREATE TABLE IF NOT EXISTS dim_route (
    route_id VARCHAR(50) PRIMARY KEY,
    route_name VARCHAR(150) NOT NULL,
    first_stop_name VARCHAR(150),
    last_stop_name VARCHAR(150),
    route_distance_km DECIMAL(6,2),
    scheduled_trip_duration INT
);


CREATE TABLE IF NOT EXISTS dim_road_network (
    road_id VARCHAR(50) PRIMARY KEY,
    road_name VARCHAR(150) NOT NULL,
    road_type VARCHAR(50) NOT NULL,
    length_km DECIMAL(6,2),
    lanes INT,
    maxspeed INT,
    oneway BOOLEAN,
    intersections INT,
    geometry TEXT
);



CREATE TABLE IF NOT EXISTS fact_integrated_bus_operations (
    fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_date DATE NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    route_id VARCHAR(50) NOT NULL,
    route_name VARCHAR(150),
    trip_id VARCHAR(100) NOT NULL,
    bus_id VARCHAR(50) NOT NULL,
    registration_number VARCHAR(50),
    bus_type VARCHAR(100),
    fuel_type VARCHAR(50),
    stop_id VARCHAR(50) NOT NULL,
    stop_name VARCHAR(150),
    area VARCHAR(100),
    zone VARCHAR(50),
    stop_sequence INT NOT NULL,
    scheduled_arrival TIME NOT NULL,
    actual_arrival TIME NOT NULL,
    delay_minutes DECIMAL(6,2) NOT NULL,
    passenger_count INT NOT NULL,
    bus_capacity INT NOT NULL,
    occupancy_percentage DECIMAL(5,2) NOT NULL,
    occupancy_status VARCHAR(20) NOT NULL,
    temperature DECIMAL(4,1),
    humidity INT,
    precipitation DECIMAL(5,2),
    rain DECIMAL(5,2),
    weather_code INT,
    traffic_speed DECIMAL(5,2),
    congestion_level VARCHAR(20),
    congestion_index DECIMAL(4,2),
    incident_flag BOOLEAN DEFAULT FALSE,
    day_of_week VARCHAR(15),
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    holiday_name VARCHAR(100),
    disruption_label VARCHAR(30) NOT NULL,
    FOREIGN KEY (bus_id) REFERENCES dim_bus(bus_id),
    FOREIGN KEY (stop_id) REFERENCES dim_stop(stop_id),
    FOREIGN KEY (service_date) REFERENCES dim_calendar(date),
    FOREIGN KEY (route_id) REFERENCES dim_route(route_id)
);


CREATE INDEX IF NOT EXISTS idx_fact_route_date ON fact_integrated_bus_operations(route_id, service_date);
CREATE INDEX IF NOT EXISTS idx_fact_stop_time ON fact_integrated_bus_operations(stop_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_fact_bus_trip ON fact_integrated_bus_operations(bus_id, trip_id);
CREATE INDEX IF NOT EXISTS idx_fact_disruption ON fact_integrated_bus_operations(disruption_label);


CREATE VIEW IF NOT EXISTS vw_route_performance_summary AS
SELECT 
    route_id,
    route_name,
    COUNT(DISTINCT trip_id) AS total_trips_conducted,
    COUNT(fact_id) AS total_stop_arrivals,
    ROUND(AVG(delay_minutes), 2) AS avg_delay_minutes,
    ROUND(MAX(delay_minutes), 2) AS max_delay_minutes,
    ROUND(AVG(occupancy_percentage), 1) AS avg_occupancy_pct,
    SUM(CASE WHEN delay_minutes > 10 THEN 1 ELSE 0 END) AS severe_delay_count
FROM fact_integrated_bus_operations
GROUP BY route_id, route_name;


CREATE VIEW IF NOT EXISTS vw_stop_occupancy_analytics AS
SELECT 
    stop_id,
    stop_name,
    area,
    zone,
    COUNT(fact_id) AS total_bus_visits,
    ROUND(AVG(passenger_count), 1) AS avg_passenger_count,
    ROUND(AVG(occupancy_percentage), 1) AS avg_occupancy_pct,
    SUM(CASE WHEN occupancy_status IN ('HIGH', 'NEARLY_FULL', 'FULL') THEN 1 ELSE 0 END) AS overcrowding_instances
FROM fact_integrated_bus_operations
GROUP BY stop_id, stop_name, area, zone;


CREATE VIEW IF NOT EXISTS vw_disruption_congestion_impact AS
SELECT 
    disruption_label,
    congestion_level,
    COUNT(fact_id) AS occurrence_count,
    ROUND(AVG(delay_minutes), 2) AS avg_delay_minutes,
    ROUND(AVG(traffic_speed), 1) AS avg_traffic_speed_kmph,
    ROUND(AVG(rain), 2) AS avg_rain_mm
FROM fact_integrated_bus_operations
GROUP BY disruption_label, congestion_level;
