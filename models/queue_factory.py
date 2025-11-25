from typing import Any, Dict, Type

from models.base_queue import BaseQueueModel
from models.mcpci import mcpci
from models.mcpsi import mcpsi
from models.mg1 import MG1
from models.mm1 import MM1
from models.mm1k import MM1K
from models.mm1n import MM1N
from models.mms import MMS
from models.mmsk import MMsK
from models.mmsn import MMSN


class QueueFactory:
    """Factory para criar instâncias de modelos de fila"""

    _models: Dict[str, Type[BaseQueueModel]] = {
        "MM1": MM1,
        "MMS": MMS,
        "MM1K": MM1K,
        "MM1N": MM1N,
        "MMSK": MMsK,
        "MMSN": MMSN,
        "MG1": MG1,
        "MCPCI": mcpci,
        "MCPSI": mcpsi,
    }

    @classmethod
    def create_queue(cls, model_type: str, **params) -> BaseQueueModel:
        """
        Cria uma instância de fila baseado no tipo de modelo

        Args:
            model_type: Tipo do modelo (ex: 'MM1', 'MM1K', etc)
            **params: Parâmetros necessários para o modelo

        Returns:
            Instância do modelo de fila

        Raises:
            ValueError: Se o modelo não for suportado
        """
        if model_type not in cls._models:
            raise ValueError(
                f"Modelo '{model_type}' não suportado. "
                f"Modelos disponíveis: {', '.join(cls._models.keys())}"
            )

        model_class = cls._models[model_type]

        try:
            return model_class(**params)
        except TypeError as e:
            raise ValueError(
                f"Parâmetros inválidos para o modelo {model_type}: {str(e)}"
            )

    @classmethod
    def get_available_models(cls) -> list:
        return list(cls._models.keys())

    @classmethod
    def get_model_info(cls, model_type: str) -> Dict[str, Any]:
        model_info = {
            "MM1": {
                "name": "M/M/1",
                "description": "Fila com chegadas Poisson, atendimento exponencial, 1 servidor",
                "params": ["lamb", "mu", "n", "r", "t", "k", "s"],
                "required": ["lamb", "mu"],
            },
            "MMS": {
                "name": "M/M/s",
                "description": "Fila com s servidores (s > 1)",
                "params": ["lamb", "mu", "s", "n", "r", "t", "k"],
                "required": ["lamb", "mu", "s"],
            },
            "MM1K": {
                "name": "M/M/1/K",
                "description": "Fila M/M/1 com capacidade finita K",
                "params": ["lamb", "mu", "k", "n", "s"],
                "required": ["lamb", "mu", "k"],
            },
            "MM1N": {
                "name": "M/M/1/N",
                "description": "Fila M/M/1 com população finita N",
                "params": ["lamb", "mu", "n", "N", "k", "s"],
                "required": ["lamb", "mu", "N"],
            },
            "MMSK": {
                "name": "M/M/s/K",
                "description": "Fila com s servidores e capacidade finita K",
                "params": ["lamb", "mu", "s", "k", "n"],
                "required": ["lamb", "mu", "s", "k"],
            },
            "MMSN": {
                "name": "M/M/s/N",
                "description": "Fila com s servidores e população finita N",
                "params": ["lamb", "mu", "s", "n", "N", "k"],
                "required": ["lamb", "mu", "s", "N"],
            },
            "MG1": {
                "name": "M/G/1",
                "description": "Fila com chegadas Poisson e tempo de serviço geral",
                "params": ["lamb", "mu", "k", "s"],
                "required": ["lamb", "mu"],
            },
            "MCPCI": {
                "name": "Modelo com Prioridades (Classes Independentes)",
                "description": "Modelo de prioridades com classes independentes",
                "params": ["lamb", "mu", "s", "k", "lamb_list"],
                "required": ["lamb", "mu", "s", "k", "lamb_list"],
            },
            "MCPSI": {
                "name": "Modelo com Prioridades (Sistema Integrado)",
                "description": "Modelo de prioridades com sistema integrado",
                "params": ["lamb", "mu", "s", "k", "lamb_list"],
                "required": ["lamb", "mu", "s", "k", "lamb_list"],
            },
        }

        return model_info.get(model_type, {})
