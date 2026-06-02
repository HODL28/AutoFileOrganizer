# AutoFileOrganizer 📷🎥📄🎵📦💻📁

[![CI](https://github.com/HODL28/AutoFileOrganizer/actions/workflows/ci.yml/badge.svg)](https://github.com/HODL28/AutoFileOrganizer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)

A modern, ultra-fast CLI tool written in Python to automatically organize your cluttered folders (such as your *Downloads* folder) into clean, themed subdirectories.

---

## 📷 Description

**AutoFileOrganizer** scans your files and instantly sorts them into structured directories based on their file extensions. It features an elegant terminal interface inspired by GitHub CLI, color-coded warnings, and a secure simulation mode (*dry-run*).

---

## ✨ Features

- **Instant Sorting**: Group files into clear categories:
  - `Images/` (jpg, png, gif, webp, svg, etc.)
  - `Videos/` (mp4, mov, avi, mkv, etc.)
  - `Documents/` (pdf, docx, xlsx, txt, etc.)
  - `Music/` (mp3, wav, flac, etc.)
  - `Archives/` (zip, rar, tar, gz, etc.)
  - `Code/` (py, js, ts, html, css, go, rs, etc.)
  - `Others/` (all other extensions)
- **Built-in Safety (Dry-Run)**: Use `--dry-run` to preview actions without modifying files.
- **Recursive Scan**: Organize all subdirectories recursively using the `--recursive` option.
- **Smart Conflict Resolution**: Automatically renames duplicate target files (e.g. `document.pdf` becomes `document_1.pdf`).
- **Robust Scanner**: Automatically excludes system folders (`.git`, `node_modules`, `__pycache__`, etc.) and safely handles symbolic links.

---

## 🚀 Installation

Install AutoFileOrganizer locally from the source files:

```bash
git clone https://github.com/HODL28/AutoFileOrganizer.git
cd AutoFileOrganizer
pip install .
```

For development, install in editable mode with development dependencies:

```bash
pip install -e .
pip install pytest pytest-cov ruff
```

---

## 💡 Usage

The global command `organize` is available after installation:

### Organize the current directory
```bash
organize
```

### Organize a specific folder
```bash
organize "/Users/username/Downloads"
```

### Simulation Mode (Dry Run)
```bash
organize --dry-run
```

### Recursive Mode
```bash
organize --recursive
```

### Show Help
```bash
organize --help
```

---

## 📊 Terminal Display Example

```
╭──────────────────────────────────────────────────────────────────────────────╮
│   🚀 ORGANIZATION COMPLETE                                                   │
│ Target directory:                                                            │
│ /Users/clement/Downloads                                                     │
╰──────────────────────────────────────────────────────────────────────────────╯

File move details :
  📷 vacation_photo.jpg → Images/vacation_photo.jpg
  📄 monthly_report.pdf → Documents/monthly_report.pdf
  📦 final_project.zip → Archives/final_project.zip
  💻 script.py → Code/script.py
  📁 config.yaml → Others/config.yaml

Category Summary
╭──────────────────────┬─────────────┬─────────────╮
│ Category             │ Files Count │ Destination │
├──────────────────────┼─────────────┼─────────────┤
│ 📷 Images            │           1 │ Images/     │
│ 📄 Documents         │           1 │ Documents/  │
│ 📦 Archives          │           1 │ Archives/   │
│ 💻 Code              │           1 │ Code/       │
│ 📁 Others            │           1 │ Others/     │
╰──────────────────────┴─────────────┴─────────────╯

Statistics
╭────────────────────────────────────╮
│   Total Scanned : 5                │
│   Total Moved : 5                  │
│   Execution Duration : 0.012s      │
╰────────────────────────────────────╯
```

---

## 🛠️ Contributing

Contributions are welcome!
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/amazing-feature`).
3. Check code formatting: `ruff check .`
4. Run unit tests: `pytest`
5. Commit your changes (`git commit -m 'Add some amazing feature'`).
6. Push to the branch (`git push origin feature/amazing-feature`).
7. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
