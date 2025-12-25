# home-assistant-bme280

A tiny container to expose a bme280 to home assistant.

In order to use this project you need:
 - A home assistant instance
 - A MQTT server without authentication (or the Mosquitto Broker add-on)
 - The MQTT integration connected to your MQTT server
 - A BME280 connected to an I2C port of the device that runs this container (e.g. a Raspberry Pi). Make sure you have correctly configured the i2c port (run `sudo raspi-config` on a Raspberry Pi).

This image supports amd64, arm64, and armv7 CPUs.

## Example

Example `docker-compose.yaml` configuration:

```yaml
services:
  bme280:
    image: swnf/home-assistant-bme280:1-latest
    restart: unless-stopped
    environment:
      MQTT_HOST: "mqtt.example.com"
      TEMPERATURE_SENSOR_NAME: "My temperature sensor"
      HUMIDITY_SENSOR_NAME: "My humidity sensor"
      PRESSURE_SENSOR_NAME: "My pressure sensor"
      # I2C_PORT: "1"             # I2C bus number
      # I2C_ADDRESS: "118"        # Device address, 0x76 in decimal
      # READ_INTERVAL: "300"      # Update interval in seconds
    devices:
      - /dev/i2c-1:/dev/i2c-1
```