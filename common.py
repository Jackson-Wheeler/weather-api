from typing import Union, List
from pydantic import BaseModel

# Device info for the ESP32 sensor
# class DeviceInfo(BaseModel):
#     group_id: str
#     mac: str

# the recorded Bluetooth Low Energy device's information
class BLEDevice(BaseModel):
    mac: str # mac address of device
    rssi: str  # Received Signal Strength Indicator

class LogInfo(BaseModel):
    gn: int # group number
    espmac: str # MAC address of ESP device
    devices: List[BLEDevice]