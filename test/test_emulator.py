import unittest

from pytket.circuit import Circuit
from pytket_pecos import Emulator


class TestEmulator(unittest.TestCase):
    def test_bell(self):
        c = Circuit(2).H(0).CX(0, 1).measure_all()
        emu = Emulator(c)
        n_shots = 20
        results = emu.run(n_shots=n_shots)
        self.assertTrue(list(results.keys()) == ["c"])
        vals = results["c"]
        self.assertTrue(len(vals) == n_shots)
        self.assertTrue(all(c0 == c1 for (c0, c1) in vals))


if __name__ == "__main__":
    unittest.main()
