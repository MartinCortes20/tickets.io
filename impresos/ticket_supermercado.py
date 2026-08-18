# -*- coding: utf-8 -*-
from escpos.printer import Usb
from PIL import Image

SEP = '================================'
p = Usb(0x0416, 0x5011, profile="TM-T88II")

# --- LOGO ---
p.set(align='center', bold=False)
try:
    logo = Image.open("logoSoriana.png").convert("RGB")
    MAX_W = 384
    if logo.width > MAX_W:
        ratio = MAX_W / logo.width
        logo = logo.resize((MAX_W, int(logo.height * ratio)), Image.LANCZOS)
    p.image(logo)
except:
    pass

# --- ENCABEZADO ---
p.set(align='center', bold=True)
p.text("TACUBAYA\n")

p.set(align='center', bold=False)
p.text("TIENDAS SORIANA,\n")
p.text("S.A. DE C.V.\n")
p.text("REGIMEN GENERAL DE LEY\n")
p.text("GRAL JOSE MORAN 3\n")
p.text("SAN MIGUEL CHAPULTEPEC\n")
p.text("11850\n")
p.text("TEL: 55 7450 1510\n")
p.text("09/05/2026  09:39 PM\n")

p.set(align='left', bold=False)
p.text(SEP + "\n")

# --- PRODUCTOS ---
p.set(align='left', bold=True)
p.text("CANT ARTICULO     P.UNIT   TOTAL\n")

p.set(align='left', bold=False)
p.text(SEP + "\n")

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

def format_product_line(cant, desc, punit, total):
    cant_str = str(cant)
    desc_str = str(desc)
    punit_str = f"{punit:.2f}" if isinstance(punit, (int, float)) else str(punit)
    total_str = f"{total:.2f}" if isinstance(total, (int, float)) else str(total)
    
    desc_cropped = desc_str[:13]
    line = f"{cant_str:<4}{desc_cropped:<13}{punit_str:>6}  {total_str:>7}"
    
    while len(line) > 32:
        if "  " in line:
            line = line.replace("  ", " ", 1)
        else:
            desc_cropped = desc_cropped[:-1]
            line = f"{cant_str:<4}{desc_cropped:<13}{punit_str:>6} {total_str:>7}"
            
    # Final assertion to ensure safety
    if len(line) > 32:
        line = line[:32]
        
    return line

for cant, desc, punit, total in productos:
    linea = format_product_line(cant, desc, punit, total)
    p.text(linea + "\n")

p.set(align='left', bold=False)
p.text(SEP + "\n")

# --- TOTALES ---
p.set(align='left', bold=True)
p.text(f"TOTAL:{'$944.20':>26}\n")

p.set(align='left', bold=False)
p.text(f"EFECTIVO:{'$944.20':>23}\n")
p.text(SEP + "\n")

p.set(align='center', bold=False)
p.text("ARTICULOS: 27\n")

p.set(align='left', bold=False)
p.text(SEP + "\n")

p.set(align='center', bold=True)
p.text("HOY TE AHORRASTE: -$104.00\n")

p.set(align='left', bold=False)
p.text("Puntos acumulados: 12\n")
p.text(SEP + "\n")

p.set(align='center', bold=False)
p.text("GRACIAS POR TU COMPRA!\n")
p.text("WWW.SORIANA.COM\n")

p.set(align='left', bold=False)
p.text("Le Atendio:\n")
p.text("  REGINA GONZALEZ\n")
p.text(SEP + "\n")

p.set(align='center', bold=True)
p.text("SORIANA: CALIDAD Y AHORRO\n")

p.set(align='center', bold=False)
p.text("VERSION: 4.41.0.0\n")
p.text(SEP + "\n")

p.set(align='center', bold=False)
p.text("||||| 7501234567890 |||||\n")
p.text("7501234567890\n")

p.ln(3)
p.cut()