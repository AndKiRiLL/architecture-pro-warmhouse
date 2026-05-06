CREATE TABLE IF NOT EXISTS devices (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    value DOUBLE PRECISION,
    unit VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'inactive',
    last_updated TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_devices_location ON devices(location);
CREATE INDEX idx_devices_status ON devices(status);
CREATE INDEX idx_devices_type ON devices(type);

-- Опционально: добавить тестовый датчик
INSERT INTO devices (name, type, location, unit, status, last_updated, created_at)
VALUES ('Test Divece', 'temperature', 'Living Room', '°C', 'active', NOW(), NOW())
ON CONFLICT DO NOTHING;