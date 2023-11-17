import unittest

from pytket.circuit import Circuit
from pytket_pecos import Emulator


class TestEmulator(unittest.TestCase):
    def test_bell(self):
        c = Circuit(2).H(0).CX(0, 1).measure_all()
        self.assertTrue(c.n_bits == 2)


if __name__ == "__main__":
    unittest.main()
