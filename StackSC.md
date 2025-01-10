```
┌──────────────────────────┐
│  Sensores y Actuadores   │
│ (Dispositivos IoT)       │
│ Ej.: ESP32, Raspberry Pi │
└───────────▲──────────────┘
            │
            │ Protocolos IoT (MQTT/HTTP/CoAP)
            ▼
┌──────────────────────────┐
│ Gateway IoT (Local)      │
│ Ej.: Mosquitto, Node-RED │
└───────────▲──────────────┘
            │
            │ Envío de datos al servidor
            ▼
┌────────────────────────────────────────────────┐
│ NGINX (Proxy Reverso y Balanceador de Carga)   │
│ - Distribuye el tráfico a servicios backend    │
│ - Maneja HTTPS                                 │
└───────────▲─────────────────────────┬──────────┘
            │                         │
            │                         │
┌───────────▼──────────────┐ ┌────────▼──────────┐
│ Middleware (FIWARE Orion │ │ Ngrok (Acceso Ext │
│ Context Broker, Flask)   │ │ Exposición HTTP)  │
│ Gestión de datos y APIs  │ │                   │
└───────────▲──────────────┘ └───────────────────┘
            │
            │
┌───────────▼───────────────────────┐
│ Base de Datos                     │
│ PostgreSQL, InfluxDB              │
│ Almacenamiento histórico de datos │
└───────────────────────────────────┘
            │
            ▼
┌───────────────────────────┐
│ Visualización             │
│ Ej.: Grafana, Power BI    │
│ Dashboards y reportes     │
└───────────────────────────┘

```
# Componentes Clave
1. Dispositivos IoT
Ejemplos: ESP32, Raspberry Pi.
Conexión: Envían datos mediante protocolos como MQTT o HTTP.

2. Gateway IoT
Software: Node-RED o Mosquitto para procesar datos en el borde.
Función: Conectar dispositivos IoT al middleware (FIWARE/NGINX).

3. NGINX
Rol Principal:
Actúa como proxy reverso para manejar el tráfico hacia el backend.
Sirve contenido estático como dashboards.
Proporciona seguridad mediante HTTPS (Certbot o Let's Encrypt).
Balanceo de carga: Distribuye las solicitudes entre múltiples instancias de microservicios.

4. Ngrok
Uso Principal:
Proporciona una URL pública para exponer APIs o dashboards locales.
Útil para pruebas remotas, como acceso externo a la demo.

5. Middleware
FIWARE Orion Context Broker:
Gestiona el contexto de la ciudad (sensores, datos, eventos).
Flask:
Implementa APIs personalizadas para interactuar con los datos.

6. Base de Datos
PostgreSQL:
Almacena datos estructurados (e.g., registros de sensores).
InfluxDB:
Ideal para datos de series temporales como temperatura, ruido o calidad del aire.

7. Visualización
Grafana:
Dashboards interactivos con datos en tiempo real.
Power BI:
Análisis y reportes de alto nivel para tomadores de decisiones.