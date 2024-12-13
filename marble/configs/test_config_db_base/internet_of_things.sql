-- 1. Devices table (stores information about IoT devices)
CREATE TABLE devices (
    device_id SERIAL PRIMARY KEY,  -- Unique device ID
    device_name VARCHAR(255) NOT NULL,  -- Device name
    device_type VARCHAR(100) NOT NULL,  -- Device type (e.g., sensor, actuator)
    manufacturer VARCHAR(255),  -- Manufacturer of the device
    model_number VARCHAR(100),  -- Model number of the device
    status VARCHAR(50) DEFAULT 'active',  -- Device status (e.g., active, inactive)
    last_communication TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Last communication time
);

-- 2. Users table (stores users of the IoT system)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,  -- Unique user ID
    first_name VARCHAR(100),  -- User's first name
    last_name VARCHAR(100),   -- User's last name
    email VARCHAR(255) UNIQUE NOT NULL,  -- User email
    password VARCHAR(255) NOT NULL,  -- User password
    role VARCHAR(50) DEFAULT 'user',  -- Role of the user (e.g., admin, user)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Account creation time
);

-- 3. Device_Data table (stores data collected by IoT devices)
CREATE TABLE device_data (
    data_id SERIAL PRIMARY KEY,  -- Unique data ID
    device_id INT REFERENCES devices(device_id),  -- Foreign key to devices
    data_value VARCHAR(255) NOT NULL,  -- Value of the data (e.g., temperature, humidity)
    data_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Time of data collection
    data_type VARCHAR(50)  -- Type of data (e.g., sensor reading, status update)
);

-- 4. Device_Logs table (stores logs for IoT devices)
CREATE TABLE device_logs (
    log_id SERIAL PRIMARY KEY,  -- Unique log ID
    device_id INT REFERENCES devices(device_id),  -- Foreign key to devices
    log_message TEXT,  -- Log message
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Time of log entry
);

-- 5. Device_Configuration table (stores configuration settings for IoT devices)
CREATE TABLE device_configuration (
    config_id SERIAL PRIMARY KEY,  -- Unique configuration ID
    device_id INT REFERENCES devices(device_id),  -- Foreign key to devices
    config_key VARCHAR(255) NOT NULL,  -- Configuration key (e.g., IP address, threshold)
    config_value VARCHAR(255) NOT NULL,  -- Configuration value
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Time of configuration update
);

-- 6. Alerts table (stores alerts triggered by IoT devices)
CREATE TABLE alerts (
    alert_id SERIAL PRIMARY KEY,  -- Unique alert ID
    device_id INT REFERENCES devices(device_id),  -- Foreign key to devices
    alert_message TEXT,  -- Description of the alert
    alert_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Time of alert
    alert_status VARCHAR(50) DEFAULT 'unresolved'  -- Alert status (e.g., resolved, unresolved)
);

-- 7. Device_Status table (stores the current status of IoT devices)
CREATE TABLE device_status (
    status_id SERIAL PRIMARY KEY,  -- Unique status ID
    device_id INT REFERENCES devices(device_id),  -- Foreign key to devices
    status_value VARCHAR(50) NOT NULL,  -- Current status (e.g., online, offline)
    status_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Time of status update
);

-- 8. Device_Commands table (stores commands sent to IoT devices)
CREATE TABLE device_commands (
    command_id SERIAL PRIMARY KEY,  -- Unique command ID
    device_id INT REFERENCES devices(device_id),  -- Foreign key to devices
    command VARCHAR(255) NOT NULL,  -- Command sent to the device
    command_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Time of command sent
    command_status VARCHAR(50) DEFAULT 'pending'  -- Command status (e.g., pending, executed)
);

-- Insert some sample devices
INSERT INTO devices (device_name, device_type, manufacturer, model_number) 
VALUES 
('Temperature Sensor', 'sensor', 'IoT Corp', 'TS-1001'),
('Smart Light', 'actuator', 'SmartHome Inc.', 'SL-2020');

-- Insert some users
INSERT INTO users (first_name, last_name, email, password, role) 
VALUES 
('John', 'Doe', 'john.doe@example.com', 'securepassword', 'admin'),
('Jane', 'Smith', 'jane.smith@example.com', 'password123', 'user');

-- Insert device data
INSERT INTO device_data (device_id, data_value, data_type) 
VALUES 
(1, '23.5', 'temperature'),
(2, 'ON', 'status');

-- Insert device logs
INSERT INTO device_logs (device_id, log_message) 
VALUES 
(1, 'Temperature sensor initialized successfully'),
(2, 'Smart light turned on remotely');

-- Insert device configuration
INSERT INTO device_configuration (device_id, config_key, config_value) 
VALUES 
(1, 'IP Address', '192.168.1.10'),
(2, 'IP Address', '192.168.1.20');

-- Insert alerts
INSERT INTO alerts (device_id, alert_message) 
VALUES 
(1, 'Temperature exceeded threshold!'),
(2, 'Smart light malfunction detected');

-- Insert device status
INSERT INTO device_status (device_id, status_value) 
VALUES 
(1, 'online'),
(2, 'offline');

-- Insert device commands
INSERT INTO device_commands (device_id, command) 
VALUES 
(1, 'Reset sensor'),
(2, 'Turn off light');
