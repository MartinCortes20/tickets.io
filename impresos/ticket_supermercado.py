# -*- coding: utf-8 -*-
from escpos.printer import Usb
from PIL import Image

SEP = '=' * 32  # 58mm = 32 caracteres

p = Usb(0x0416, 0x5011, profile='TM-T88II')

try:
    p.charcode("CP850")
except:
    try:
        p.charcode("CP437")
    except:
        pass

# --- LOGO ---
p.set(align='center')
logo = Image.open("logoSoriana.png").convert("RGB")
MAX_W = 384
if logo.width > MAX_W:
    ratio = MAX_W / logo.width
    logo = logo.resize((MAX_W, int(logo.height * ratio)), Image.LANCZOS)
p.image(logo)

# --- ENCABEZADO (fuente pequeña) ---
p.set(align='center', bold=True, width=2, height=2, font='b')
p.text("TACUBAYA\n")
p.set(align='center', bold=False, width=1, height=1, font='b')
p.text("TIENDAS SORIANA, S.A. DE C.V.\n")
p.text("REGIMEN GENERAL DE LEY\n")
p.text("GRAL JOSE MORAN 3\n")
p.text("SAN MIGUEL CHAPULTEPEC 11850\n")
p.text("TEL: 55 7450 1510\n")
p.text("09/05/2026  09:39 PM\n")
p.text(SEP + '\n')

# --- PRODUCTOS ---
# Con font='b' caben ~42 chars en 58mm
# CT(2) + sp + ARTICULO(14) + sp + P.U(6) + sp + TOTAL(6) = 32
p.set(align='left', bold=True, font='b')
p.text("CT ARTICULO          P.U    TOTAL\n")
p.set(align='left', bold=False, font='b')
p.text(SEP + '\n')

productos = [
    (15, "AGUA BONAFO",    8.30,  124.50),
    ( 1, "DORITOS NACHOS", 59.90,  59.90),
    ( 1, "PAKETAXO QUEXO", 90.90,  90.90),
    ( 1, "RANCHERITOS",    62.90,  62.90),
    ( 3, "COCA COLA",     160.00, 480.00),
    ( 2, "DELAWARE",       21.00,  42.00),
    ( 1, "FANTA NARANJA",  21.00,  21.00),
    ( 2, "SIDRAL",         21.00,  42.00),
    ( 1, "SPRITE",         21.00,  21.00),
]

for cant, desc, punit, total in productos:
    linea = f"{cant:<2} {desc:<14} {punit:>6.2f} {total:>6.2f}"
    p.text(linea + "\n")

p.text(SEP + '\n')

# --- TOTALES ---
p.set(align='left', bold=True, font='b')
p.text("TOTAL:               $944.20\n")
p.set(align='left', bold=False, font='b')
p.text("EFECTIVO             $944.20\n")
p.text(SEP + '\n')

# --- PIE ---
p.set(align='center', bold=False, font='b')
p.text("ARTICULOS: 27\n")
p.text(SEP + '\n')
p.set(align='center', bold=True, font='b')
p.text("HOY TE AHORRASTE: -$104.00\n")
p.set(align='left', bold=False, font='b')
p.text("Puntos acumulados: 12\n")
p.text(SEP + '\n')
p.set(align='center', bold=False, font='b')
p.text("GRACIAS POR TU COMPRA!\n")
p.text("WWW.SORIANA.COM\n")
p.set(align='left', bold=False, font='b')
p.text("Le Atendio:\n")
p.text("  REGINA GONZALEZ\n")
p.text(SEP + '\n')
p.set(align='center', bold=True, font='b')
p.text("SORIANA: CALIDAD Y AHORRO\n")
p.set(align='center', bold=False, font='b')
p.text("VERSION: 4.41.0.0\n")
p.text(SEP + '\n')
p.set(align='center', bold=False, font='b')
p.text("||||| 7501234567890 |||||\n")
p.text("7501234567890\n")

p.ln(3)
p.cut()