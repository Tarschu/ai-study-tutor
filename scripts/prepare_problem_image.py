#!/usr/bin/env python3
"""Create readability-enhanced copies of a problem image."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps
except ModuleNotFoundError as exc:  # pragma: no cover - environment guard
    raise SystemExit(
        "Pillow is required. Run with a Python environment that has Pillow installed."
    ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Enhance a photographed or screenshot problem image for easier reading."
    )
    parser.add_argument("image", help="Input image path")
    parser.add_argument(
        "--outdir",
        default=None,
        help="Output directory. Defaults to '<input parent>/prepared'.",
    )
    parser.add_argument("--scale", type=float, default=2.0, help="Resize multiplier")
    parser.add_argument("--contrast", type=float, default=1.65, help="Contrast multiplier")
    parser.add_argument("--sharpness", type=float, default=1.4, help="Sharpness multiplier")
    parser.add_argument(
        "--threshold",
        type=int,
        default=0,
        help="Optional black/white threshold from 1 to 255. Disabled by default.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    src = Path(args.image).expanduser().resolve()
    if not src.is_file():
        raise SystemExit(f"Input image does not exist: {src}")

    outdir = Path(args.outdir).expanduser().resolve() if args.outdir else src.parent / "prepared"
    outdir.mkdir(parents=True, exist_ok=True)

    image = Image.open(src)
    image = ImageOps.exif_transpose(image).convert("RGB")
    if args.scale <= 0:
        raise SystemExit("--scale must be greater than 0")
    if args.scale != 1:
        width = max(1, round(image.width * args.scale))
        height = max(1, round(image.height * args.scale))
        image = image.resize((width, height), Image.Resampling.LANCZOS)

    base = src.stem
    outputs: list[Path] = []

    gray = ImageOps.grayscale(image)
    gray_path = outdir / f"{base}_gray.png"
    gray.save(gray_path)
    outputs.append(gray_path)

    enhanced = ImageEnhance.Contrast(gray).enhance(args.contrast)
    enhanced = ImageEnhance.Sharpness(enhanced).enhance(args.sharpness)
    enhanced = enhanced.filter(ImageFilter.UnsharpMask(radius=1.2, percent=130, threshold=3))
    enhanced_path = outdir / f"{base}_enhanced.png"
    enhanced.save(enhanced_path)
    outputs.append(enhanced_path)

    if args.threshold:
        if not 1 <= args.threshold <= 255:
            raise SystemExit("--threshold must be between 1 and 255")
        bw = enhanced.point(lambda pixel: 255 if pixel >= args.threshold else 0)
        bw_path = outdir / f"{base}_bw.png"
        bw.save(bw_path)
        outputs.append(bw_path)

    print("Generated:")
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()
