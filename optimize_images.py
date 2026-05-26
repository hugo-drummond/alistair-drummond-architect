#!/usr/bin/env python3
import os
from pathlib import Path
from PIL import Image

IMAGES_DIR = Path("/Users/hugodrummond/alistair-drummond-architect/images")
SKIP_FILES = {"favicon.png", "apple-touch-icon.png"}
PNG_PHOTO_CONVERT = {"Kruger355.png", "Fieggen3bbb.png"}
SKIP_UNDER_KB = 200

DESKTOP_MAX_W = 1400
MOBILE_MAX_W = 800
QUALITY = 85

total_before = 0
total_after = 0
changed = []
skipped_small = []
png_converted = []
errors = []

def process_jpeg(path):
    global total_before, total_after
    fname = path.name
    size_before = path.stat().st_size

    if size_before < SKIP_UNDER_KB * 1024:
        skipped_small.append(f"{path} ({size_before // 1024}KB)")
        total_before += size_before
        total_after += size_before
        return

    is_mobile = fname.lower().startswith("mob-")
    max_w = MOBILE_MAX_W if is_mobile else DESKTOP_MAX_W

    try:
        img = Image.open(path)
        orig_w, orig_h = img.size

        # Only resize if wider than target
        if orig_w > max_w:
            ratio = max_w / orig_w
            new_w = max_w
            new_h = int(orig_h * ratio)
            img = img.resize((new_w, new_h), Image.LANCZOS)
        else:
            new_w, new_h = orig_w, orig_h

        # Convert to RGB if needed (e.g. RGBA)
        if img.mode != "RGB":
            img = img.convert("RGB")

        img.save(path, "JPEG", quality=QUALITY, optimize=True)
        size_after = path.stat().st_size

        total_before += size_before
        total_after += size_after

        saved_kb = (size_before - size_after) // 1024
        if saved_kb > 0:
            changed.append(
                f"{path.relative_to(IMAGES_DIR)}: {size_before//1024}KB → {size_after//1024}KB (saved {saved_kb}KB)"
                + (f" [resized {orig_w}→{new_w}px]" if orig_w > max_w else "")
            )
        else:
            skipped_small.append(f"{path.relative_to(IMAGES_DIR)} (no saving)")
    except Exception as e:
        errors.append(f"{path}: {e}")
        total_before += size_before
        total_after += size_before

def convert_png_to_jpg(path):
    global total_before, total_after
    size_before = path.stat().st_size
    jpg_path = path.with_suffix(".jpg")

    try:
        img = Image.open(path)
        orig_w, orig_h = img.size

        if orig_w > DESKTOP_MAX_W:
            ratio = DESKTOP_MAX_W / orig_w
            img = img.resize((DESKTOP_MAX_W, int(orig_h * ratio)), Image.LANCZOS)

        if img.mode != "RGB":
            img = img.convert("RGB")

        img.save(jpg_path, "JPEG", quality=QUALITY, optimize=True)
        size_after = jpg_path.stat().st_size

        total_before += size_before
        total_after += size_after

        saved_kb = (size_before - size_after) // 1024
        png_converted.append(
            f"{path.name} → {jpg_path.name}: {size_before//1024}KB → {size_after//1024}KB (saved {saved_kb}KB)"
        )
    except Exception as e:
        errors.append(f"{path}: {e}")
        total_before += size_before
        total_after += size_before

# Walk all images
for root, dirs, files in os.walk(IMAGES_DIR):
    for fname in files:
        path = Path(root) / fname

        if fname in SKIP_FILES:
            continue

        ext = fname.lower()

        if ext.endswith((".jpg", ".jpeg")):
            process_jpeg(path)
        elif fname in PNG_PHOTO_CONVERT:
            convert_png_to_jpg(path)
        # else skip non-photo PNGs, CSS, JS, etc.

# Print report
print("\n" + "="*60)
print("IMAGE OPTIMIZATION REPORT")
print("="*60)
print(f"\nTotal before: {total_before//1024//1024:.1f} MB ({total_before//1024} KB)")
print(f"Total after:  {total_after//1024//1024:.1f} MB ({total_after//1024} KB)")
print(f"Total saved:  {(total_before-total_after)//1024} KB ({(total_before-total_after)//1024//1024:.1f} MB)")

print(f"\n--- CHANGED ({len(changed)} files) ---")
for line in changed:
    print(f"  {line}")

if png_converted:
    print(f"\n--- PNG → JPEG CONVERSIONS ({len(png_converted)}) ---")
    for line in png_converted:
        print(f"  {line}")

print(f"\n--- SKIPPED (small/no gain): {len(skipped_small)} files ---")

if errors:
    print(f"\n--- ERRORS ({len(errors)}) ---")
    for line in errors:
        print(f"  {line}")
