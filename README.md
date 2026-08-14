# Magisk & KernelSU Module Builder Utility

A Python command-line utility for Android module developers designed to validate module property metadata (`module.prop`), verify shell script syntax (`service.sh`), and package modules into zip archives.

---

## 🛠 Features

- **Metadata Validation**: Checks required fields in `module.prop` (`id`, `name`, `version`, `versionCode`, `author`).
- **Script Verification**: Validates execution permissions and shell syntax of `service.sh` and `action.sh`.
- **Automated Zip Packaging**: Packages the module directory into a clean, flashable zip file.

---

## 💻 Usage

```bash
python3 builder.py path/to/module_directory -o output_module.zip
```

---

## 📄 License
MIT License
