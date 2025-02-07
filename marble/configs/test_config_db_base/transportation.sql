-- 1. Vehicles table (stores information about vehicles)
CREATE TABLE vehicles (
    vehicle_id SERIAL PRIMARY KEY,  -- Unique vehicle ID
    vehicle_type VARCHAR(50) NOT NULL,  -- Type of vehicle (e.g., truck, bus, car)
    license_plate VARCHAR(20) UNIQUE NOT NULL,  -- Vehicle license plate number
    model VARCHAR(100),  -- Vehicle model
    capacity INT NOT NULL,  -- Capacity of the vehicle
    manufacturer VARCHAR(100),  -- Manufacturer of the vehicle
    status VARCHAR(50) DEFAULT 'available',  -- Vehicle status (available, in repair, etc.)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Date of vehicle registration
);

-- 2. Drivers table (stores information about drivers)
CREATE TABLE drivers (
    driver_id SERIAL PRIMARY KEY,  -- Unique driver ID
    first_name VARCHAR(100) NOT NULL,  -- Driver's first name
    last_name VARCHAR(100) NOT NULL,  -- Driver's last name
    date_of_birth DATE,  -- Driver's date of birth
    license_number VARCHAR(50) UNIQUE NOT NULL,  -- Driver's license number
    phone VARCHAR(20),  -- Driver's phone number
    hire_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Date the driver was hired
);

-- 3. Routes table (stores information about routes)
CREATE TABLE routes (
    route_id SERIAL PRIMARY KEY,  -- Unique route ID
    start_location VARCHAR(100) NOT NULL,  -- Starting point of the route
    end_location VARCHAR(100) NOT NULL,  -- Destination of the route
    distance DECIMAL(10, 2) NOT NULL,  -- Distance in kilometers
    estimated_time TIME NOT NULL,  -- Estimated travel time
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Date of route creation
);

-- 4. Trips table (stores information about each trip)
CREATE TABLE trips (
    trip_id SERIAL PRIMARY KEY,  -- Unique trip ID
    vehicle_id INT REFERENCES vehicles(vehicle_id),  -- Foreign key to vehicles
    driver_id INT REFERENCES drivers(driver_id),  -- Foreign key to drivers
    route_id INT REFERENCES routes(route_id),  -- Foreign key to routes
    departure_time TIMESTAMP,  -- Time of departure
    arrival_time TIMESTAMP,  -- Time of arrival
    status VARCHAR(50) DEFAULT 'scheduled',  -- Trip status (scheduled, completed, canceled)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Date of trip creation
);

-- 5. Cargo table (stores information about cargo being transported)
CREATE TABLE cargo (
    cargo_id SERIAL PRIMARY KEY,  -- Unique cargo ID
    trip_id INT REFERENCES trips(trip_id),  -- Foreign key to trips
    cargo_type VARCHAR(100),  -- Type of cargo (e.g., goods, passengers)
    weight DECIMAL(10, 2),  -- Weight of the cargo in kilograms
    description TEXT,  -- Description of the cargo
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Date of cargo registration
);

-- 6. Maintenance table (stores maintenance records for vehicles)
CREATE TABLE maintenance (
    maintenance_id SERIAL PRIMARY KEY,  -- Unique maintenance ID
    vehicle_id INT REFERENCES vehicles(vehicle_id),  -- Foreign key to vehicles
    maintenance_type VARCHAR(100),  -- Type of maintenance (e.g., oil change, tire replacement)
    maintenance_date TIMESTAMP,  -- Date of maintenance
    cost DECIMAL(10, 2),  -- Cost of maintenance
    description TEXT,  -- Description of the maintenance work done
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Date of maintenance record creation
);

-- 7. Fuel_Logs table (stores fuel consumption records for vehicles)
CREATE TABLE fuel_logs (
    fuel_log_id SERIAL PRIMARY KEY,  -- Unique fuel log ID
    vehicle_id INT REFERENCES vehicles(vehicle_id),  -- Foreign key to vehicles
    fuel_date TIMESTAMP,  -- Date of fuel log entry
    fuel_quantity DECIMAL(10, 2),  -- Amount of fuel added (in liters)
    fuel_cost DECIMAL(10, 2),  -- Cost of the fuel
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Date of fuel log creation
);

