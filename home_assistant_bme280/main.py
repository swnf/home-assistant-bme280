from os import environ
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Sensor, SensorInfo
from time import sleep

from smbus2 import SMBus
from bme280 import load_calibration_params, sample


def main():
    print("Starting...")

    mqtt_settings = Settings.MQTT(host=environ["MQTT_HOST"])

    sensor_info_temperature = SensorInfo(
        name=environ["TEMPERATURE_SENSOR_NAME"],
        device_class="temperature",
        unit_of_measurement="°C",
    )
    settings_temperature = Settings(mqtt=mqtt_settings, entity=sensor_info_temperature)
    temperature_sensor = Sensor(settings_temperature)

    sensor_info_humidity = SensorInfo(
        name=environ["HUMIDITY_SENSOR_NAME"],
        device_class="humidity",
        unit_of_measurement="%",
    )
    settings_humidity = Settings(mqtt=mqtt_settings, entity=sensor_info_humidity)
    humidity_sensor = Sensor(settings_humidity)

    sensor_info_pressure = SensorInfo(
        name=environ["PRESSURE_SENSOR_NAME"],
        device_class="pressure",
        unit_of_measurement="hPa",
    )
    settings_pressure = Settings(mqtt=mqtt_settings, entity=sensor_info_pressure)
    pressure_sensor = Sensor(settings_pressure)

    print("MQTT configuration complete")

    print("Initializing Sensor...")

    port = int(environ.get("I2C_PORT", "1"))
    address = int(environ.get("I2C_ADDRESS", "118"))  # 0x76
    bus = SMBus(port)
    calibration_params = load_calibration_params(bus, address)

    print("Sensor ready")

    read_interval = int(environ.get("READ_INTERVAL", "300"))  # 5min
    print(f"Reading sensor every {read_interval}s")
    while True:
        data = sample(bus, address, calibration_params)
        print(data)
        temperature_sensor.set_state(round(data.temperature, 1))
        humidity_sensor.set_state(round(data.humidity, 1))
        pressure_sensor.set_state(round(data.pressure, 1))
        sleep(read_interval)


if __name__ == "__main__":
    main()
