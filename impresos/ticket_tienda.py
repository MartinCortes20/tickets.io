# -*- coding: utf-8 -*-
from escpos.printer import Usb

SEP = '-' * 32  # 58mm = 32 caracteres

p = Usb(0x0416, 0x5011, profile='TM-T88II')

try:
    p.charcode("CP850")
except:
    try:
        p.charcode("CP437")
    except:
        pass

def center(s, w=32):
    s = s[:w]
    spaces = (w - len(s)) // 2
    return ' ' * spaces + s + ' ' * (w - len(s) - spaces)

def pad_lr(left, right, w=32):
    left = left[:w - len(right) - 1]
    spaces = w - len(left) - len(right)
    return left + ' ' * spaces + right

# --- ENCABEZADO ---
p.set(align='center', bold=True)
p.text("LORENZO SERRANO ALONSO\n")
p.set(align='center', bold=False)
p.text("CREM. Y SALCHICHONERIA LOS CHINOS\n")
p.text("PLAN DE SAN LUIS #1 TEL.56412086\n")
p.text("SAN LORENZO LA CEBADA,CP.16035\n")
p.text("XOCHIMILCO,CDMX RFC. SEAL700810D38\n")
p.text("\n")

# --- FECHA Y HORA ---
p.text(center("16/07/2026 02:34 PM") + "\n")
p.text("\n")

# --- DATOS DE VENTA ---
p.text(pad_lr("CAJERO:", "VALERIA") + "\n")
p.text(pad_lr("TURNO #", "9078") + "\n")
p.text(pad_lr("FOLIO:", "613557") + "\n")
p.text("\n")

# --- CABECERA TABLA ---
# CANT. DESCRIPCION        IMPORTE (total 32 chars)
p.text("CANT. DESCRIPCION        IMPORTE\n")
p.text(SEP + "\n")

# --- PRODUCTOS ---
# Formato: CANT. (2 chars) + "  " + DESC (20 chars max) + " " + IMPORTE (7 chars max)
# Ejemplo: "1  BOTANAS Y SEMILLAS      $14.00"
productos = [
    (1, "BOTANAS Y SEMILLAS", 14.00),
    (1, "CHURRITO CHILEYLIMON", 18.00),
    (1, "SABRITAS ADOBADAS CHIC", 20.00),
]

for cant, desc, importe in productos:
    imp_str = f"${importe:.2f}"
    # Limitar descripción a 20 caracteres para asegurar alineación exacta
    desc_cropped = desc[:20]
    # cant (2 chars left) + "  " (2 chars) + desc (20 chars left) + " " + imp_str (7 chars right)
    # Total = 2 + 2 + 20 + 1 + 7 = 32
    linea = f"{cant:<2}  {desc_cropped:<20} {imp_str:>7}"
    p.text(linea + "\n")

p.text(SEP + "\n")

# --- TOTALES ---
p.text("NO. DE ARTICULOS: 3\n")
p.text(pad_lr("TOTAL:", "$52.00") + "\n")
p.text(pad_lr("PAGO CON:", "$52.00") + "\n")
p.text(pad_lr("SU CAMBIO:", "$0.00") + "\n")
p.text("\n")

# --- PIE DE TICKET ---
p.set(align='center')
p.text("REGIMEN DE INCORPORACION FISCAL\n")
p.text("WWW.ELEVENTA.COM\n")

p.ln(3)
p.cut()
