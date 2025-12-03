from dataclasses import dataclass, asdict
from typing import Optional, Dict
import re
import uuid


class ValidationError(ValueError):
    pass


EMAIL_RE = re.compile(r"^[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+$")


def _validate_name(name: str):
    if not isinstance(name, str):
        raise ValidationError("nome deve ser string")
    length = len(name.strip())
    if length < 2 or length > 100:
        raise ValidationError("nome deve ter entre 2 e 100 caracteres")


def _validate_email(email: str):
    if not isinstance(email, str) or not EMAIL_RE.match(email):
        raise ValidationError("email em formato inválido")


def _validate_idade(idade: int):
    if not isinstance(idade, int):
        raise ValidationError("idade deve ser inteiro")
    if idade < 18:
        raise ValidationError("idade mínima é 18 anos")


def _validate_ativo(ativo: bool):
    if not isinstance(ativo, bool):
        raise ValidationError("ativo deve ser booleano")


@dataclass
class User:
    id: str
    nome: str
    email: str
    idade: int
    ativo: bool = True

    def __post_init__(self):
        _validate_name(self.nome)
        _validate_email(self.email)
        _validate_idade(self.idade)
        _validate_ativo(self.ativo)

    def to_dict(self):
        return asdict(self)


class UserService:
    def __init__(self):
        self._store: Dict[str, User] = {}

    def _normalize_user_payload(self, payload: dict) -> dict:
        allowed = {"id", "nome", "email", "idade", "ativo"}
        return {k: v for k, v in payload.items() if k in allowed}

    def criarUsuario(self, usuario: dict) -> User:
        payload = self._normalize_user_payload(usuario)
        uid = payload.get("id") or str(uuid.uuid4())

        if uid in self._store:
            raise ValidationError("id já existe")

        payload["id"] = uid
        if "ativo" not in payload:
            payload["ativo"] = True

        user = User(**payload)
        self._store[user.id] = user
        return user

    def buscarUsuario(self, id: str) -> Optional[User]:
        return self._store.get(id)

    def atualizarUsuario(self, id: str, usuario: dict) -> User:
        if id not in self._store:
            raise KeyError("usuario não encontrado")

        payload = self._normalize_user_payload(usuario)
        payload["id"] = id

        merged = self._store[id].to_dict()
        merged.update(payload)

        updated = User(**merged)
        self._store[id] = updated
        return updated

    def excluirUsuario(self, id: str) -> bool:
        return self._store.pop(id, None) is not None
