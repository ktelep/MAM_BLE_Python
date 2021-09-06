import asyncio
import sys
import logging

from bleak import BleakScanner, BleakClient
from bleak.backends.scanner import AdvertisementData
from bleak.backends.device import BLEDevice

MAM_NAME = "MAM"
MAM_SERV_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
MAM_SERVICE_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"
MAM_NOTIFY_UUID  = "0000fff4-0000-1000-8000-00805f9b34fb"
MAM_WRITE_UUID   = "0000fff5-0000-1000-8000-00805f9b34fb"

async def MAM_terminal():
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    h = logging.StreamHandler(sys.stdout)
    h.setLevel(logging.DEBUG)
    log.addHandler(h)

    def match_mam_uuid(device: BLEDevice, adv:AdvertisementData):
        if MAM_NAME in device.name:
            return True

    device = await BleakScanner.find_device_by_filter(match_mam_uuid)
    print(device)

try:
    asyncio.run(MAM_terminal())
except asyncio.CancelledError:
    # task is cancelled on disconnect, so we ignore this error
    pass