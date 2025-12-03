import pytest
from test import UserService, ValidationError


# ------------------------------------------------------------------------------
# 1 — TESTES DE SUCESSO
# ------------------------------------------------------------------------------

def test_criar_usuario_valido_completo():
    service = UserService()
    entrada = {"nome": "Renan", "email": "renan@example.com", "idade": 25, "ativo": True}

    user = service.criarUsuario(entrada)

    assert user.id is not None
    assert user.nome == "Renan"
    assert user.email == "renan@example.com"
    assert user.idade == 25
    assert user.ativo is True


def test_criar_usuario_id_custom_inexistente():
    service = UserService()
    entrada = {"id": "123", "nome": "Maria", "email": "maria@example.com", "idade": 30}

    user = service.criarUsuario(entrada)

    assert user.id == "123"
    assert user.nome == "Maria"


def test_buscar_usuario_existente():
    service = UserService()
    user = service.criarUsuario({"nome": "A", "email": "a@a.com", "idade": 20})

    result = service.buscarUsuario(user.id)

    assert result is not None
    assert result.id == user.id


def test_atualizar_usuario_existente():
    service = UserService()
    user = service.criarUsuario({"nome": "Renan", "email": "r@a.com", "idade": 20})

    atualizado = service.atualizarUsuario(user.id, {"nome": "Renan Silva"})

    assert atualizado.nome == "Renan Silva"
    assert atualizado.email == user.email   # não deve mudar
    assert atualizado.id == user.id


def test_excluir_usuario_existente():
    service = UserService()
    user = service.criarUsuario({"nome": "R", "email": "r@r.com", "idade": 20})

    result = service.excluirUsuario(user.id)

    assert result is True
    assert service.buscarUsuario(user.id) is None


# ------------------------------------------------------------------------------
# 2 — TESTES DE ERRO
# ------------------------------------------------------------------------------

def test_criar_usuario_nome_invalido_curto():
    service = UserService()
    entrada = {"nome": "A", "email": "a@example.com", "idade": 20}

    with pytest.raises(ValidationError):
        service.criarUsuario(entrada)


def test_criar_usuario_email_invalido():
    service = UserService()
    entrada = {"nome": "João", "email": "email_invalido", "idade": 25}

    with pytest.raises(ValidationError):
        service.criarUsuario(entrada)


def test_criar_usuario_idade_menor_que_18():
    service = UserService()
    entrada = {"nome": "Ana", "email": "ana@example.com", "idade": 17}

    with pytest.raises(ValidationError):
        service.criarUsuario(entrada)


def test_criar_usuario_ativo_invalido():
    service = UserService()
    entrada = {"nome": "Eli", "email": "eli@example.com", "idade": 25, "ativo": "sim"}

    with pytest.raises(ValidationError):
        service.criarUsuario(entrada)


def test_criar_usuario_id_duplicado():
    service = UserService()
    entrada = {"id": "x1", "nome": "A", "email": "a@a.com", "idade": 25}

    service.criarUsuario(entrada)

    with pytest.raises(ValidationError):
        service.criarUsuario(entrada)


def test_atualizar_usuario_inexistente():
    service = UserService()

    with pytest.raises(KeyError):
        service.atualizarUsuario("naoexiste", {"nome": "Teste"})


# ------------------------------------------------------------------------------
# 3 — CASOS DE BORDA
# ------------------------------------------------------------------------------

def test_criar_usuario_nome_2_caracteres():
    service = UserService()
    entrada = {"nome": "Al", "email": "al@example.com", "idade": 18}

    user = service.criarUsuario(entrada)
    assert user.nome == "Al"


def test_criar_usuario_nome_100_caracteres():
    service = UserService()
    nome = "A" * 100
    entrada = {"nome": nome, "email": "a@a.com", "idade": 18}

    user = service.criarUsuario(entrada)
    assert len(user.nome) == 100


def test_criar_usuario_idade_18():
    service = UserService()
    entrada = {"nome": "Teste", "email": "t@t.com", "idade": 18}

    user = service.criarUsuario(entrada)
    assert user.idade == 18


def test_buscar_usuario_inexistente():
    service = UserService()

    result = service.buscarUsuario("naoexiste")

    assert result is None


def test_excluir_usuario_inexistente():
    service = UserService()

    result = service.excluirUsuario("ghost")

    assert result is False


# ------------------------------------------------------------------------------
# 4 — TESTES POR MÉTODO (COBERTURA TOTAL)
# ------------------------------------------------------------------------------

def test_criarUsuario_campos_minimos():
    service = UserService()
    entrada = {"nome": "Leo", "email": "leo@a.com", "idade": 20}

    user = service.criarUsuario(entrada)

    assert user.ativo is True  # default
    assert isinstance(user.id, str)


def test_buscarUsuario_retorno_none():
    service = UserService()

    assert service.buscarUsuario("x") is None


def test_atualizarUsuario_multiplos_campos():
    service = UserService()
    user = service.criarUsuario({"nome": "A", "email": "a@a.com", "idade": 20})

    atualizado = service.atualizarUsuario(user.id, {
        "nome": "B",
        "email": "b@b.com",
        "idade": 30,
        "ativo": False
    })

    assert atualizado.nome == "B"
    assert atualizado.email == "b@b.com"
    assert atualizado.idade == 30
    assert atualizado.ativo is False


def test_excluirUsuario_depois_de_atualizar():
    service = UserService()
    user = service.criarUsuario({"nome": "X", "email": "x@x.com", "idade": 20})

    service.atualizarUsuario(user.id, {"nome": "Novo"})
    assert service.excluirUsuario(user.id) is True
    assert service.buscarUsuario(user.id) is None
