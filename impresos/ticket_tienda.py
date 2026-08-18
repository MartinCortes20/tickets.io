# -*- coding: utf-8 -*-
from escpos.printer import Usb

SEP = '--------------------------------'
p = Usb(0x0416, 0x5011, profile="TM-T88II")

# --- ENCABEZADO ---
p.set(align='center', bold=True)
p.text("LORENZO SERRANO ALONSO\n")

p.set(align='center', bold=False)
p.text("CREM. Y SALCHICHONERIA\n")
p.text("LOS CHINOS\n")
p.text("PLAN DE SAN LUIS #1\n")
p.text("TEL.56412086\n")
p.text("SAN LORENZO LA CEBADA\n")
p.text("CP.16035\n")
p.text("XOCHIMILCO, CDMX\n")
p.text("RFC. SEAL700810D38\n")
p.text("\n")

# --- FECHA Y HORA ---
p.set(align='center', bold=False)
p.text("16/07/2026 02:34 PM\n")
p.text("\n")

# --- DATOS DE VENTA ---
p.set(align='left', bold=False)
p.text(f"CAJERO:{'VALERIA':>25}\n")
p.text(f"TURNO #{'9078':>24}\n")
p.text(f"FOLIO:{'613557':>26}\n")
p.text("\n")

# --- PRODUCTOS ---
p.set(align='left', bold=True)
p.text("CANT ARTICULO     P.UNIT   TOTAL\n")

p.set(align='left', bold=False)
p.text(SEP + "\n")

productos = [
    (1, "BOTANAS Y SEMILL", 14.00, 14.00),
    (1, "CHURRITO CHILEYL", 18.00, 18.00),
    (1, "SABRITAS ADOBADA", 20.00, 20.00),
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
            
    if len(line) > 32:
        line = line[:32]
        
    return line

for cant, desc, punit, total in productos:
    linea = format_product_line(cant, desc, punit, total)
    p.text(linea + "\n")

p.set(align='left', bold=False)
p.text(SEP + "\n")

# --- TOTALES ---
p.set(align='left', bold=False)
p.text("NO. DE ARTICULOS: 3\n")
p.text(f"TOTAL:{'$52.00':>26}\n")
p.text(f"PAGO CON:{'$52.00':>23}\n")
p.text(f"SU CAMBIO:{'$0.00':>22}\n")
p.text("\n")

# --- PIE DE TICKET ---
p.set(align='center', bold=False)
p.text("REGIMEN DE INCORPORACION\n")
p.text("FISCAL\n")
p.text("WWW.ELEVENTA.COM\n")

p.ln(3)
p.cut()
