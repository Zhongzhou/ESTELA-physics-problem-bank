"""Generated calculation functions. Python writes this file."""

import math
from decimal import Decimal, ROUND_HALF_UP

ROUNDING_DECIMAL = 2

def round_step(value, places):
    quantum = Decimal(1).scaleb(-places)
    return float(Decimal(str(value)).quantize(quantum, rounding=ROUND_HALF_UP))


def solve_eqset_01(F_net, m, r):
    # F_{\mathrm{net}} = \frac{m v^{2}}{r}
    # T = \frac{2 \pi r}{v}
    v = round_step(math.sqrt(F_net*r/m), 2)
    T = round_step(2*math.pi*r/v, 2)
    return {'v': v, 'T': T}


def solve_eqset_02(F_net, m, r):
    # F_{\mathrm{net}} = \frac{m v^{2}}{r}
    # f = \frac{v}{2 \pi r}
    v = round_step(math.sqrt(F_net*r/m), 2)
    f = round_step((1/2)*v/(math.pi*r), 2)
    return {'v': v, 'f': f}
