#!/usr/bin/env python3
"""
Magisk & KernelSU Module Builder Utility v1.1.0
"""

import sys
import os
import zipfile
import argparse
import hashlib
import json

REQUIRED_PROPS = ["id", "name", "version", "versionCode", "author"]

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def validate_module(module_path):
    print(f"[*] Validating Magisk Module Directory: {module_path}")
    prop_path = os.path.join(module_path, "module.prop")
    if not os.path.exists(prop_path):
        print(f"[!] Error: {prop_path} not found.")
        return False, {}

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
            return False, {}
        print(f"  [OK] Property '{prop}': {props[prop]}")

    sepolicy_path = os.path.join(module_path, "sepolicy.rule")
    if os.path.exists(sepolicy_path):
        print(f"  [OK] Found sepolicy.rule")

    return True, props

def package_module(module_path, output_zip, generate_json=False):
    valid, props = validate_module(module_path)
    if not valid:
        sys.exit(1)

    print(f"\n[*] Packaging module into {output_zip}...")
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(module_path):
            for file in files:
                abs_file = os.path.join(root, file)
                rel_file = os.path.relpath(abs_file, module_path)
                zipf.write(abs_file, rel_file)

    sha256 = calculate_sha256(output_zip)
    print(f"\n[+] Success: Module packaged successfully -> {output_zip}")
    print(f"[+] SHA-256 Checksum: {sha256}")

    if generate_json:
        manifest = {
            "module_id": props.get("id"),
            "version": props.get("version"),
            "versionCode": props.get("versionCode"),
            "sha256": sha256,
            "filename": output_zip
        }
        with open("module_build.json", "w") as jf:
            json.dump(manifest, jf, indent=2)
        print(f"[+] Generated manifest -> module_build.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Magisk & KernelSU Module Builder Utility v1.1.0")
    parser.add_argument("module_dir", help="Path to module directory")
    parser.add_argument("-o", "--output", default="module.zip", help="Output zip filename")
    parser.add_argument("--json", action="store_true", help="Generate JSON build manifest")
    args = parser.parse_args()

    package_module(args.module_dir, args.output, args.json)
