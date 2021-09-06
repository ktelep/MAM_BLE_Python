import asyncio
import sys
import logging

from bleak import BleakScanner, BleakClient
from bleak.backends.scanner import AdvertisementData
from bleak.backends.device import BLEDevice
from bleak.exc import BleakError

MAM_NAME = "MAM"
MAM_SERV_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
MAM_SERVICE_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"
MAM_NOTIFY_UUID  = "0000fff4-0000-1000-8000-00805f9b34fb"
MAM_WRITE_UUID   = "0000fff5-0000-1000-8000-00805f9b34fb"

def notification_handler(sender, dat):
    log = logging.getLogger(__name__)
    devid = (dat[1] << 16) + (dat[2] << 8) + dat[3]
    count = (dat[4] << 16) + (dat[5] << 8) + dat[6]
    log.info(f'Ball ID: {devid} - Count: {count}')

async def MAM_terminal():
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    h = logging.StreamHandler(sys.stdout)
    h.setLevel(logging.DEBUG)
    log.addHandler(h)

    def match_mam_uuid(device: BLEDevice, adv:AdvertisementData):
        print(adv.service_uuids)
        if MAM_SERV_UUID.lower() in adv.service_uuids:
            return True

    #device = await BleakScanner.find_device_by_filter(match_mam_uuid)
    #print(device)

    #async with BleakClient(device) as client:
    async with BleakClient('00:00:00:00:42:5b') as client:
        log.info(f"Connected: {client.is_connected}")
        paired = await client.pair(protection_level=1)
        log.info(f"Paired: {paired}")

    #  Get Bounces
        await client.write_gatt_char(MAM_WRITE_UUID,
                            bytearray([0x56,0x0]))
        
    #  Setup Notifier
        log.info("Bounce the ball a few times to get count")
        await client.start_notify(MAM_NOTIFY_UUID, notification_handler)
        await asyncio.sleep(5.0)
        await client.stop_notify(MAM_NOTIFY_UUID)
    

try:
    loop=asyncio.get_event_loop()
    loop.run_until_complete(MAM_terminal())
except asyncio.CancelledError:
    # task is cancelled on disconnect, so we ignore this error
    pass