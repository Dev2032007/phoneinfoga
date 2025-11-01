# PhoneInfoga (Python Version)

<p align="center">
  <img src="../docs/images/banner.png" width=500  alt="project logo"/>
</p>

## About

This is a Python conversion of PhoneInfoga, an advanced OSINT tool for phone number information gathering.

PhoneInfoga is one of the most advanced tools to scan international phone numbers. It allows you to first gather basic information such as country, area, carrier and line type, then use various techniques to try to find the VoIP provider or identify the owner.

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install the package
pip install -e .
```

## Usage

### CLI Commands

```bash
# Scan a phone number
phoneinfoga scan -n +33678342311

# List available scanners
phoneinfoga scanners

# Start web server
phoneinfoga serve -p 5000

# Show version
phoneinfoga version
```

### Python API

```python
from phoneinfoga.lib.number import Number
from phoneinfoga.lib.remote import Library, init_scanners
from phoneinfoga.lib.filter import Engine

# Create a phone number
num = Number("+33678342311")

# Initialize scanners
filter_engine = Engine()
library = Library(filter_engine)
init_scanners(library)

# Run scan
results, errors = library.scan(num)
```

## Features

- Check if phone number exists
- Gather basic information such as country, line type and carrier
- OSINT footprinting using external APIs, phone books & search engines
- Check for reputation reports, social media, disposable numbers and more
- Use the graphical user interface to run scans from the browser
- Programmatic usage with the REST API and Python modules

## License

This tool is licensed under the GNU General Public License v3.0.

## Original Project

This is a Python conversion of the original Go project:
https://github.com/sundowndev/phoneinfoga
