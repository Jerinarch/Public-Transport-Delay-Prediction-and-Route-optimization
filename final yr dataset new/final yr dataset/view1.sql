SELECT 
    route_id,
    route_name,
    COUNT(DISTINCT trip_id) AS total_trips_conducted,
    COUNT(*) AS total_stop_arrivals,
    ROUND(AVG(delay_minutes), 2) AS avg_delay_minutes,
    ROUND(MAX(delay_minutes), 2) AS max_delay_minutes,
    ROUND(AVG(occupancy_percentage), 1) AS avg_occupancy_pct,
    SUM(CASE WHEN delay_minutes > 10 THEN 1 ELSE 0 END) AS severe_delay_count
FROM fact_integrated_bus_operations
GROUP BY route_id, route_name;
