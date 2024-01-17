# pytket-pecos

This package enables emulation of [pytket](https://github.com/CQCL/tket)
circuits using the
[PECOS](https://github.com/PECOS-packages/PECOS/tree/development) emulator.

## Installation

Installation requires Python 3.10, 3.11 or 3.12. Linux, MacOS and Windows are
all supported.

### From pypi

```shell
pip install pytket_pecos
```

### From source

```shell

# Clone the pytket-pecos repo:

git clone git@github.com:CQCL/pytket-pecos.git

# Set up the virtual environment

cd pytket-pecos
python -m venv env
. env/bin/activate
pip install -U pip flit wheel

# Install pytket-pecos

flit install
```

## Testing

To run the unit tests:

```shell
python -m unittest test.test_emulator
```
