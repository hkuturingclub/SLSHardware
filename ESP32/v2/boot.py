def connect():
    magic = get_magic()
    connect_iphone()
    send_connect_request(magic)

def connect_iphone():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if sta_if.isconnected():
        sta_if.disconnect()
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect("Waqas' iPhone", "waqas1234")
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def send_connect_request(magic):
    import urequests
    request = "4Tredir=http%3A%2F%2Fmsftconnect.com%2F&magic="+magic+"&username=wifi&password=wifi"
    r = urequests.post("http://10.99.180.41:1000/fgtauth", data=request, headers={"content-type":"application/x-www-form-urlencoded"})

def get_magic():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if sta_if.isconnected():
        sta_if.disconnect()
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect("Wi-Fi.HK via HKU")
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

    import urequests_mod
    r = urequests_mod.get('http://msftconnect.com')
    magic_start=r.text.find('fgtauth') + 8
    magic_end=magic_start + 16
    magic=r.text[magic_start:magic_end]
    r.close()
    return magic

def no_debug():
    import esp
    # this can be run from the REPL as well
    esp.osdebug(None)
