from dataclasses import dataclass


@dataclass
class Collegamento:
    id_filiale_1: int
    id_filiale_2: int
    somma_importi: float
    num_bonifici: int

    @property
    def valore(self) -> float:
        return self.somma_importi / self.num_bonifici if self.num_bonifici > 0 else 0.0
