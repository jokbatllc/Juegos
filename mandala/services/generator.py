import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from django.conf import settings

# SVG helpers --------------------------------------------------------------


def svg_header(w: int, h: int, bg: str | None = None) -> str:
    bg_rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" stroke-linecap="round">{bg_rect}'
    )


def svg_footer() -> str:
    return "</svg>"


def group_open(transform: str = "", opacity: float | None = None) -> str:
    t = f' transform="{transform}"' if transform else ""
    o = f' opacity="{opacity}"' if opacity is not None else ""
    return f"<g{t}{o}>"


def group_close() -> str:
    return "</g>"


def path(d: str, stroke="#000", fill="none", sw=1.5) -> str:
    return f'<path d="{d}" stroke="{stroke}" fill="{fill}" stroke-width="{sw}"/>'


def circle(cx, cy, r, stroke="#000", fill="none", sw=1) -> str:
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{stroke}" fill="{fill}" stroke-width="{sw}"/>'


def dot(cx, cy, r=1.2, fill="#000") -> str:
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="none"/>'


# Geometry -----------------------------------------------------------------


def rotate_point(x: float, y: float, ang: float) -> Tuple[float, float]:
    ca, sa = math.cos(ang), math.sin(ang)
    return (x * ca - y * sa, x * sa + y * ca)


def pol2cart(r: float, theta: float) -> Tuple[float, float]:
    return (r * math.cos(theta), r * math.sin(theta))


# Motifs (Bézier petals/leaves, arcs, stars, etc.) -------------------------


def bezier_petal(r_in: float, r_out: float, w: float) -> str:
    x0, y0 = r_in, 0
    x3, y3 = r_out, 0
    c1 = (x0 + (r_out - r_in) * 0.25, w)
    c2 = (x3 - (r_out - r_in) * 0.25, w * 0.6)
    c3 = (x3 - (r_out - r_in) * 0.25, -w * 0.6)
    c4 = (x0 + (r_out - r_in) * 0.25, -w)
    return (
        f"M {x0:.3f} {y0:.3f} "
        f"C {c1[0]:.3f} {c1[1]:.3f}, {c2[0]:.3f} {c2[1]:.3f}, {x3:.3f} {y3:.3f} "
        f"C {c3[0]:.3f} {c3[1]:.3f}, {c4[0]:.3f} {c4[1]:.3f}, {x0:.3f} {y0:.3f} Z"
    )


def leaf(r_in: float, r_out: float, w: float) -> str:
    return bezier_petal(r_in, r_out, w * 0.75)


def arc_ring(r: float, a0: float, a1: float) -> str:
    steps = max(8, int((a1 - a0) / (math.pi / 48)))
    pts = [pol2cart(r, a0 + i * (a1 - a0) / steps) for i in range(steps + 1)]
    d = f"M {pts[0][0]:.3f} {pts[0][1]:.3f} " + " ".join(
        f"L {x:.3f} {y:.3f}" for (x, y) in pts[1:]
    )
    return d


def star(r_in: float, r_out: float, tips: int = 5) -> str:
    pts = []
    for i in range(tips * 2):
        ang = i * math.pi / tips
        r = r_out if i % 2 == 0 else r_in
        pts.append(pol2cart(r, ang))
    d = (
        f"M {pts[0][0]:.3f} {pts[0][1]:.3f} "
        + " ".join(f"L {x:.3f} {y:.3f}" for x, y in pts[1:])
        + " Z"
    )
    return d


def kfold(d: str, k: int, stroke="#000", fill="none", sw=1.2) -> str:
    out = []
    for i in range(k):
        ang = (2 * math.pi / k) * i
        out.append(
            f'<g transform="rotate({math.degrees(ang):.3f})">{path(d, stroke, fill, sw)}</g>'
        )
    return "".join(out)


# Parameters ----------------------------------------------------------------


@dataclass
class MandalaParams:
    size: int = 2048
    margin: int = 80
    symmetry: int = 12
    rings: int = 7
    complexity: int = 5
    stroke: str = "#000"
    bg: str | None = None
    seed: int | None = None


# Generator -----------------------------------------------------------------


