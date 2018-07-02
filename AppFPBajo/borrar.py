import SchemDraw as schem
import SchemDraw.elements as e
d = schem.Drawing()
V1 = d.add(e.SOURCE_V, label='10V')
d.add(e.RES, d='right', label='100K$\Omega$')
d.add(e.CAP, d='down', botlabel='0.1$\mu$F')
d.add(e.LINE, to=V1.start)
d.add(e.GND)
d.draw()
