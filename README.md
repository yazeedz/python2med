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
- Interactive command-line interface
- Supports paths with or without quotes

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

### Running the Script

Simply run the script and follow the interactive prompts:

```bash
# Windows
python src/create_mimic_subset.py

# macOS/Linux
python3 src/create_mimic_subset.py
```

The script will ask you for:
1. The path to your MIMIC-III zip file
2. The directory where you want to save the subset
3. The number of admissions to include (optional, default is 3000)

You can enter paths with or without quotes:
```
/path/to/file.zip
"/path/to/file.zip"
'C:\path\to\file.zip'
```

### Example Sessions

```
========================================
MIMIC-III Subset Creator
========================================

# Example with regular paths
Enter the path to the MIMIC-III zip file: /Downloads/mimic-iii-clinical-database-1.4.zip
Enter the path where you want to save the subset: /MIMIC-III-Subset

# Example with quoted paths (also works)
Enter the path to the MIMIC-III zip file: "/Users/username/Downloads/mimic-iii-clinical-database-1.4.zip"
Enter the path where you want to save the subset: 'C:\Users\username\MIMIC-III-Subset'

Enter the number of admissions to include (default: 3000): 

Starting MIMIC-III subset creation...
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
   - Reduce the sample size when prompted
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