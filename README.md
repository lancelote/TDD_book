[![Requirements Status](https://requires.io/github/lancelote/TDD_book/requirements.svg?branch=master)](https://requires.io/github/lancelote/TDD_book/requirements/?branch=master)
[![Build Status](https://travis-ci.org/lancelote/TDD_book.svg)](https://travis-ci.org/lancelote/TDD_book)

# TDD_book

Code for "Test-Driven Development with Python" book by Harry J.W. Percival

## ToDo List

- [ ] Check native test runners
- [ ] Staging version
- [ ] Refactor Qunit test code
- [ ] JavaScript style validation
- [ ] HTML style validation
- [ ] JavaScript tests automation
- [x] Hide error after user click inside field
- [x] Remove duplication of validation logic in views
- [x] Remove hardcoded URLs from views.py
- [x] Remove hardcoded URLs from forms in list.html and home.html

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
