from pathlib import Path

from mandala.services.generator import (
    MandalaParams,
    generate_mandala_svg,
    svg_to_pdf,
    svg_to_png,
)


def test_generate_svg():
    p = MandalaParams(symmetry=8, rings=6, complexity=5, seed=42)
    svg = generate_mandala_svg(p)
    assert svg.startswith("<svg")


def test_export_png_pdf(tmp_path: Path):
    p = MandalaParams(symmetry=6, rings=5, complexity=4, seed=1)
    svg = generate_mandala_svg(p)
    png_path = tmp_path / "out.png"
    pdf_path = tmp_path / "out.pdf"
    svg_to_png(svg, png_path)
    svg_to_pdf(svg, pdf_path)
    assert png_path.exists()
    assert pdf_path.exists()