-- 8. Locations table (stores information about locations for trips and routes)
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,  -- Unique location ID
    location_name VARCHAR(100) NOT NULL,  -- Location name
    latitude DECIMAL(9, 6),  -- Latitude of the location
    longitude DECIMAL(9, 6),  -- Longitude of the location
    description TEXT,  -- Description of the location
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Date of location record creation
);

-- 9. Trip_Logs table (stores detailed logs of each trip)
CREATE TABLE trip_logs (
    log_id SERIAL PRIMARY KEY,  -- Unique log ID
    trip_id INT REFERENCES trips(trip_id),  -- Foreign key to trips
    log_time TIMESTAMP,  -- Time of the log entry
    log_description TEXT,  -- Description of what happened during the trip
    location_id INT REFERENCES locations(location_id),  -- Foreign key to locations
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Date of log entry
);

-- 10. Payments table (stores payment records for transportation services)
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,  -- Unique payment ID
    trip_id INT REFERENCES trips(trip_id),  -- Foreign key to trips
    amount DECIMAL(10, 2),  -- Amount paid for the trip
    payment_method VARCHAR(50),  -- Payment method (e.g., credit card, cash)
    payment_date TIMESTAMP,  -- Date of payment
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Date of payment record creation
);

-- Sample Data Insertion

-- Insert vehicles
INSERT INTO vehicles (vehicle_type, license_plate, model, capacity, manufacturer)
VALUES
('Truck', 'ABC123', 'Model X', 20, 'Ford'),
('Bus', 'XYZ789', 'Model Y', 50, 'Mercedes');

-- Insert drivers
INSERT INTO drivers (first_name, last_name, date_of_birth, license_number, phone)
VALUES
('John', 'Doe', '1985-06-15', 'DL12345', '555-1234'),
('Jane', 'Smith', '1990-08-25', 'DL98765', '555-5678');

-- Insert routes
INSERT INTO routes (start_location, end_location, distance, estimated_time)
VALUES
('City A', 'City B', 100.5, '02:00:00'),
('City C', 'City D', 150.0, '03:00:00');

-- Insert trips
INSERT INTO trips (vehicle_id, driver_id, route_id, departure_time, arrival_time, status)
VALUES
(1, 1, 1, '2024-12-01 08:00:00', '2024-12-01 10:00:00', 'completed'),
(2, 2, 2, '2024-12-02 09:00:00', '2024-12-02 12:00:00', 'completed');

-- Insert cargo
INSERT INTO cargo (trip_id, cargo_type, weight, description)
VALUES
(1, 'Goods', 1000.00, 'Electronics shipment'),
(2, 'Passengers', 3000.00, 'Tourists for sightseeing');

-- Insert maintenance
INSERT INTO maintenance (vehicle_id, maintenance_type, maintenance_date, cost, description)
VALUES
(1, 'Oil Change', '2024-11-20', 50.00, 'Routine oil change'),
(2, 'Tire Replacement', '2024-11-25', 200.00, 'Replaced 2 tires');

-- Insert fuel logs
INSERT INTO fuel_logs (vehicle_id, fuel_date, fuel_quantity, fuel_cost)
VALUES
(1, '2024-12-01', 50.00, 100.00),
(2, '2024-12-02', 70.00, 140.00);

-- Insert locations
INSERT INTO locations (location_name, latitude, longitude, description)
VALUES
('City A', 40.7128, -74.0060, 'Starting point of route 1'),
('City B', 34.0522, -118.2437, 'Destination point of route 1');

-- Insert trip logs
INSERT INTO trip_logs (trip_id, log_time, log_description, location_id)
VALUES
(1, '2024-12-01 08:15:00', 'Departed City A', 1),
(1, '2024-12-01 09:45:00', 'Arrived in City B', 2);

-- Insert payments
INSERT INTO payments (trip_id, amount, payment_method, payment_date)
VALUES
(1, 500.00, 'Credit Card', '2024-12-01'),
(2, 1000.00, 'Cash', '2024-12-02');
