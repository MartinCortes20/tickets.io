# -*- coding: utf-8 -*-
import functools
import threading
from http.server import HTTPServer

import os
import shlex
import subprocess

import objc
import rumps
from AppKit import NSAlert, NSOpenPanel, NSApp, NSBackingStoreBuffered, NSMakeRect, NSWindow
from Foundation import NSObject, NSURL
from WebKit import WKWebView, WKWebViewConfiguration
import usb.backend.libusb1
import usb.core



def _libusb():
    import glob, os, sys
    res = os.environ.get('RESOURCEPATH', '')
    for pat in (res + '/../Frameworks/libusb*.dylib', '/opt/homebrew/lib/libusb-1.0.dylib', '/usr/local/lib/libusb-1.0.dylib'):
        m = glob.glob(pat)
        if m:
            return m[0]


_be = usb.backend.libusb1.get_backend(find_library=lambda _: _libusb())
usb.core.find = functools.partial(usb.core.find, backend=_be)

import servidor  # noqa: E402  (debe ir después de parchear usb.core.find)


class UI(NSObject):
    # WKWebView ignora alert() si no hay delegate que lo muestre.
    def webView_runJavaScriptAlertPanelWithMessage_initiatedByFrame_completionHandler_(self, wv, msg, frame, done):
        a = NSAlert.alloc().init()
        a.setMessageText_(msg)
        a.runModal()
        done()


class App(rumps.App):
    def __init__(self):
        super().__init__('🖨 Impresora', quit_button='Salir')
        self.httpd = None
        self.estado = rumps.MenuItem('')
        self.iniciar = rumps.MenuItem('Iniciar', callback=self.on_iniciar)
        self.detener = rumps.MenuItem('Detener', callback=self.on_detener)
        self.menu = [rumps.MenuItem('Abrir tickets', callback=self.on_abrir), rumps.MenuItem('Imprimir archivo .py', callback=self.on_archivo), None, self.estado, None, self.iniciar, self.detener]
        self.win = None
        self.on_iniciar(None)

    def on_abrir(self, _):
        if not self.win:
            self.ui = UI.alloc().init()
            wv = WKWebView.alloc().initWithFrame_configuration_(NSMakeRect(0, 0, 1000, 800), WKWebViewConfiguration.alloc().init())
            wv.setUIDelegate_(self.ui)
            html = os.path.join(os.environ.get('RESOURCEPATH', '..'), 'index.html')
            u = NSURL.fileURLWithPath_(html)
            wv.loadFileURL_allowingReadAccessToURL_(u, u.URLByDeletingLastPathComponent())
            self.win = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(NSMakeRect(0, 0, 1000, 800), 15, NSBackingStoreBuffered, False)
            self.win.setTitle_('ImprimiTicket')
            self.win.setContentView_(wv)
            self.win.setReleasedWhenClosed_(False)
            self.win.center()
        self.win.makeKeyAndOrderFront_(None)
        NSApp.activateIgnoringOtherApps_(True)

    def on_archivo(self, _):
        NSApp.activateIgnoringOtherApps_(True)
        panel = NSOpenPanel.openPanel()
        panel.setAllowedFileTypes_(['py'])
        if not panel.runModal():
            return
        path = panel.URL().path()
        # Equivale a `sudo python3 archivo.py`; osascript pide la contraseña en una ventana.
        cmd = 'PATH=/opt/homebrew/bin:/usr/local/bin:$PATH sudo python3 ' + shlex.quote(path)
        script = 'do shell script "%s" with administrator privileges' % cmd.replace('\\', '\\\\').replace('"', '\\"')
        r = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if r.returncode:
            rumps.alert('Error al imprimir', r.stderr.strip()[-500:])
        else:
            rumps.notification('ImprimiTicket', '', 'Ticket enviado')

    def refrescar(self):
        on = self.httpd is not None
        self.estado.title = 'Servidor: corriendo ✅' if on else 'Servidor: detenido ❌'
        self.iniciar.set_callback(None if on else self.on_iniciar)
        self.detener.set_callback(self.on_detener if on else None)

    def on_iniciar(self, _):
        if not self.httpd:
            try:
                self.httpd = HTTPServer(('localhost', 8765), servidor.H)
            except OSError as e:
                rumps.alert('No se pudo iniciar', str(e))
            else:
                threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.refrescar()

    def on_detener(self, _):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            self.httpd = None
        self.refrescar()


if __name__ == '__main__':
    App().run()
