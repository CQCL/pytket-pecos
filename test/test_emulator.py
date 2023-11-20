import unittest

from pecos.error_models.generic_error_model import GenericErrorModel
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

    def test_bell_with_noise(self):
        c = Circuit(2).H(0).CX(0, 1).measure_all()
        error_model = GenericErrorModel(
            error_params={
                "p1": 2e-1,
                "p2": 2e-1,
                "p_meas": 2e-1,
                "p_init": 1e-1,
                "p1_error_model": {
                    "X": 0.25,
                    "Y": 0.25,
                    "Z": 0.25,
                    "L": 0.25,
                },
            },
        )
        emu = Emulator(c, error_model=error_model, seed=7)
        n_shots = 100
        results = emu.run(n_shots=n_shots)
        self.assertTrue(list(results.keys()) == ["c"])
        vals = results["c"]
        self.assertTrue(len(vals) == n_shots)
        self.assertTrue(len([(c0, c1) for (c0, c1) in vals if c0 == c1]) == 88)


if __name__ == "__main__":
    unittest.main()
