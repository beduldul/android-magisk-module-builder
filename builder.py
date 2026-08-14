#!/usr/bin/env python3
"""
Magisk & KernelSU Module Builder Utility
"""

import sys
import os
import zipfile
import argparse

REQUIRED_PROPS = ["id", "name", "version", "versionCode", "author"]

def validate_module(module_path):
    print(f"[*] Validating Magisk Module Directory: {module_path}")
    prop_path = os.path.join(module_path, "module.prop")
    if not os.path.exists(prop_path):
        print(f"[!] Error: {prop_path} not found.")
        return False

    props = {}
    with open(prop_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split("=", 1)
                if len(parts) == 2:
                    props[parts[0]] = parts[1]

    for prop in REQUIRED_PROPS:
        if prop not in props:
            print(f"[!] Error: Missing required property '{prop}' in module.prop")
            return False
        print(f"  [✓] Property '{prop}': {props[prop]}")

    return True

def package_module(module_path, output_zip):
    if not validate_module(module_path):
        sys.exit(1)

    print(f"\n[*] Packaging module into {output_zip}...")
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(module_path):
            for file in files:
                abs_file = os.path.join(root, file)
                rel_file = os.path.relpath(abs_file, module_path)
                zipf.write(abs_file, rel_file)
                print(f"  + Added: {rel_file}")

    print(f"\n[+] Success: Module packaged successfully -> {output_zip}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Magisk & KernelSU Module Builder Utility")
    parser.add_argument("module_dir", help="Path to module directory")
    parser.add_argument("-o", "--output", default="module.zip", help="Output zip filename")
    args = parser.parse_args()

    package_module(args.module_dir, args.output)
