from pathlib import Path
import unittest

from pecos.error_models.generic_error_model import GenericErrorModel  # type: ignore
from pytket.circuit import Circuit, Qubit
from pytket.wasm import WasmFileHandler
from pytket_pecos import Emulator


class TestEmulator(unittest.TestCase):
    def test_bell(self):
        c = Circuit(2).H(0).CX(0, 1).measure_all()
        emu = Emulator(c)
        n_shots = 20
        results = emu.run(n_shots=n_shots)
        self.assertTrue(results.n_outcomes == n_shots)
        self.assertTrue(all(n in [0, 3] for n in results.to_intlist()))

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
        self.assertTrue(results.n_outcomes == n_shots)
        # https://github.com/PECOS-packages/PECOS/issues/89
        # self.assertEqual(sum(n in [0, 3] for n in results.to_intlist()), 62)

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
        self.assertTrue(all(n in [0, 3, 12, 15] for n in results.to_intlist()))

    def test_phasedx(self):
        c = Circuit(1).PhasedX(0.5, 0.5, 0).measure_all()
        emu = Emulator(c, qsim="state-vector")
        n_shots = 10
        results = emu.run(n_shots=n_shots)
        self.assertTrue(results.n_outcomes == n_shots)

    def test_results_order(self):
        c = Circuit(2).X(0).measure_all()
        emu = Emulator(c)
        n_shots = 10
        results = emu.run(n_shots=n_shots)
        self.assertTrue(results.to_intlist() == [2] * n_shots)

    def test_conditional(self):
        c = Circuit(2, 2).H(0).Measure(0, 0)
        c.X(1, condition_bits=[0], condition_value=1).Measure(1, 1)
        emu = Emulator(c)
        n_shots = 10
        results = emu.run(n_shots=n_shots)
        self.assertTrue(all(n in [0, 3] for n in results.to_intlist()))

    def test_setbits(self):
        # https://github.com/CQCL/pytket-pecos/issues/9
        c = Circuit(1)
        a = c.add_c_register("a", 3)
        b = c.add_c_register("b", 3)
        c.add_c_setbits([True, True, False], a)
        c.add_c_copyreg(a, b)
        emu = Emulator(c)
        result = emu.run(n_shots=1).to_intlist()[0]
        assert result == 0b110110

    def test_wasm(self):
        wasmfile = WasmFileHandler(str(Path(__file__).parent / "wasm" / "add1.wasm"))
        c = Circuit(1)
        a = c.add_c_register("a", 8)
        c.add_c_setreg(23, a)
        c.add_wasm_to_reg("add_one", wasmfile, [a], [a])
        c.X(0)
        c.Measure(Qubit(0), a[0])
        emu = Emulator(c, wasm=wasmfile)
        result = emu.run(n_shots=1).to_intlist()[0]
        assert result == 0b10011000

    def test_multithreading(self):
        c = Circuit(2).H(0).CX(0, 1).measure_all()
        emu = Emulator(c)
        n_shots = 1000
        results = emu.run(n_shots=n_shots, multithreading=True)
        self.assertTrue(results.n_outcomes == n_shots)
        self.assertTrue(all(n in [0, 3] for n in results.to_intlist()))


if __name__ == "__main__":
    unittest.main()
