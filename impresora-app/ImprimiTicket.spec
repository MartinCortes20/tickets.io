# Uso: .venv/bin/pyinstaller ImprimiTicket.spec   (genera dist/ImprimiTicket.app)
from PyInstaller.utils.hooks import collect_data_files
a = Analysis(
    ['MenuBarApp.py'],
    binaries=[('/opt/homebrew/lib/libusb-1.0.dylib', '.')],  # Intel: /usr/local/lib/...
    datas=[('../index.html', '.')] + collect_data_files('escpos'),
    hiddenimports=['servidor', 'usb.backend.libusb1', 'escpos.printer'],
)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='ImprimiTicket', console=False)
coll = COLLECT(exe, a.binaries, a.datas, name='ImprimiTicket')
app = BUNDLE(coll, name='ImprimiTicket.app', info_plist={'LSUIElement': True})
