import unittest

from pecos.error_models.generic_error_model import GenericErrorModel  # type: ignore
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

    def test_multi_reg(self):
        c = Circuit()
        q0 = c.add_q_register("q0", 2)
        q1 = c.add_q_register("q1", 2)
        c0 = c.add_c_register("c0", 2)
        c1 = c.add_c_register("c1", 2)
        c.H(q0[0]).CX(q0[0], q0[1]).Measure(q0[0], c0[0]).Measure(q0[1], c0[1])
        c.H(q1[0]).CX(q1[0], q1[1]).Measure(q1[0], c1[0]).Measure(q1[1], c1[1])
        emu = Emulator(c)
        results = emu.run(n_shots=20)
        self.assertTrue(all(m0 == m1 for m0, m1 in results["c0"]))
        self.assertTrue(all(m0 == m1 for m0, m1 in results["c1"]))


if __name__ == "__main__":
    unittest.main()
