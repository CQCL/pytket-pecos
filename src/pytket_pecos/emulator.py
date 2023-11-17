from pecos.engines.hybrid_engine import HybridEngine
from pytket.circuit import Circuit
from pytket.phir.api import pytket_to_phir


class Emulator:
    def __init__(self, circuit: Circuit):
        self.phir = pytket_to_phir(circuit)
        self.engine = HybridEngine()

    def run(self, n_shots):
        return self.engine.run(self.phir, shots=n_shots)
