# pytket-pecos

This package enables emulation of [pytket](https://github.com/CQCL/tket)
circuits using the [PECOS](https://github.com/CQCL/PECOS) emulator.

## Installation

This package depends on versions of `pytket-phir` and `quantum-pecos` that are
not on PyPI, so these must be installed manually from their respective
repositories. In full detail:

```shell

# Clone the three repos and checkout the `development` branch of PECOS:

git clone git@github.com:CQCL/pytket-phir.git
git clone git@github.com:PECOS-packages/PECOS.git
git -C PECOS checkout development
git clone git@github.com:CQCL/pytket-pecos.git

# Set up the virtual environment

cd pytket-pecos
python -m venv env
. env/bin/activate
pip install -U pip setuptools flit

# Install pytket-phir:

pip install -r ../pytket-phir/requirements.txt
pip install -e ../pytket-phir/

# Install quantum-pecos:

pip install -r ../PECOS/requirements.txt
pip install -e ../PECOS/

# Install pytket-pecos

flit install
```

## Testing

To run the unit tests:

```shell
python -m unittest test.test_emulator
```
