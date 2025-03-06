# MIMIC-III Subset Creator

A Python script to create a manageable subset of the MIMIC-III database for educational purposes. This tool extracts a random sample of hospital admissions and all related data, making it easier to work with the MIMIC-III database in tutorials and research projects.

## Important Note

To use this tool, you need access to the MIMIC-III Clinical Database. To get access:
1. Complete the [CITI "Data or Specimens Only Research" course](https://physionet.org/about/citi-course/)
2. [Sign up for a PhysioNet account](https://physionet.org/register/)
3. [Request access to MIMIC-III](https://physionet.org/content/mimiciii/)
4. Download the MIMIC-III Clinical Database v1.4 zip file

## Features

- Creates a random subset of 3,000 hospital admissions (configurable)
- Extracts all related patient information, ICU stays, diagnoses, and procedures
- Includes vital signs from CHARTEVENTS and a sample of lab results
- Maintains data relationships and integrity
- Progress bars and detailed status updates
- Creates a comprehensive README for the subset

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- MIMIC-III Clinical Database v1.4 zip file
- At least 1GB of free disk space

## Installation

### Windows

1. Install Python 3.8 or higher:
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Open Command Prompt and verify installation:
     ```cmd
     python --version
     pip --version
     ```

2. Clone this repository:
   ```cmd
   git clone https://github.com/yazeedz/python2med.git
   cd python2med/mimic-subset-creator
   ```

   Or download as ZIP:
   - Go to https://github.com/yazeedz/python2med
   - Click "Code" → "Download ZIP"
   - Extract the ZIP file
   - Navigate to the mimic-subset-creator directory

3. Create a virtual environment (recommended):
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

4. Install required packages:
   ```cmd
   pip install -r requirements.txt
   ```

### macOS

1. Install Python 3.8 or higher:
   ```bash
   # Using Homebrew
   brew install python

   # Or using pyenv (recommended)
   brew install pyenv
   pyenv install 3.11.9
   pyenv global 3.11.9
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/yazeedz/python2med.git
   cd python2med/mimic-subset-creator
   ```

3. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install required packages:
   ```bash
   pip3 install -r requirements.txt
   ```

### Linux (Ubuntu/Debian)

1. Install Python 3.8 or higher:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv git
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/yazeedz/python2med.git
   cd python2med/mimic-subset-creator
   ```

3. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install required packages:
   ```bash
   pip3 install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
# Windows
python src/create_mimic_subset.py "path\to\mimic-iii-clinical-database-1.4.zip" "path\to\output\directory"

# macOS/Linux
python3 src/create_mimic_subset.py "/path/to/mimic-iii-clinical-database-1.4.zip" "/path/to/output/directory"
```

### Advanced Usage

You can specify the number of admissions to include in the subset:

```bash
python3 src/create_mimic_subset.py "/path/to/mimic.zip" "/path/to/output" --sample-size 5000
```

### Example

```bash
# Windows
python src/create_mimic_subset.py "C:\Downloads\mimic-iii-clinical-database-1.4.zip" "C:\MIMIC-III-Subset"

# macOS/Linux
python3 src/create_mimic_subset.py "/Downloads/mimic-iii-clinical-database-1.4.zip" "/MIMIC-III-Subset"
```

## Output

The script will create a directory containing:

1. Core tables:
   - ADMISSIONS.csv
   - PATIENTS.csv
   - ICUSTAYS.csv
   - DIAGNOSES_ICD.csv
   - PROCEDURES_ICD.csv
   - PRESCRIPTIONS.csv
   - CHARTEVENTS_VITALS.csv (vital signs only)
   - LABEVENTS_SAMPLE.csv (sample of lab results)

2. Dictionary tables:
   - D_ICD_DIAGNOSES.csv
   - D_ICD_PROCEDURES.csv
   - D_ITEMS.csv
   - D_LABITEMS.csv

3. A detailed README.md with dataset information

## Troubleshooting

### Common Issues

1. **Python not found**
   - Make sure Python is installed and added to PATH
   - Try using `python3` instead of `python` on macOS/Linux

2. **Package installation errors**
   - Try upgrading pip: `python -m pip install --upgrade pip`
   - Make sure you're in the virtual environment
   - Install packages individually if needed

3. **Permission errors**
   - Use `sudo` for package installation on Linux if needed
   - Check write permissions for the output directory

4. **Memory errors**
   - Close other applications
   - Reduce the sample size using `--sample-size`
   - If using a VM, increase allocated RAM

### Getting Help

If you encounter issues:
1. Check the error message in the terminal
2. Verify Python version and package installation
3. Check file paths and permissions
4. [Open an issue](https://github.com/yazeedz/python2med/issues) with:
   - Your operating system and Python version
   - The complete error message
   - Steps to reproduce the issue

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- MIMIC-III Clinical Database v1.4
- PhysioNet for providing the original database
- The pandas and numpy development teams 