def generate_mandala_svg(p: MandalaParams) -> str:
    if p.seed is not None:
        random.seed(p.seed)

    w = h = p.size
    cx = cy = p.size / 2
    R = (p.size / 2) - p.margin

    svg = [svg_header(w, h, p.bg), group_open(transform=f"translate({cx},{cy})")]

    guide_count = max(3, p.rings // 2)
    for i in range(guide_count):
        r = R * (0.2 + 0.75 * i / max(1, guide_count - 1))
        svg.append(circle(0, 0, r, stroke=p.stroke, fill="none", sw=0.6))

    for ring_idx in range(1, p.rings + 1):
        progress = ring_idx / (p.rings + 1)
        r_in = R * (0.04 + 0.9 * (ring_idx - 1) / (p.rings + 0.5))
        r_out = R * (0.06 + 0.9 * ring_idx / (p.rings + 0.3))
        sw = 0.8 + 1.2 * (1 - progress)

        ring_group = [group_open(opacity=0.98)]

        choice = random.random()
        motif_count = p.symmetry

        if choice < 0.30:
            base_w = (r_out - r_in) * (0.55 + 0.15 * random.random())
            d0 = bezier_petal(r_in, r_out, base_w)
            ring_group.append(
                kfold(d0, p.symmetry, stroke=p.stroke, fill="none", sw=sw)
            )
        elif choice < 0.55:
            d0 = leaf(r_in, r_out, (r_out - r_in) * (0.5 + 0.2 * random.random()))
            ring_group.append(
                kfold(d0, p.symmetry, stroke=p.stroke, fill="none", sw=sw)
            )
            d1 = arc_ring((r_in + r_out) * 0.5, 0, 2 * math.pi / p.symmetry - 0.06)
            ring_group.append(
                kfold(d1, p.symmetry, stroke=p.stroke, fill="none", sw=sw * 0.7)
            )
        elif choice < 0.75:
            tips = 5 if p.symmetry % 2 == 0 else 6
            d0 = star(r_in * 0.9, r_out * 0.95, tips)
            ring_group.append(
                kfold(d0, p.symmetry, stroke=p.stroke, fill="none", sw=sw)
            )
        else:
            for i in range(motif_count):
                ang = (2 * math.pi / motif_count) * i
                r_mid = (r_in + r_out) * 0.5
                jitter = (r_out - r_in) * 0.15 * (random.random() - 0.5)
                x, y = pol2cart(r_mid + jitter, ang)
                ring_group.append(
                    dot(x, y, r=1.0 + 0.6 * random.random(), fill=p.stroke)
                )
            d1 = arc_ring(r_out, 0, 2 * math.pi / p.symmetry - 0.05)
            ring_group.append(
                kfold(d1, p.symmetry, stroke=p.stroke, fill="none", sw=sw * 0.7)
            )

        ring_group.append(group_close())
        svg.extend(ring_group)

        extra = max(0, p.complexity - 5)
        for _ in range(extra):
            r = random.uniform(r_in, r_out)
            d = arc_ring(r, 0, 2 * math.pi / p.symmetry - random.uniform(0.02, 0.08))
            svg.append(kfold(d, p.symmetry, stroke=p.stroke, fill="none", sw=sw * 0.6))

    svg.append(group_close())
    svg.append(svg_footer())
    return "".join(svg)


# Export helpers ------------------------------------------------------------


def svg_to_png(svg: str, out_path: Path, scale: float = 1.0) -> None:
    try:
        import cairosvg
    except Exception as e:  # pragma: no cover - missing dependency
        raise RuntimeError("cairosvg is required for PNG/PDF export") from e
    cairosvg.svg2png(
        bytestring=svg.encode("utf-8"), write_to=str(out_path), scale=scale
    )


def svg_to_pdf(svg: str, out_path: Path, scale: float = 1.0) -> None:
    try:
        import cairosvg
    except Exception as e:  # pragma: no cover - missing dependency
        raise RuntimeError("cairosvg is required for PNG/PDF export") from e
    cairosvg.svg2pdf(
        bytestring=svg.encode("utf-8"), write_to=str(out_path), scale=scale
    )


def save_svg(svg: str, filename: str) -> str:
    base = Path(settings.MEDIA_ROOT) / "exports" / "mandala"
    base.mkdir(parents=True, exist_ok=True)
    out_path = base / filename
    out_path.write_text(svg, encoding="utf-8")
    return f"exports/mandala/{filename}"
