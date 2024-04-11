import time
from pybleno import *

bleno = Bleno()

PrimaryService = BlenoPrimaryService
Characteristic = BlenoCharacteristic

class MyCharacteristic(Characteristic):
    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': 'fffffffffffffffffffffffffffffff1',
            'properties': ['read', 'write'],
            'value': None
        })

    def onReadRequest(self, offset, callback):
        print('MyCharacteristic - onReadRequest: value = ' + str(self._value))
        callback(Characteristic.RESULT_SUCCESS, self._value)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data
        print('MyCharacteristic - onWriteRequest: value = ' + str(self._value))
        callback(Characteristic.RESULT_SUCCESS)

def onStateChange(state):
    print('on -> stateChange: ' + state)

    if (state == 'poweredOn'):
        bleno.startAdvertising('myDevice', ['fffffffffffffffffffffffffffffff0'])
    else:
        bleno.stopAdvertising()

bleno.on('stateChange', onStateChange)

myService = PrimaryService({
    'uuid': 'fffffffffffffffffffffffffffffff0',
    'characteristics': [
        MyCharacteristic()
    ]
})

bleno.setServices([
    myService
])

bleno.start()

print ('Hit <ENTER> to disconnect')

if (input()):
    bleno.stopAdvertising()
    bleno.disconnect()