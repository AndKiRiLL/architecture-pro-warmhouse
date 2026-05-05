import grpc
from concurrent import futures
import random
import time
from datetime import datetime, timezone

# Импорты сгенерированных файлов (создадим далее)
import telemetry_pb2
import telemetry_pb2_grpc

class TelemetryServicer(telemetry_pb2_grpc.TelemetryServiceServicer):
    
    def GetTemperature(self, request, context):
        """Получаем температуру по запросу"""
        location = request.location
        sensor_id = request.sensor_id
        
        # Логика как в задании
        if not location and sensor_id:
            location_map = {"1": "Living Room", "2": "Bedroom", "3": "Kitchen"}
            location = location_map.get(sensor_id, "Unknown")
        
        if not sensor_id and location:
            sensor_map = {"Living Room": "1", "Bedroom": "2", "Kitchen": "3"}
            sensor_id = sensor_map.get(location, "0")
        
        # Генерируем случайную температуру
        temperature = round(random.uniform(15.0, 35.0), 2)
        
        return telemetry_pb2.TemperatureResponse(
            sensor_id=sensor_id,
            location=location,
            value=temperature,
            unit="celsius",
            status="active",
            timestamp=datetime.now(timezone.utc).isoformat()
        )
    
    def StreamTemperatures(self, request_iterator, context):
        """Стриминг температуры"""
        for request in request_iterator:
            yield self.GetTemperature(request, context)
            time.sleep(1)  # Имитация задержки

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    telemetry_pb2_grpc.add_TelemetryServiceServicer_to_server(
        TelemetryServicer(), server
    )
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    print("Telemetry service started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

# Для теста в postman
# [
#     {"location": "Living Room", "sensor_id": ""},
#     {"location": "Bedroom", "sensor_id": ""},
#     {"location": "", "sensor_id": "3"},
#     {"location": "Kitchen", "sensor_id": ""}
# ]