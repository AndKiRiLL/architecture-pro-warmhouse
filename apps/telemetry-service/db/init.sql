CREATE TABLE IF NOT EXISTS telemtry (
    id SERIAL PRIMARY KEY,
    device_id DOUBLE PRECISION,
    device_type VARCHAR(100) NOT NULL,
    value DOUBLE PRECISION,
    unit VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL
);

CREATE INDEX idx_telemtry_device_type ON telemtry(device_type);

-- Опционально: добавить тестовый датчик
INSERT INTO telemtry (device_id, device_type, value, unit, timestamp)
VALUES (1, 'temperature', 20.5, '°C', NOW())
ON CONFLICT DO NOTHING;