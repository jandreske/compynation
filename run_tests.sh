cd "${BASH_SOURCE%/*}/" || exit
PYTHONPATH='src' python3 -m pytest tests/