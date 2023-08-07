"""Zaptec component binary sensors."""
from __future__ import annotations

import logging
from dataclasses import dataclass

from homeassistant import const
from homeassistant.components.button import (ButtonDeviceClass, ButtonEntity,
                                             ButtonEntityDescription)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import ZaptecBaseEntity, ZaptecUpdateCoordinator
from .api import Account, Charger
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ZaptecButton(ZaptecBaseEntity, ButtonEntity):

    async def async_press(self) -> None:
        """Press the button."""
        _LOGGER.debug(
            "Press %s '%s' in %s",
            self.__class__.__qualname__,
            self.entity_description.key,
            self.zaptec_obj.id
        )

        key = self.description.key
        charger: Charger = self.zaptec_obj

        try:
            await charger.command(key)
        except Exception as exc:
            raise HomeAssistantError(exc) from exc


@dataclass
class ZapButtonEntityDescription(ButtonEntityDescription):

    cls: type|None = None


INSTALLATION_ENTITIES: list[EntityDescription] = [
]

CIRCUIT_ENTITIES: list[EntityDescription] = [
]

CHARGER_ENTITIES: list[EntityDescription] = [
    ZapButtonEntityDescription(
        key="resume_charging",
        translation_key="resume_charging",
        icon="mdi:play-circle-outline",
    ),
    ZapButtonEntityDescription(
        key="stop_pause",
        translation_key="stop_pause",
        icon="mdi:pause-circle-outline",
    ),
    ZapButtonEntityDescription(
        key="restart_charger",
        translation_key="restart_charger",
        entity_category=const.EntityCategory.DIAGNOSTIC,
        icon="mdi:restart"
    ),
    ZapButtonEntityDescription(
        key="update_firmware",
        translation_key="update_firmware",
        entity_category=const.EntityCategory.DIAGNOSTIC,
        icon="mdi:memory"
    ),
]


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    _LOGGER.debug("Setup buttons")

    coordinator: ZaptecUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    acc = coordinator.account

    entities = ZaptecButton.create_from_zaptec(
        acc,
        coordinator,
        INSTALLATION_ENTITIES,
        CIRCUIT_ENTITIES,
        CHARGER_ENTITIES,
    )
    async_add_entities(entities, True)
