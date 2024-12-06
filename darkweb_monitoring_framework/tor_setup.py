import requests
from stem import Signal
from stem.control import Controller
def get_tor_session():
	session = requests.Session()
	session.proxies = {
		'http': 'socks5h://127.0.0.1:9050',
		'https': 'socks5h://127.0.0.1:9050'
	}
	return session

def get_new_identity():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()  # Use this if using cookie authentication
        controller.signal(Signal.NEWNYM)
