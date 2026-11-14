# DLP Scanner — Data Loss Prevention Tool

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-AGPL--3.0-purple.svg)
![Security](https://img.shields.io/badge/Domain-Cybersecurity-red)
![Project](https://img.shields.io/badge/Type-Data%20Protection-blue)

**A Python-based Data Loss Prevention (DLP) scanner designed to detect sensitive information across files, databases, and network traffic.**

DLP Scanner helps identify exposed Personally Identifiable Information (PII), credentials, financial records, and Protected Health Information (PHI), supporting security assessments and data protection compliance.

## Overview

The tool provides multiple scanning capabilities:

- **File scanning:** Detect sensitive data in PDF, DOCX, XLSX, CSV, JSON, XML, YAML, Parquet, Avro, archives, and email files.
- **Database scanning:** Inspect PostgreSQL, MySQL, MongoDB, and SQLite databases using schema introspection and data sampling.
- **Network traffic scanning:** Analyze PCAP/PCAPNG captures with protocol parsing, TCP stream reassembly, and DNS exfiltration detection.
- **Confidence scoring:** Combine pattern matching, checksum validation, contextual analysis, and entity co-occurrence.
- **Compliance mapping:** Associate findings with HIPAA, PCI DSS, GDPR, CCPA, SOX, GLBA, and FERPA.
- **Reporting:** Export findings to Console, JSON, SARIF 2.1.0, and CSV.

## Architecture & Detection

The scanner uses a layered detection pipeline:

1. Data extraction from supported sources.
2. Pattern matching and sensitive-data identification.
3. Checksum validation (Luhn, Mod-97, Mod-11).
4. Contextual keyword and proximity analysis.
5. Confidence scoring and severity classification.
6. Sensitive-value redaction and compliance mapping.
7. Structured report generation.

## Technology Stack

| Component | Technologies |
|---|---|
| Language | Python 3.12+ |
| CLI | Typer, Rich |
| Detection | Regex, checksum validation, Shannon entropy |
| Configuration | Pydantic, YAML |
| File processing | PyMuPDF, python-docx, openpyxl, xlrd |
| Databases | PostgreSQL, MySQL, MongoDB, SQLite |
| Network analysis | dpkt, TCP reassembly, protocol identification |
| Testing | pytest, Hypothesis |
| Code quality | Ruff, mypy, YAPF |

## Project Structure

```text
dlp-scanner/
├── learn/
│   ├── 00-OVERVIEW.md
│   ├── 01-CONCEPTS.md
│   ├── 02-ARCHITECTURE.md
│   ├── 03-IMPLEMENTATION.md
│   └── 04-CHALLENGES.md
├── src/
│   └── dlp_scanner/
├── tests/
├── .dlp-scanner.yml
├── .env.example
├── .gitignore
├── install.sh
├── justfile
├── pyproject.toml
├── uv.lock
└── README.md
```

## Installation

### Linux / macOS

```bash
git clone https://github.com/hamzaatlili/dlp-scanner-Copier.git
cd dlp-scanner-Copier

bash install.sh
```

### Python environment

If you prefer manual installation:

```bash
python -m venv .venv
```

Activate the environment:

**Linux / macOS**
```bash
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project according to its `pyproject.toml` configuration:

```bash
pip install -e .
```

## Usage

### Scan files

```bash
dlp-scan file ./data/
```

Scan a specific file:

```bash
dlp-scan file ./data/employees.csv
```

### Scan databases

```bash
dlp-scan db postgres://user:password@host/database
```

```bash
dlp-scan db sqlite:///path/to/database.db
```

### Scan network traffic

```bash
dlp-scan network capture.pcap
```

### Generate reports

JSON:

```bash
dlp-scan file ./data/ -f json
```

SARIF:

```bash
dlp-scan file ./data/ -f sarif -o results.sarif
```

CSV:

```bash
dlp-scan report convert results.json -f csv
```

View report summary:

```bash
dlp-scan report summary results.json
```

## Output Formats

| Format | Purpose |
|---|---|
| Console | Interactive terminal output |
| JSON | Structured security findings |
| SARIF 2.1.0 | Integration with code scanning and CI/CD |
| CSV | Compliance reviews and spreadsheet analysis |

## Configuration

The scanner can be customized through `.dlp-scanner.yml`.

Example:

```yaml
detection:
  min_confidence: 0.20
  enable_rules: ["*"]
  allowlists:
    values:
      - "123-45-6789"

output:
  format: "console"
  redaction_style: "partial"
```

Review the configuration file before running scans in production environments.

## Testing

Run the test suite using:

```bash
pytest
```

For verbose output:

```bash
pytest -v
```

## Learning Resources

The `learn/` directory contains educational documentation:

| Module | Description |
|---|---|
| 00 - Overview | Prerequisites and quick start |
| 01 - Concepts | DLP fundamentals and real-world security incidents |
| 02 - Architecture | System architecture and data flow |
| 03 - Implementation | Code walkthrough |
| 04 - Challenges | Practical exercises and extension ideas |

## Security & Responsible Use

- Only scan files, databases, and network traffic you are authorized to inspect.
- Avoid committing real credentials, API keys, personal data, or production datasets.
- Use synthetic data for testing and demonstrations.
- Review findings before taking remediation actions.

## License

This project is distributed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

See the [LICENSE](LICENSE) file for details.

---

**Developed for cybersecurity learning, sensitive-data discovery, and data protection research.**