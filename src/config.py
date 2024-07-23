from dataclasses import dataclass

@dataclass
class Data:
    raw: str
    processed: str
    final: str

@dataclass
class Model:
    name: str

@dataclass
class OnlineRetailConfig:
    data: Data
    model: Model
