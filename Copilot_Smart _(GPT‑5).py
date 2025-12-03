import pytest
from test import User, UserService, ValidationError


# ---------------------------
# 1 — Testes de Sucesso
# ---------------------------

def test_criar_usuario_valido_sem_id():
    service = UserService()
    usuario = {"nome": "Ana Maria", "email": "ana.maria@example.com", "idade": 30}
    user = service.criarUsuario(usuario)
    assert isinstance(user, User)
    assert user.id is not None
    assert user.ativo is True
    assert service.buscarUsuario(user.id) == user


def test_criar_usuario_valido_com_id():
    service = UserService()
    usuario = {
        "id": "fixed-id-123",
        "nome": "Bruno Silva",
        "email": "bruno.silva@example.com",
        "idade": 25,
        "ativo": False,
    }
    user = service.criarUsuario(usuario)
    assert user.id == "fixed-id-123"
    assert user.ativo is False
    assert service.buscarUsuario("fixed-id-123") == user


def test_buscar_usuario_existente():
    service = UserService()
    usuario = {"nome": "Carlos", "email": "carlos@example.com", "idade": 40}
    user = service.criarUsuario(usuario)
    found = service.buscarUsuario(user.id)
    assert found == user


def test_atualizar_usuario_parcial():
    service = UserService()
    usuario = {"nome": "Daniel", "email": "daniel@example.com", "idade": 22}
    user = service.criarUsuario(usuario)
    updated = service.atualizarUsuario(user.id, {"nome": "Nome Atualizado"})
    assert updated.nome == "Nome Atualizado"
    assert updated.email == user.email
    assert updated.idade == user.idade


def test_atualizar_usuario_todos_campos():
    service = UserService()
    usuario = {"nome": "Eva", "email": "eva@example.com", "idade": 28}
    user = service.criarUsuario(usuario)
    updated = service.atualizarUsuario(
        user.id,
        {"nome": "Carlos", "email": "carlos@example.com", "idade": 40, "ativo": False},
    )
    assert updated.nome == "Carlos"
    assert updated.email == "carlos@example.com"
    assert updated.idade == 40
    assert updated.ativo is False
    assert updated.id == user.id


def test_excluir_usuario_existente():
    service = UserService()
    usuario = {"nome": "Fernanda", "email": "fernanda@example.com", "idade": 35}
    user = service.criarUsuario(usuario)
    assert service.excluirUsuario(user.id) is True
    assert service.buscarUsuario(user.id) is None


def test_criar_usuario_ignora_campos_extras():
    service = UserService()
    usuario = {"nome": "Debora", "email": "debora@example.com", "idade": 22, "extra": "ignore-me"}
    user = service.criarUsuario(usuario)
    assert not hasattr(user, "extra")


# ---------------------------
# 2 — Testes de Erro
# ---------------------------

def test_nome_nao_string():
    service = UserService()
    with pytest.raises(ValidationError):
        service.criarUsuario({"nome": 123, "email": "valid@example.com", "idade": 20})


def test_nome_curto():
    service = UserService()
    with pytest.raises(ValidationError):
        service.criarUsuario({"nome": "A", "email": "valid@example.com", "idade": 20})


def test_nome_longo():
    service = UserService()
    with pytest.raises(ValidationError):
        service.criarUsuario({"nome": "X" * 101, "email": "valid@example.com", "idade": 20})


def test_email_invalido_sem_arroba():
    service = UserService()
    with pytest.raises(ValidationError):
        service.criarUsuario({"nome": "João", "email": "joao.example.com", "idade": 22})


def test_email_invalido_com_espaco():
    service = UserService()
    with pytest.raises(ValidationError):
        service.criarUsuario({"nome": "Maria", "email": "maria @example.com", "idade": 22})


def test_idade_nao_inteiro():
    service = UserService()
    with pytest.raises(ValidationError):
        service.criarUsuario({"nome": "Pedro", "email": "pedro@example.com", "idade": "18"})


