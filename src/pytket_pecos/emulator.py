from pecos.engines.hybrid_engine import HybridEngine  # type: ignore
from pecos.error_models.error_model_abc import ErrorModel  # type: ignore
from pytket.circuit import Circuit
from pytket.phir.api import pytket_to_phir
from typing import Optional


class Emulator:
    def __init__(
        self,
        circuit: Circuit,
        error_model: Optional[ErrorModel] = None,
        seed: Optional[int] = None,
    ):
        self.phir = pytket_to_phir(circuit)
        self.engine = HybridEngine(error_model=error_model)
        self.engine.use_seed(seed)

    def run(self, n_shots):
        return self.engine.run(self.phir, shots=n_shots)
