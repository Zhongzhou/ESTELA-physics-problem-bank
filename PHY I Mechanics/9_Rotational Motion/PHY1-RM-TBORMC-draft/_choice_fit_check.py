"""Check whether the q1 choice pattern yields distinct choices for every TBOR item."""
import math
from fractions import Fraction

ROWS = """
0,1/8,3/4,4,8,F
0,1/8,1,8,16,W_rod
0,1/4,3/4,16,32,W_block
0,1/4,1,32,4,F
0,3/4,1/4,4,8,W_rod
0,3/4,1,8,16,W_block
0,7/8,1/4,16,32,F
0,7/8,1,32,4,W_rod
0,1,1/4,4,8,W_block
0,1,3/4,8,16,F
1/4,0,3/4,16,32,W_rod
1/4,0,1,4,32,W_block
1/4,3/4,1,4,8,F
1/4,7/8,1,8,16,W_rod
1/4,1,3/4,16,32,W_block
3/4,0,1/4,32,4,F
3/4,1/8,0,4,8,W_rod
3/4,1/4,0,8,16,W_block
3/4,1,0,16,32,F
3/4,1,1/4,4,32,W_rod
1,0,1/4,4,8,W_block
1,0,3/4,8,16,F
1,1/8,0,16,32,W_rod
1,1/8,3/4,32,4,W_block
1,1/4,0,4,8,F
1,1/4,3/4,8,16,W_rod
1,3/4,0,16,32,W_block
1,3/4,1/4,32,4,F
1,7/8,0,4,8,W_rod
1,7/8,1/4,8,16,W_block
""".strip().splitlines()

SIN = math.sqrt(3) / 2
COS = 0.5


def rint(x):
    if abs(x) < 1e-9:
        return 0
    return int(math.floor(abs(x) + 0.5)) * (1 if x >= 0 else -1)


def val(unk, perp, ab, ar, arm_f, Wb, Wr, F, drop_rod=False):
    if drop_rod and unk == "W_rod":
        return None
    Wr_ = 0 if drop_rod else Wr
    if unk == "F":
        num = float(Wb * ab + Wr_ * ar)
        den = perp * float(arm_f)
        return num / den
    if unk == "W_rod":
        num = (float(F) * perp) * float(arm_f) - float(Wb * ab)
        return num / float(ar)
    num = (float(F) * perp) * float(arm_f) - float(Wr_ * ar)
    return num / float(ab)


def main():
    header = (
        f"{'q':>3} {'unk':<8} {'sides':<5} "
        f"{'correct':>8} {'noang':>8} {'sincos':>8} {'opp':>8} "
        f"{'nobeam':>8} {'fullL':>8} {'farend':>8} {'addW':>8}"
    )
    print(header)
    for i, line in enumerate(ROWS, 1):
        ps, bs, fs, Wbs, Wrs, unk = line.split(",")
        p, b, f = Fraction(ps), Fraction(bs), Fraction(fs)
        Wb, Wr = Fraction(Wbs), Fraction(Wrs)
        arm_b = b - p
        arm_r = Fraction(1, 2) - p
        arm_f = f - p
        F = (Wb * arm_b + Wr * arm_r) / (Fraction(1, 2) * arm_f)
        same = (arm_b > 0) == (arm_r > 0)
        arm_full = (1 if arm_r > 0 else -1) * Fraction(1)
        arm_far = (1 - p) if arm_r > 0 else (0 - p)

        correct = val(unk, COS, arm_b, arm_r, arm_f, Wb, Wr, F)
        noang = val(unk, 1.0, arm_b, arm_r, arm_f, Wb, Wr, F)
        sincos = val(unk, SIN, arm_b, arm_r, arm_f, Wb, Wr, F)
        oppsign = val(unk, COS, -arm_b, arm_r, arm_f, Wb, Wr, F)
        nobeam = val(unk, COS, arm_b, arm_r, arm_f, Wb, Wr, F, drop_rod=True)
        fulllen = val(unk, COS, arm_b, arm_full, arm_f, Wb, Wr, F)
        farend = val(unk, COS, arm_b, arm_far, arm_f, Wb, Wr, F)
        addW = float(Wb + Wr) if unk == "F" else None

        def fmt(x):
            if x is None:
                return "     n/a"
            return f"{rint(x):8d}"

        canon = {
            "correct": correct,
            "noang": noang,
            "sincos": sincos,
            "opp": None if oppsign is None else abs(oppsign),
            "nobeam": None if nobeam is None else abs(nobeam),
            "full": None if fulllen is None else abs(fulllen),
            "add": addW,
        }
        rounded = {}
        for k, v in canon.items():
            if v is None:
                continue
            rounded.setdefault(rint(v), []).append(k)
        collisions = {n: ks for n, ks in rounded.items() if len(ks) > 1}
        neg = [
            k
            for k, v in [
                ("noang", noang),
                ("sincos", sincos),
                ("opp", oppsign),
                ("nobeam", nobeam),
                ("full", fulllen),
                ("far", farend),
            ]
            if v is not None and v < -1e-6
        ]
        notes = []
        if not same:
            notes.append("OPPOSITE-SIDES")
        if p not in (0, 1):
            notes.append("PIVOT-MID")
        if collisions:
            notes.append("COLLIDE " + str(collisions))
        if neg:
            notes.append("NEG " + ",".join(neg))
        if addW is None:
            notes.append("ADD-UNDEF")
        if nobeam is None:
            notes.append("NOBEAM-UNDEF")
        print(
            f"{i:3d} {unk:<8} {('SAME' if same else 'OPP'):<5} "
            f"{fmt(correct)} {fmt(noang)} {fmt(sincos)} {fmt(abs(oppsign))} "
            f"{fmt(None if nobeam is None else abs(nobeam))} "
            f"{fmt(None if fulllen is None else abs(fulllen))} "
            f"{fmt(None if farend is None else abs(farend))} {fmt(addW)}"
        )
        print(
            "    raw "
            f"c={correct:.4f} na={noang:.4f} sc={sincos:.4f} "
            f"opp={oppsign:.4f} "
            f"nb={'n/a' if nobeam is None else f'{nobeam:.4f}'} "
            f"full={fulllen:.4f} far={farend:.4f} "
            f"F={float(F):.4f} arms b={float(arm_b):.4f} r={float(arm_r):.4f} f={float(arm_f):.4f}"
        )
        if notes:
            print("   ", "; ".join(notes))


if __name__ == "__main__":
    main()
