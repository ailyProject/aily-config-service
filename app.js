const bleno = require('bleno');

const name = 'MyDevice';
const serviceUuids = ['fffffffffffffffffffffffffffffff0'];

bleno.on('stateChange', function(state) {
    if (state === 'poweredOn') {
        bleno.startAdvertising(name, serviceUuids);
    } else {
        bleno.stopAdvertising();
    }
});

bleno.on('advertisingStart', function(error) {
    if (!error) {
        const echoService = new bleno.PrimaryService({
            uuid: 'fffffffffffffffffffffffffffffff0',
            characteristics: [
                new bleno.Characteristic({
                    value: null, 
                    uuid: 'fffffffffffffffffffffffffffffff1', 
                    properties: ['read', 'write', 'notify'], 
                    onReadRequest: function(offset, callback) {
                        console.log('Read request received');
                        callback(this.RESULT_SUCCESS, new Buffer('Hello!'));
                    },
                    onWriteRequest: function(data, offset, withoutResponse, callback) {
                        console.log('Write request received. Data: ' + data.toString());
                        callback(this.RESULT_SUCCESS);
                    }
                })
            ]
        });
        bleno.setServices([echoService]);
    }
});