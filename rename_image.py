import os
import re
from typing import List, Tuple

IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tif", ".tiff", ".webp")

def list_image_files(dirpath: str) -> List[str]:
    return [f for f in os.listdir(dirpath)
            if os.path.isfile(os.path.join(dirpath, f))
            and f.lower().endswith(IMAGE_EXTS)]

def natural_sort_key(name: str):
    parts = re.split(r'(\d+)', name)
    return [int(p) if p.isdigit() else p.lower() for p in parts]

def rename_sequentially(dirpath: str, dry_run: bool = False) -> Tuple[int,int]:
    files = list_image_files(dirpath)
    if not files:
        return (0, 0)

    files.sort(key=natural_sort_key)
    total = len(files)
    width = len(str(total))

    tmp_pairs = []
    # step1: rename to unique tmp names to avoid collisions
    for idx, fname in enumerate(files):
        src = os.path.join(dirpath, fname)
        tmp = os.path.join(dirpath, f".tmp_rename_{os.getpid()}_{idx}")
        tmp_pairs.append((tmp, fname))
        if dry_run:
            print(f"[DRY] {dirpath}: {fname} -> {os.path.basename(tmp)}")
        else:
            os.rename(src, tmp)

    renamed = 0
    # step2: tmp -> final sequential (1..N)
    for idx, (tmp_path, original_name) in enumerate(tmp_pairs):
        _, ext = os.path.splitext(original_name)
        ext = ext.lower()
        final_name = f"{(idx+1):0{width}d}{ext}"
        final_path = os.path.join(dirpath, final_name)

        if dry_run:
            print(f"[DRY] {dirpath}: {os.path.basename(tmp_path)} -> {final_name}")
            renamed += 1
            continue

        # if final exists (unlikely), append suffix
        if os.path.exists(final_path):
            final_path = os.path.join(dirpath, f"{(idx+1):0{width}d}_dup{ext}")

        os.rename(tmp_path, final_path)
        renamed += 1
        print(f"{dirpath}: {original_name} -> {final_name}")

    return (renamed, total)

def walk_and_rename_all(root_base: str, dry_run: bool = False):
    if not os.path.isdir(root_base):
        print("Base directory not found:", root_base)
        return

    # assume structure: root_base/<class>/<species>
    for class_name in sorted(os.listdir(root_base)):
        class_path = os.path.join(root_base, class_name)
        if not os.path.isdir(class_path):
            continue
        for species in sorted(os.listdir(class_path)):
            species_path = os.path.join(class_path, species)
            if not os.path.isdir(species_path):
                continue
            renamed, total = rename_sequentially(species_path, dry_run=dry_run)
            if total:
                print(f"[{class_name}/{species}] Renamed {renamed}/{total} -> 1..{total}")
            else:
                print(f"[{class_name}/{species}] No images")

if __name__ == "__main__":
    # no arguments: use ./fungi folder next to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(script_dir, "fungi")
    # set dry_run = True to preview
    DRY_RUN = False
    walk_and_rename_all(base_dir, dry_run=DRY_RUN)