def test_idade_menor_que_18():
    service = UserService()
    with pytest.raises(ValidationError):
        service.criarUsuario({"nome": "Luisa", "email": "luisa@example.com", "idade": 17})


def test_ativo_nao_booleano():
    service = UserService()
    with pytest.raises(ValidationError):
        service.criarUsuario({"nome": "Nina", "email": "nina@example.com", "idade": 21, "ativo": "true"})


def test_id_duplicado():
    service = UserService()
    usuario1 = {"id": "dup", "nome": "A", "email": "a@example.com", "idade": 30}
    usuario2 = {"id": "dup", "nome": "B", "email": "b@example.com", "idade": 35}
    service.criarUsuario(usuario1)
    with pytest.raises(ValidationError):
        service.criarUsuario(usuario2)


def test_atualizar_usuario_inexistente():
    service = UserService()
    with pytest.raises(KeyError):
        service.atualizarUsuario("nao-existe", {"nome": "Novo"})


def test_atualizar_email_invalido():
    service = UserService()
    user = service.criarUsuario({"nome": "Teste", "email": "teste@example.com", "idade": 20})
    with pytest.raises(ValidationError):
        service.atualizarUsuario(user.id, {"email": "invalido"})


def test_atualizar_idade_invalida():
    service = UserService()
    user = service.criarUsuario({"nome": "Teste", "email": "teste@example.com", "idade": 20})
    with pytest.raises(ValidationError):
        service.atualizarUsuario(user.id, {"idade": 17})


def test_atualizar_ativo_invalido():
    service = UserService()
    user = service.criarUsuario({"nome": "Teste", "email": "teste@example.com", "idade": 20})
    with pytest.raises(ValidationError):
        service.atualizarUsuario(user.id, {"ativo": "False"})


# ---------------------------
# 3 — Casos de Borda
# ---------------------------

def test_nome_com_espacos():
    service = UserService()
    user = service.criarUsuario({"nome": "  Ana  ", "email": "ana@example.com", "idade": 18})
    assert user.nome.strip() == "Ana"


def test_nome_dois_caracteres():
    service = UserService()
    user = service.criarUsuario({"nome": "AB", "email": "ab@example.com", "idade": 18})
    assert user.nome == "AB"


def test_nome_cem_caracteres():
    service = UserService()
    nome = "N" * 100
    user = service.criarUsuario({"nome": nome, "email": "n100@example.com", "idade": 18})
    assert user.nome == nome


def test_email_com_subdominio():
    service = UserService()
    user = service.criarUsuario({"nome": "Ed", "email": "ed@mail.example.com", "idade": 19})
    assert user.email == "ed@mail.example.com"


def test_email_com_tld_longo():
    service = UserService()
    user = service.criarUsuario({"nome": "Tami", "email": "tami@example.technology", "idade": 30})
    assert user.email.endswith(".technology")


def test_criar_sem_ativo():
    service = UserService()
    user = service.criarUsuario({"nome": "Leo", "email": "leo@example.com", "idade": 28})
    assert user.ativo is True


def test_atualizar_ignora_extras():
    service = UserService()
    user = service.criarUsuario({"nome": "Leo", "email": "leo@example.com", "idade": 28})
    updated = service.atualizarUsuario(user.id, {"apelido": "Leo", "cidade": "SP", "nome": "Leonardo"})
    assert updated.nome == "Leonardo"
    assert not hasattr(updated, "apelido")


def test_atualizar_payload_vazio():
    service = UserService()
    user = service.criarUsuario({"nome": "Leo", "email": "leo@example.com", "idade": 28})
    updated = service.atualizarUsuario(user.id, {})
    assert updated == user


def test_buscar_inexistente():
    service = UserService()
    assert service.buscarUsuario("inexistente") is None


def test_excluir_inexistente():
    service = UserService()
    assert service.excluirUsuario("inexistente") is False


def test_atualizar_nao_altera_id():
    service = UserService()
    user = service.criarUsuario