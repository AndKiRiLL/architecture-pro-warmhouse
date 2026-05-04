# Задание 1. Анализ и планирование

### 1. Описание функциональности монолитного приложения

**Управление отоплением:**

- Пользователи могут удалённо включать/выключать отопление в своих домах.
- Система поддерживает удалённое включение/отключение реле отопления.
- Система поддерживает одновременное управление до 100 модулями.

**Мониторинг температуры:**

- Пользователи могут просматривать текущую температуру в своих домах через веб-интерфейс
- Система поддерживает запрос текущих показаний с датчиков в реальном времени.
- Система поддерживает отображение температуры в веб-интерфейсе без истории изменений.


### 2. Анализ архитектуры монолитного приложения

- Язык программирования: Go
- База данных: PostgreSQL
- Архитектура: Монолитная, все компоненты системы (обработка запросов, бизнес-логика, работа с данными) находятся в рамках одного приложения.
- Взаимодействие: Синхронное, запросы обрабатываются последовательно.
- Масштабируемость: Ограничена, так как монолит сложно масштабировать по частям.
- Развертывание: Требует остановки всего приложения.

### 3. Определение доменов и границы контекстов

- Домен "Управление отоплением":
	- Функции: включение / выключение отопления, отправка команд на реле.
	- Сущности: реле, команды управления.
	- Связанные данные: состояние отопления (вкл/выкл)

- Домен "Мониторинг температуры":
	- Функции: запрос текущей температуры с датчиков, отображение пользователю.
	- Сущности: датчик температуры, показания температуры.
	- Связанные данные: текущее значение температуры.

### **4. Проблемы монолитного решения**

- Нет возможности добавления новых типов устройств
- Пользователь не может самостоятельно подключать устройства
- Сложно масштабировать
- Развертывание требует остановки всего приложения 
- Синхронное взаимодействие с датчиками

### 5. Визуализация контекста системы — диаграмма С4

