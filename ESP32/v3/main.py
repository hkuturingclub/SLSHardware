import urequests
import ujson
from machine import ADC
from utime import time
from utime import sleep

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    print("Attempting to connect")
    if not sta_if.isconnected():
        sta_if.active(True)
        
        #Provide the wifi SSID and password here
        sta_if.connect("Wi-Fi.HK via HKU")
        
        while not sta_if.isconnected():
            pass
    print("connected")


def getMagic():
    import urequests_mod

    r = urequests_mod.get('http://msftconnect.com')

    #This is the position where the redirect URL starts. It will be required to initiate the authentication
    url_start = r.text.find('http://')

    #This gives us the position of the magic URL
    magic_start=r.text.find('fgtauth') + 8
    magic_end=magic_start + 16
    magic=r.text[magic_start:magic_end]

    #The extracted URL
    url = r.text[url_start: magic_end]

    r.close()
    return url, magic


"""
    Using the redirect URL and magic value, this function will initiate authentication
    and then complete the authentication, thus connecting to the internet.
"""
def connectWithMagic(url, magic):
    st = "4Tredir=http%3A%2F%2Fmsftconnect.com%2F&magic="+str(magic)+"&username=wifi&password=wifi"
    try:
        #Initiate the authentication by sending GET request to the redirected URL
        print("Logging in to the internet")
        r = urequests.get(url)
        r.close()

        #Complete the authentication by sending the form data to the required URL
        r = urequests.post(url[:url.find("?")], data=st, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        r.close()

    except IndexError:
        print("Already connected to the internet")

    except ValueError:
        print("The device was already logged in. Therefore, there was no URL")


def sendData(x):
    print(x)
    res = urequests.post('http://chisunsls.azurewebsites.net/api/laundry_status', json=x, headers={'Content-Type': 'application/json'})
    print(res.text)


def main():
    do_connect()
    url, magic = getMagic()
    connectWithMagic(url, magic)

    #Test webhook when connected to the internet
    r = urequests.get("http://webhook.site/510a5c99-b9f8-4a23-aabb-30b293a6aa59")


    adc = ADC(0)
    t = time()
    while(True):
        if time() - t > 3:
            data = {
                "status": adc.read()
            }
            sendData(data)
            t = time()
    

main()