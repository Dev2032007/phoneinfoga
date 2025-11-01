# PhoneInfoga - Go to Python Conversion Notes

## Overview

This is a complete conversion of the PhoneInfoga project from Go to Python. The conversion maintains the same architecture, features, and command-line interface while adapting to Python idioms and best practices.

## Project Structure

```
python/
├── phoneinfoga/              # Main package
│   ├── __init__.py
│   ├── __main__.py          # Entry point for python -m phoneinfoga
│   ├── build/               # Build information module
│   │   ├── __init__.py
│   │   └── build.py
│   ├── logs/                # Logging configuration
│   │   ├── __init__.py
│   │   └── config.py
│   ├── lib/                 # Core library modules
│   │   ├── __init__.py
│   │   ├── number/          # Phone number handling
│   │   │   ├── __init__.py
│   │   │   ├── number.py
│   │   │   └── utils.py
│   │   ├── filter/          # Scanner filtering
│   │   │   ├── __init__.py
│   │   │   └── filter.py
│   │   ├── output/          # Output formatting
│   │   │   ├── __init__.py
│   │   │   ├── output.py
│   │   │   └── console.py
│   │   └── remote/          # Scanner system
│   │       ├── __init__.py
│   │       ├── scanner.py
│   │       ├── library.py
│   │       ├── local_scanner.py
│   │       └── init.py
│   └── cli/                 # CLI commands
│       ├── __init__.py
│       ├── root.py
│       ├── scan.py
│       ├── serve.py
│       ├── version.py
│       └── scanners.py
├── main.py                  # Standalone entry point
├── setup.py                 # Setup script
├── pyproject.toml          # Project configuration
├── requirements.txt        # Dependencies
└── README.md               # Documentation
```

## Key Conversions

### 1. Dependencies Mapping

| Go Package | Python Package | Purpose |
|------------|---------------|---------|
| `github.com/spf13/cobra` | `click` | CLI framework |
| `github.com/gin-gonic/gin` | `flask` | Web framework |
| `github.com/sirupsen/logrus` | `logging` | Logging |
| `github.com/nyaruka/phonenumbers` | `phonenumbers` | Phone number parsing |
| `github.com/joho/godotenv` | `python-dotenv` | Environment variables |
| `github.com/fatih/color` | `colorama` | Terminal colors |

### 2. Language Feature Conversions

#### Goroutines → Threading/AsyncIO
- Go's goroutines with `sync.WaitGroup` → Python's `ThreadPoolExecutor`
- Concurrent scanner execution maintained using thread pools

#### Error Handling
- Go's `error` return values → Python exceptions
- Go's `if err != nil` → Python's `try/except` blocks

#### Type System
- Go's explicit types → Python type hints (PEP 484)
- Go's structs → Python dataclasses

#### Interfaces
- Go interfaces → Python abstract base classes (ABC)

### 3. Module Conversions

#### build/ → phoneinfoga/build/
- Version and commit tracking
- Release detection
- Demo mode detection

#### logs/ → phoneinfoga/logs/
- Logging configuration
- Log level management from environment variables
- Structured logging support

#### lib/number/ → phoneinfoga/lib/number/
- Phone number validation and parsing
- Country code detection
- Number formatting utilities
- Uses `phonenumbers` library (Python port of libphonenumber)

#### lib/filter/ → phoneinfoga/lib/filter/
- Scanner filtering engine
- Rule-based matching system

#### lib/output/ → phoneinfoga/lib/output/
- Console output formatter
- Colored output using `colorama`
- Structured result display

#### lib/remote/ → phoneinfoga/lib/remote/
- Scanner interface (ABC)
- Scanner library for managing scanners
- Concurrent scanner execution
- Plugin system (simplified)
- Local scanner implementation

#### cmd/ → phoneinfoga/cli/
- `root.go` → `root.py` - Main CLI setup
- `scan.go` → `scan.py` - Scan command
- `serve.go` → `serve.py` - Web server command
- `version.go` → `version.py` - Version command
- `scanners.go` → `scanners.py` - List scanners command

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Install Dependencies

