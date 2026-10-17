# Uso:  pip install py2app rumps python-escpos pyusb && brew install libusb
#       python3 setup.py py2app        (genera dist/MenuBarApp.app)
#       python3 setup.py py2app -A     (modo alias, para probar rápido)
from setuptools import setup

setup(
    name='ImprimiTicket',
    app=['MenuBarApp.py'],
    options={'py2app': {
        'packages': ['rumps', 'escpos', 'usb', 'WebKit'],
        'resources': ['../index.html'],
        'includes': ['servidor'],
        'frameworks': ['/opt/homebrew/lib/libusb-1.0.dylib'],  # Intel: /usr/local/lib/...
        'plist': {
            'CFBundleName': 'ImprimiTicket',
            'LSUIElement': True,  # solo menu bar, sin ícono en el Dock
        },
    }},
    setup_requires=['py2app'],
)
