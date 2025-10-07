import os
import sys
from typing import List, Tuple

IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tif", ".tiff", ".webp")

def list_image_files(dirpath: str) -> List[str]:
    return [f for f in os.listdir(dirpath)
            if os.path.isfile(os.path.join(dirpath, f))
            and f.lower().endswith(IMAGE_EXTS)]

def natural_sort_key(name: str):
    # try to sort numerically when possible, fallback to name
    import re
    parts = re.split(r'(\d+)', name)
    return [int(p) if p.isdigit() else p.lower() for p in parts]

def rename_sequentially(dirpath: str, dry_run: bool = False) -> Tuple[int,int]:
    """
    Rename all images in dirpath to 1..N preserving extension.
    Returns (renamed_count, total_files).
    Uses two-step rename (tmp -> final) to avoid name collisions.
    """
    files = list_image_files(dirpath)
    if not files:
        return (0, 0)

    files.sort(key=natural_sort_key)

    total = len(files)
    width = len(str(total))

    # Step 1: rename to temporary unique names
    tmp_names = []
    for idx, fname in enumerate(files):
        src = os.path.join(dirpath, fname)
        tmp = os.path.join(dirpath, f".tmp_rename_{idx}")
        tmp_names.append((tmp, fname))
        if dry_run:
            print(f"[DRY] would rename: {fname} -> {os.path.basename(tmp)}")
        else:
            os.rename(src, tmp)

    # Step 2: rename tmp -> final (1..N)
    renamed = 0
    for idx, (tmp_path, original_name) in enumerate(tmp_names):
        # reuse extension of original
        _, ext = os.path.splitext(original_name)
        ext = ext.lower() if ext else ""
        final_name = f"{(idx+1):0{width}d}{ext}"
        final_path = os.path.join(dirpath, final_name)

        if dry_run:
            print(f"[DRY] would rename: {os.path.basename(tmp_path)} -> {final_name}")
            renamed += 1
            continue

        # If final already exists (shouldn't after tmp step), avoid overwrite by using tmp suffix
        if os.path.exists(final_path):
            final_path = os.path.join(dirpath, f"{(idx+1):0{width}d}_dup{ext}")

        os.rename(tmp_path, final_path)
        renamed += 1
        print(f"Renamed: {original_name} -> {final_name}")

    return (renamed, total)

def walk_and_rename(base_dir: str, dry_run: bool = False):
    if not os.path.isdir(base_dir):
        print("Base directory does not exist:", base_dir)
        return

    for folder_name in sorted(os.listdir(base_dir)):
        folder_path = os.path.join(base_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue

        # If you have species folders under this, iterate them; otherwise treat folder_path as species folder.
        # Here we assume structure: base_dir/<class>/<species> like your earlier script.
        for sub in sorted(os.listdir(folder_path)):
            sub_path = os.path.join(folder_path, sub)
            if not os.path.isdir(sub_path):
                continue

            renamed, total = rename_sequentially(sub_path, dry_run=dry_run)
            if total:
                print(f"[{folder_name}/{sub}] Renamed {renamed}/{total} images -> 1..{total}")
            else:
                print(f"[{folder_name}/{sub}] No images found")

if __name__ == "__main__":
    # usage: python rename_images_sequentially.py /path/to/fungi [--dry]
    if len(sys.argv) < 2:
        print("Usage: python rename_images_sequentially.py /path/to/fungi [--dry]")
        sys.exit(1)

    base = sys.argv[1]
    dry = ("--dry" in sys.argv) or ("-n" in sys.argv)
    walk_and_rename(base, dry_run=dry)