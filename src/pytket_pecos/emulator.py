from collections import defaultdict
from typing import Optional
from pecos.engines.hybrid_engine import HybridEngine  # type: ignore
from pecos.error_models.error_model_abc import ErrorModel  # type: ignore
from pytket.circuit import Circuit
from pytket.phir.api import pytket_to_phir
from pytket.utils.outcomearray import OutcomeArray


def is_reglike(units):
    regmap = defaultdict(set)
    for unit in units:
        if len(unit.index) != 1:
            return False
        regmap[unit.reg_name].add(unit.index[0])
    return all(indices == set(range(len(indices))) for indices in regmap.values())


class Emulator:
    def __init__(
        self,
        circuit: Circuit,
        error_model: Optional[ErrorModel] = None,
        qsim: str = "stabilizer",
        seed: Optional[int] = None,
    ):
        if (not is_reglike(circuit.qubits)) or (not is_reglike(circuit.bits)):
            raise ValueError("Circuit contains units that do not belong to a register.")

        self.phir = pytket_to_phir(circuit)
        self.engine = HybridEngine(qsim=qsim, error_model=error_model)
        self.engine.use_seed(seed)

    def run(self, n_shots) -> OutcomeArray:
        results = self.engine.run(self.phir, shots=n_shots)
        c_regs = sorted(results.keys())
        readouts = []
        for i in range(n_shots):
            readout = []
            for c_reg in c_regs:
                readout.extend(reversed(list(map(int, results[c_reg][i]))))
            readouts.append(readout)
        return OutcomeArray.from_readouts(readouts)
