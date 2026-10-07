# Reglas para tickets térmicos (32 columnas)

Al crear o editar cualquier ticket `.py`:

1. Cada `p.text(...)` termina con `\n` real: `p.text(SEP + "\n")`. Nunca un salto de línea literal dentro del string.
2. Nunca `\\n` (doble backslash). Correcto: `p.text("TEXTO\n")`.
3. Ninguna línea puede pasar de 32 caracteres (incluye f-strings con `:>N`: etiqueta + N <= 32).
4. No imprimir `TERMINAL:` si no tiene valor.
5. Antes de dar por terminado: `python3 check_ticket.py <archivo>`. Debe imprimir cero avisos.