[Диаграмма контекста As-Is](https://github.com/AndKiRiLL/architecture-pro-warmhouse/blob/warmhouse/diagrams/As-Is/Diagram-context.svg)

# Задание 2. Проектирование микросервисной архитектуры

Также добавлю очень важную диаграмму для To-Be
**Диаграмма контекста (Context)**  
[Диаграмма контекста To-Be](https://github.com/AndKiRiLL/architecture-pro-warmhouse/blob/warmhouse/diagrams/To-Be/Diagram-context.svg)

**Диаграмма контейнеров (Containers)**  
[Диаграмма контейнеров To-Be](https://github.com/AndKiRiLL/architecture-pro-warmhouse/blob/warmhouse/diagrams/To-Be/Diagram-container.svg)

**Диаграммы компонентов (Components)**  

 - Диаграммы компонентов клиентской логики
	- [Диаграмма компонентов "Мобильное приложение"](https://github.com/AndKiRiLL/architecture-pro-warmhouse/blob/warmhouse/diagrams/To-Be/services/client-logic/Diagram-components-mobile-app.svg)

	- [Диаграмма компонентов "Веб приложение"](https://github.com/AndKiRiLL/architecture-pro-warmhouse/blob/warmhouse/diagrams/To-Be/services/client-logic/Diagram-components-web-app.svg)

 - Диаграммы компонентов бизнес логики
	- [Диаграмма компонентов "Сервис Пользователей"](https://github.com/AndKiRiLL/architecture-pro-warmhouse/blob/warmhouse/diagrams/To-Be/services/business-logic/Diagram-components-user-service.svg)

	- [Диаграмма компонентов "Сервис Устройств и Сценариев"](https://github.com/AndKiRiLL/architecture-pro-warmhouse/blob/warmhouse/diagrams/To-Be/services/business-logic/Diagram-components-device-and-scenario-service.svg)

	- [Диаграмма компонентов "Сервис Телеметрии"](https://github.com/AndKiRiLL/architecture-pro-warmhouse/blob/warmhouse/diagrams/To-Be/services/business-logic/Diagram-components-telemetry-service.svg)

	- [Диаграмма компонентов "Сервис Каталога и Платежей"](https://github.com/AndKiRiLL/architecture-pro-warmhouse/blob/warmhouse/diagrams/To-Be/services/business-logic/Diagram-components-catalog-and-payments-service.svg)

 - Диаграммы компонентов технической логики
	- [Диаграмма компонентов "API-шлюз"](https://github.com/AndKiRiLL/architecture-pro-warmhouse/blob/warmhouse/diagrams/To-Be/services/tech-logic/Diagram-components-api-gateway.svg)

	- [Диаграмма компонентов "Транзакционная БД"](https://github.com/AndKiRiLL/architecture-pro-warmhouse/blob/warmhouse/diagrams/To-Be/services/tech-logic/Diagram-components-transaction-bd.svg)

	- [Диаграмма компонентов "Брокер сообщений"](https://github.com/AndKiRiLL/architecture-pro-warmhouse/blob/warmhouse/diagrams/To-Be/services/tech-logic/Diagram-components-broker-message.svg)

	- [Диаграмма компонентов "БД Временных рядов"](https://github.com/AndKiRiLL/architecture-pro-warmhouse/blob/warmhouse/diagrams/To-Be/services/tech-logic/Diagram-components-bd-timeseries.svg)

**Диаграмма кода (Code)**

- Диаграммы кода User Service
	- [Диаграмма кода "User Manager"](https://github.com/AndKiRiLL/architecture-pro-warmhouse/blob/warmhouse/diagrams/To-Be/codes/business-logic/user-service/Diagram-codes-user-manager.svg)

# Задание 3. Разработка ER-диаграммы

[ER-диаграмма](https://github.com/AndKiRiLL/architecture-pro-warmhouse/blob/warmhouse/diagrams/To-Be/Diagram-ER.svg)

# Задание 4. Создание и документирование API

### 1. Тип API

Обосновываю решение:  
1. Выбор синхронного REST API на текущий момент:  
	- Простота реализации и отладки - REST на HTTP/JSON является наиболее зрелым и понятным подходом, имеющим огромную экосистему инструментов и библиотек для любого языка программирования.
	- Прозрачность взаимодействия - каждый запрос к микросервису инициирует немедленный ответ, что упрощает понимание потока данных и выявление ошибок на начальных этапах разработки.
	- Универсальность - не требует дополнительной инфраструктуры (брокеров сообщений), что снижает порог входа и упрощает развёртывание MVP (минимально жизнеспособного продукта).

2. Возможность расширения асинхронным взаимодействием в будущем:
	- Сценарии для асинхронности – по мере роста системы могут появиться задачи, не требующие мгновенного ответа (рассылка уведомлений, генерация отчётов, логирование событий, интеграция с медленными внешними системами).
	- Повышение надёжности и развязки – брокер сообщений (например, RabbitMQ или Kafka) позволит одному сервису публиковать события, не дожидаясь обработки подписчиками, а также гарантирует доставку даже при временной недоступности потребителя.
	- Горизонтальное масштабирование – асинхронная модель упростит организацию очередей задач с несколькими конкурентными обработчиками.
	- Отказоустойчивость – при пиковых нагрузках брокер выступит в роли буфера, предотвращая потерю запросов.

### 2. Документация API

[Документация API](https://andkirill.github.io/architecture-pro-warmhouse/)

# Задание 5. Работа с docker и docker-compose

Перейдите в apps.

Там находится приложение-монолит для работы с датчиками температуры. В README.md описано как запустить решение.

Вам нужно:

1) сделать простое приложение temperature-api на любом удобном для вас языке программирования, которое при запросе /temperature?location= будет отдавать рандомное значение температуры.

Locations - название комнаты, sensorId - идентификатор названия комнаты

```
	// If no location is provided, use a default based on sensor ID
	if location == "" {
		switch sensorID {
		case "1":
			location = "Living Room"
		case "2":
			location = "Bedroom"
		case "3":
			location = "Kitchen"
		default:
			location = "Unknown"
		}
	}

	// If no sensor ID is provided, generate one based on location
	if sensorID == "" {
		switch location {
		case "Living Room":
			sensorID = "1"
		case "Bedroom":
			sensorID = "2"
		case "Kitchen":
			sensorID = "3"
		default:
			sensorID = "0"
		}
	}
```

2) Приложение следует упаковать в Docker и добавить в docker-compose. Порт по умолчанию должен быть 8081

3) Кроме того для smart_home приложения требуется база данных - добавьте в docker-compose файл настройки для запуска postgres с указанием скрипта инициализации ./smart_home/init.sql

Для проверки можно использовать Postman коллекцию smarthome-api.postman_collection.json и вызвать:

- Create Sensor
- Get All Sensors

Должно при каждом вызове отображаться разное значение температуры

Ревьюер будет проверять точно так же.

** (Выполнил)**


# **Задание 6. Разработка MVP**

Необходимо создать новые микросервисы и обеспечить их интеграции с существующим монолитом для плавного перехода к микросервисной архитектуре. 

### **Что нужно сделать**

1. Создайте новые микросервисы для управления телеметрией и устройствами (с простейшей логикой), которые будут интегрированы с существующим монолитным приложением. Каждый микросервис на своем ООП языке.
2. Обеспечьте взаимодействие между микросервисами и монолитом (при желании с помощью брокера сообщений), чтобы постепенно перенести функциональность из монолита в микросервисы. 

В результате у вас должны быть созданы Dockerfiles и docker-compose для запуска микросервисов. 