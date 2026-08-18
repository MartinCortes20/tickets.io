# -*- coding: utf-8 -*-
from escpos.printer import Usb

SEP = '================================'
p = Usb(0x0416, 0x5011, profile="TM-T88II")

# --- ENCABEZADO ---
p.set(align='left', bold=False)
p.text(SEP + "\n")

p.set(align='center', bold=True)
p.text("COCINA LALITA\n")

p.set(align='center', bold=False)
p.text("MUYUGUARDA 15\n")
p.text("SAN BERNARDINO\n")

p.set(align='left', bold=False)
p.text(SEP + "\n")

p.set(align='center', bold=True)
p.text("!GRACIAS POR SU VISITA!\n")

p.set(align='left', bold=False)
p.text(SEP + "\n")

# --- DATOS DE ORDEN ---
p.set(align='left', bold=False)
p.text("ORDEN DE MESA\n")
p.text(f"FOLIO:{'0':>26}\n")
p.text(f"FECHA:{'13/05/2026':>26}\n")
p.text(f"HORA:{'11:45 AM':>27}\n")
p.text(f"MESA:{'1':>27}\n")
p.text(f"PERSONAS:{'2':>23}\n")
p.text(f"ORDEN:{'PARA COMER':>26}\n")
p.text(f"MESERO:{'MARGARITA':>25}\n")

p.set(align='left', bold=False)
p.text(SEP + "\n")

# --- PRODUCTOS ---
p.set(align='left', bold=True)
p.text("CANT ARTICULO     P.UNIT   TOTAL\n")

p.set(align='left', bold=False)
p.text(SEP + "\n")

productos = [
    (2, "COMIDA CORRIDA", 105.00, 210.00),
    (3, "REFRESCOS",       30.00,  90.00),
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

p.set(align='left', bold=False)
p.text("TOTAL ARTICULOS: 5\n")

p.set(align='left', bold=False)
p.text(SEP + "\n")

# --- TOTALES ---
p.set(align='left', bold=False)
p.text(f"SUBTOTAL:{'$300.00':>23}\n")
p.text(f"IVA (16%):{'$0.00':>22}\n")

p.set(align='left', bold=True)
p.text(f"TOTAL:{'$300.00':>26}\n")

p.set(align='left', bold=False)
p.text(SEP + "\n")

p.set(align='left', bold=False)
p.text("FORMA DE PAGO: EFECTIVO\n")
p.text(f"MONTO RECIBIDO:{'$300.00':>17}\n")
p.text(f"CAMBIO:{'$0.00':>25}\n")

p.set(align='left', bold=False)
p.text(SEP + "\n")

p.set(align='center', bold=True)
p.text("!GRACIAS POR SU VISITA!\n")

p.set(align='center', bold=False)
p.text("LOS ESPERAMOS PRONTO\n")

p.set(align='left', bold=False)
p.text(SEP + "\n")

p.text("TERMINAL: 0\n")

p.set(align='left', bold=False)
p.text(SEP + "\n")

p.set(align='center', bold=True)
p.text("FACTURA SOLICITALA AL\n")
p.text("MOMENTO DEL PAGO!\n")

p.set(align='left', bold=False)
p.text(SEP + "\n")

p.ln(3)
p.cut()
