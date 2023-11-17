# pytket-pecos

This package enables emulation of [pytket](https://github.com/CQCL/tket)
circuits using the [PECOS](https://github.com/CQCL/PECOS) emulator.

## Installation

This package depends on a version of `quantum-pecos` that is not on PyPI,
so this must be installed manually from its repository. In full detail:

```shell

# Clone the PECOS and pytket-pecos repos and checkout the `development` branch
# of PECOS:

git clone git@github.com:PECOS-packages/PECOS.git
git -C PECOS checkout development
git clone git@github.com:CQCL/pytket-pecos.git

# Set up the virtual environment

cd pytket-pecos
python -m venv env
. env/bin/activate
pip install -U pip setuptools flit

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
