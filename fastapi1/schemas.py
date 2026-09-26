from pydantic import BaseModel, ConfigDict, Field, model_validator
class ItemCriacao(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
    nome: str = Field(min_length=1, max_length=100)
    preco: float = Field(gt=0)
    em_oferta: bool = False
class ItemAtualizacao(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
    nome: str | None = Field(default=None, min_length=1, max_length=100)
    preco: float | None = Field(default=None, gt=0)
    em_oferta: bool | None = Field(default=None)
    @model_validator(mode='after')
    def validar_sem_nulos(self):
        dados = self.model_dump(exclude_unset=True)
        if any(valor is None for valor in dados.values()):
            raise ValueError('valor nulo não permitido')
        return self
class ItemResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    preco: float
    em_oferta: bool
