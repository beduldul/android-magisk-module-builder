# Magisk & KernelSU Module Builder Utility v1.1.0

A Python command-line utility for Android module developers designed to validate module property metadata (`module.prop`), verify shell script syntax (`service.sh`), and package modules into zip archives with SHA-256 checksum generation.

---

## Features in v1.1.0

- **Metadata Validation**: Checks required fields in `module.prop` (`id`, `name`, `version`, `versionCode`, `author`).
- **Integrity Checksums**: Automatically calculates and outputs SHA-256 cryptographic checksums for generated zip packages.
- **JSON Build Manifest**: Generates `--json` manifest file (`module_build.json`) for CI/CD integration.
- **Automated Zip Packaging**: Packages the module directory into a clean, flashable zip file.

---

## Usage

```bash
python3 builder.py path/to/module_directory -o output_module.zip --json
```

---

## License
MIT License
