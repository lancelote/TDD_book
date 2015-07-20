[![Requirements Status](https://requires.io/github/lancelote/TDD_book/requirements.svg?branch=master)](https://requires.io/github/lancelote/TDD_book/requirements/?branch=master)
[![Build Status](https://travis-ci.org/lancelote/TDD_book.svg)](https://travis-ci.org/lancelote/TDD_book)

# TDD_book

Code for "Test-Driven Development with Python" book by Harry J.W. Percival

## ToDo List

- [ ] Remove hardcoded URLs from views.py
- [ ] Remove hardcoded URLs from forms in list.html and home.html
- [ ] Remove duplication of validation logic in views

## Testing

Do not forget:
```bash
pip install -r requirements.txt
```

### Unit testing
```bash
paver unit
```

### Acceptance testing
```bash
paver accept
```

Liveserver:
```bash
paver accept --liveserver=example.com
```

### Style validation (PEP8)
```bash
paver style
```

### Everything
```bash
paver
```
