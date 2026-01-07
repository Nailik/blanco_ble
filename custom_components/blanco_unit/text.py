"""Text entities to define calibration properties for Blanco Unit BLE entities."""

from homeassistant.components.text import TextEntity, TextMode
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import BlancoUnitConfigEntry
from .base import BlancoUnitBaseEntity
from .coordinator import BlancoUnitCoordinator


async def async_setup_entry(
    _: HomeAssistant,
    config_entry: BlancoUnitConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the TextEntities for calibration."""
    coordinator: BlancoUnitCoordinator = config_entry.runtime_data

    async_add_entities(
        [
            CalibrationStillText(coordinator),
            CalibrationSodaText(coordinator),
        ]
    )


class CalibrationStillText(BlancoUnitBaseEntity, TextEntity):
    """Implementation of the Still Water Calibration Text."""

    _attr_unique_id = "calibration_still"
    _attr_translation_key = _attr_unique_id
    _attr_native_min = 1
    _attr_native_max = 10
    _attr_mode = TextMode.TEXT
    _attr_pattern = r"^\d+$"
    _attr_icon = "mdi:water"
    _attr_entity_category = EntityCategory.CONFIG

    @property
    def available(self) -> bool:
        """Set availability if settings are available."""
        return (
            super().available
            and self.coordinator.data.settings is not None
        )

    @property
    def native_value(self):
        """Return the state of the entity."""
        if self.coordinator.data.settings is None:
            return None
        return str(self.coordinator.data.settings.calib_still_wtr)

    async def async_set_value(self, value: str) -> None:
        """Set the calibration value from the UI."""
        await self.coordinator.set_calibration_still(int(value))


class CalibrationSodaText(BlancoUnitBaseEntity, TextEntity):
    """Implementation of the Soda Water Calibration Text."""

    _attr_unique_id = "calibration_soda"
    _attr_translation_key = _attr_unique_id
    _attr_native_min = 1
    _attr_native_max = 10
    _attr_mode = TextMode.TEXT
    _attr_pattern = r"^\d+$"
    _attr_icon = "mdi:cup-water"
    _attr_entity_category = EntityCategory.CONFIG

    @property
    def available(self) -> bool:
        """Set availability if settings are available."""
        return (
            super().available
            and self.coordinator.data.settings is not None
        )

    @property
    def native_value(self):
        """Return the state of the entity."""
        if self.coordinator.data.settings is None:
            return None
        return str(self.coordinator.data.settings.calib_soda_wtr)

    async def async_set_value(self, value: str) -> None:
        """Set the calibration value from the UI."""
        await self.coordinator.set_calibration_soda(int(value))
