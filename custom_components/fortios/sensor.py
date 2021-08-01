
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    DATA_GIGABITS,
    PERCENTAGE,
)
from homeassistant.exceptions import PlatformNotReady
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle



SENSOR_TYPES = {
    "version": ["Version", PERCENTAGE, "mdi:percent"],
    "Connected": ["Connected", DATA_GIGABITS, "mdi:download"]
}



    sensors = []
    for variable in config[CONF_MONITORED_VARIABLES]:
        sensors.append(EBoxSensor(ebox_data, variable, name))

    async_add_entities(sensors, True)


class EBoxSensor(SensorEntity):
    """Implementation of a EBox sensor."""

    def __init__(self, ebox_data, sensor_type, name):
        """Initialize the sensor."""
        self.client_name = name
        self.type = sensor_type
        self._name = SENSOR_TYPES[sensor_type][0]
        self._unit_of_measurement = SENSOR_TYPES[sensor_type][1]
        self._icon = SENSOR_TYPES[sensor_type][2]
        self.ebox_data = ebox_data
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.client_name} {self._name}"
    
    @property
    def unique_id(self):
        """Return the unique ID."""
        return f"{self._client_name}_{self._name}"


    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    async def async_update(self):
        """Get the latest data from EBox and update the state."""
        await self.ebox_data.async_update()
        if self.type in self.ebox_data.data:
            self._state = round(self.ebox_data.data[self.type], 2)


class EBoxData:
    """Get data from Ebox."""

    def __init__(self, username, password, httpsession):
        """Initialize the data object."""
        self.client = EboxClient(username, password, REQUESTS_TIMEOUT, httpsession)
        self.data = {}

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Get the latest data from Ebox."""
        try:
            await self.client.fetch_data()
        except PyEboxError as exp:
            _LOGGER.error("Error on receive last EBox data: %s", exp)
            return
        # Update data
        self.data = self.client.get_data()