```bash
cd python/
pip install -r requirements.txt
```

### Install as Package

```bash
cd python/
pip install -e .
```

## Usage

### Command Line Interface

```bash
# Show version
python main.py version
# or
phoneinfoga version

# List available scanners
python main.py scanners
# or
phoneinfoga scanners

# Scan a phone number
python main.py scan -n +33678342311
# or
phoneinfoga scan -n +33678342311

# Scan with disabled scanners
phoneinfoga scan -n +33678342311 -D googlesearch -D numverify

# Start web server (placeholder)
phoneinfoga serve -p 5000
```

### Python API

```python
from phoneinfoga.lib.number import Number
from phoneinfoga.lib.remote import Library, init_scanners
from phoneinfoga.lib.filter import Engine
from phoneinfoga.lib.output import get_output, OutputType
import sys

# Parse phone number
number = Number("+33678342311")
print(f"Country: {number.country}")
print(f"E164: {number.e164}")

# Initialize scanner library
filter_engine = Engine()
library = Library(filter_engine)
init_scanners(library)

# Run scan
results, errors = library.scan(number)

# Display results
output = get_output(OutputType.CONSOLE, sys.stdout)
output.write(results, errors)
```

## Testing

### Basic Tests

```bash
cd python/
python test_basic.py
```

### Unit Tests (when implemented)

```bash
cd python/
pytest tests/
```

## Differences from Go Version

### Implemented
- ✅ Core phone number parsing and validation
- ✅ Scanner system architecture
- ✅ Filter engine
- ✅ Console output formatting
- ✅ CLI commands (scan, version, scanners)
- ✅ Logging configuration
- ✅ Build information tracking
- ✅ Local scanner

### Not Yet Implemented
- ❌ Web server (serve command is placeholder)
- ❌ External scanners (Numverify, Google Search, OVH, Google CSE)
- ❌ Plugin loading system (simplified version only)
- ❌ Full test suite
- ❌ Web client UI

### Simplified
- Plugin system uses Python's importlib (not fully implemented)
- Web server would use Flask/FastAPI instead of Gin
- Async operations use ThreadPoolExecutor instead of goroutines

## Development

### Code Style
- Follow PEP 8 style guide
- Use type hints for all functions
- Use docstrings for all modules, classes, and functions
- Format code with `black`

### Adding New Scanners

```python
from phoneinfoga.lib.remote import Scanner, ScannerOptions
from phoneinfoga.lib.number import Number
from dataclasses import dataclass
from typing import Optional

@dataclass
class MyScannerResponse:
    field1: str
    field2: int

class MyScanner(Scanner):
    def name(self) -> str:
        return "myscanner"
    
    def description(self) -> str:
        return "My custom scanner"
    
    def dry_run(self, number: Number, options: ScannerOptions) -> Optional[Exception]:
        # Return None if scanner should run, Exception otherwise
        return None
    
    def run(self, number: Number, options: ScannerOptions) -> MyScannerResponse:
        # Implement scanner logic
        return MyScannerResponse(field1="value", field2=123)
```

## Performance Considerations

### Concurrency
- Scanners run concurrently using ThreadPoolExecutor
- Default max workers: 10
- Thread-safe result collection using locks

### Memory
- Results stored in memory during scan
- Consider streaming for large result sets

## Future Enhancements

1. **Complete Web Server Implementation**
   - REST API using Flask or FastAPI
   - Web client serving
   - API documentation with Swagger/OpenAPI

2. **External Scanner Implementations**
   - Numverify API integration
   - Google Search integration
   - OVH API integration
   - Google Custom Search Engine

3. **Plugin System**
   - Full dynamic plugin loading
   - Plugin discovery
   - Plugin validation

4. **Testing**
   - Complete unit test coverage
   - Integration tests
   - End-to-end tests

5. **Async/Await**
   - Convert to async/await for better performance
   - Use aiohttp for HTTP requests
   - Async scanner execution

## License

GNU General Public License v3.0 (same as original project)

## Credits

Original Go project: https://github.com/sundowndev/phoneinfoga
Converted to Python by: Blackbox AI
