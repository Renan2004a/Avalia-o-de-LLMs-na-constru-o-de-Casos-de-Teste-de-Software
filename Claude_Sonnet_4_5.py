import pytest
import uuid
from user_service import UserService, ValidationError, User


class TestUserService:
    
    # GRUPO 1: TESTES DE SUCESSO
    
    def test_criar_usuario_completo_sucesso(self):
        """Teste 1.1: Criar usuário com todos os campos válidos"""
        # Instanciar UserService
        service = UserService()
        
        # Chamar criarUsuario com payload válido
        payload = {
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25,
            "ativo": True
        }
        usuario = service.criarUsuario(payload)
        
        # Verificar retorno
        assert usuario is not None
        assert isinstance(usuario, User)
        assert usuario.id is not None
        assert usuario.nome == "João Silva"
        assert usuario.email == "joao@example.com"
        assert usuario.idade == 25
        assert usuario.ativo == True
        
        # Verificar se usuário está armazenado no _store
        usuario_store = service._store.get(usuario.id)
        assert usuario_store is not None
        assert usuario_store.nome == "João Silva"

    def test_criar_usuario_sem_ativo_usa_padrao(self):
        """Teste 1.2: Criar usuário sem campo 'ativo' (deve usar padrão True)"""
        service = UserService()
        
        payload = {
            "nome": "Maria Santos",
            "email": "maria@example.com",
            "idade": 30
        }
        usuario = service.criarUsuario(payload)
        
        assert usuario is not None
        assert usuario.ativo == True  # valor padrão

    def test_criar_usuario_com_id_fornecido(self):
        """Teste 1.3: Criar usuário com ID fornecido manualmente"""
        service = UserService()
        
        payload = {
            "id": "user-123",
            "nome": "Carlos Mendes",
            "email": "carlos@example.com",
            "idade": 40
        }
        usuario = service.criarUsuario(payload)
        
        assert usuario.id == "user-123"
        # Verificar que não foi gerado automaticamente
        assert usuario.id == "user-123"

    def test_criar_usuario_inativo(self):
        """Teste 1.4: Criar usuário com ativo=False"""
        service = UserService()
        
        payload = {
            "nome": "Ana Paula",
            "email": "ana@example.com",
            "idade": 28,
            "ativo": False
        }
        usuario = service.criarUsuario(payload)
        
        assert usuario.ativo == False

    def test_buscar_usuario_existente(self):
        """Teste 1.5: Buscar usuário existente"""
        service = UserService()
        
        # Criar usuário
        payload = {
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25
        }
        usuario_criado = service.criarUsuario(payload)
        usuario_id = usuario_criado.id
        
        # Buscar usuário
        usuario_encontrado = service.buscarUsuario(usuario_id)
        
        assert usuario_encontrado is not None
        assert isinstance(usuario_encontrado, User)
        assert usuario_encontrado.id == usuario_id
        assert usuario_encontrado.nome == "João Silva"

    def test_atualizar_nome_usuario(self):
        """Teste 1.6: Atualizar nome de usuário existente"""
        service = UserService()
        
        # Criar usuário
        payload = {
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25,
            "ativo": True
        }
        usuario_criado = service.criarUsuario(payload)
        usuario_id = usuario_criado.id
        
        # Atualizar nome
        update_payload = {
            "nome": "João Silva Atualizado"
        }
        service.atualizarUsuario(usuario_id, update_payload)
        
        # Buscar e verificar
        usuario_atualizado = service.buscarUsuario(usuario_id)
        assert usuario_atualizado.nome == "João Silva Atualizado"
        assert usuario_atualizado.email == "joao@example.com"  # inalterado
        assert usuario_atualizado.idade == 25  # inalterado
        assert usuario_atualizado.ativo == True  # inalterado
        assert usuario_atualizado.id == usuario_id  # ID permanece

    def test_atualizar_email_usuario(self):
        """Teste 1.7: Atualizar email de usuário existente"""
        service = UserService()
        
        usuario_criado = service.criarUsuario({
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25
        })
        
        update_payload = {
            "email": "novo.email@example.com"
        }
        service.atualizarUsuario(usuario_criado.id, update_payload)
        
        usuario_atualizado = service.buscarUsuario(usuario_criado.id)
        assert usuario_atualizado.email == "novo.email@example.com"
        assert usuario_atualizado.nome == "João Silva"  # inalterado

    def test_atualizar_idade_usuario(self):
        """Teste 1.8: Atualizar idade de usuário existente"""
        service = UserService()
        
        usuario_criado = service.criarUsuario({
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25
        })
        
        update_payload = {
            "idade": 35
        }
        service.atualizarUsuario(usuario_criado.id, update_payload)
        
        usuario_atualizado = service.buscarUsuario(usuario_criado.id)
        assert usuario_atualizado.idade == 35

    def test_atualizar_status_ativo(self):
        """Teste 1.9: Atualizar status ativo de usuário"""
        service = UserService()
        
        usuario_criado = service.criarUsuario({
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25,
            "ativo": True
        })
        
        update_payload = {
            "ativo": False
        }
        service.atualizarUsuario(usuario_criado.id, update_payload)
        
        usuario_atualizado = service.buscarUsuario(usuario_criado.id)
        assert usuario_atualizado.ativo == False

    def test_atualizar_multiplos_campos(self):
        """Teste 1.10: Atualizar múltiplos campos simultaneamente"""
        service = UserService()
        
        usuario_criado = service.criarUsuario({
            "nome": "Nome Antigo",
            "email": "antigo@example.com",
            "idade": 30,
            "ativo": True
        })
        
        update_payload = {
            "nome": "Nome Novo",
            "email": "novoemail@example.com",
            "idade": 45
        }
        service.atualizarUsuario(usuario_criado.id, update_payload)
        
        usuario_atualizado = service.buscarUsuario(usuario_criado.id)
        assert usuario_atualizado.nome == "Nome Novo"
        assert usuario_atualizado.email == "novoemail@example.com"
        assert usuario_atualizado.idade == 45
        assert usuario_atualizado.ativo == True  # inalterado

    def test_excluir_usuario_existente(self):
        """Teste 1.11: Excluir usuário existente"""
        service = UserService()
        
        usuario_criado = service.criarUsuario({
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25
        })
        usuario_id = usuario_criado.id
        
        # Excluir usuário
        resultado = service.excluirUsuario(usuario_id)
        
        assert resultado == True
        # Verificar que usuário não está mais no store
        usuario_excluido = service.buscarUsuario(usuario_id)
        assert usuario_excluido is None

    def test_criar_multiplos_usuarios(self):
        """Teste 1.12: Criar múltiplos usuários"""
        service = UserService()
        
        usuarios_payload = [
            {
                "nome": "Usuário 1",
                "email": "user1@example.com",
                "idade": 25
            },
            {
                "nome": "Usuário 2",
                "email": "user2@example.com",
                "idade": 30
            },
            {
                "nome": "Usuário 3",
                "email": "user3@example.com",
                "idade": 35
            }
        ]
        
        usuarios_criados = []
        for payload in usuarios_payload:
            usuario = service.criarUsuario(payload)
            usuarios_criados.append(usuario)
        
        # Verificar que todos foram criados
        assert len(usuarios_criados) == 3
        
        # Verificar que IDs são únicos
        ids = [usuario.id for usuario in usuarios_criados]
        assert len(ids) == len(set(ids))
        
        # Verificar que todos são acessíveis
        for usuario in usuarios_criados:
            usuario_buscado = service.buscarUsuario(usuario.id)
            assert usuario_buscado is not None
            assert usuario_buscado.id == usuario.id
    
    # GRUPO 2: TESTES DE ERRO
    
    def test_criar_usuario_nome_nao_string(self):
        """Teste 2.1: Criar usuário com nome não-string"""
        service = UserService()
        
        payload = {
            "nome": 12345,
            "email": "teste@example.com",
            "idade": 25
        }
        
        with pytest.raises(ValidationError, match="nome deve ser string"):
            service.criarUsuario(payload)

    def test_criar_usuario_nome_muito_curto(self):
        """Teste 2.2: Criar usuário com nome muito curto (1 caractere)"""
        service = UserService()
        
        payload = {
            "nome": "A",
            "email": "teste@example.com",
            "idade": 25
        }
        
        with pytest.raises(ValidationError, match="nome deve ter entre 2 e 100 caracteres"):
            service.criarUsuario(payload)

    def test_criar_usuario_nome_muito_longo(self):
        """Teste 2.3: Criar usuário com nome muito longo (101 caracteres)"""
        service = UserService()
        
        payload = {
            "nome": "A" * 101,
            "email": "teste@example.com",
            "idade": 25
        }
        
        with pytest.raises(ValidationError, match="nome deve ter entre 2 e 100 caracteres"):
            service.criarUsuario(payload)

    def test_criar_usuario_nome_vazio(self):
        """Teste 2.4: Criar usuário com nome vazio"""
        service = UserService()
        
        payload = {
            "nome": "",
            "email": "teste@example.com",
            "idade": 25
        }
        
        with pytest.raises(ValidationError, match="nome deve ter entre 2 e 100 caracteres"):
            service.criarUsuario(payload)

    def test_criar_usuario_nome_apenas_espacos(self):
        """Teste 2.5: Criar usuário com nome apenas espaços"""
        service = UserService()
        
        payload = {
            "nome": "   ",
            "email": "teste@example.com",
            "idade": 25
        }
        
        with pytest.raises(ValidationError, match="nome deve ter entre 2 e 100 caracteres"):
            service.criarUsuario(payload)

    def test_criar_usuario_email_sem_arroba(self):
        """Teste 2.6: Criar usuário com email inválido (sem @)"""
        service = UserService()
        
        payload = {
            "nome": "João Silva",
            "email": "emailinvalido.com",
            "idade": 25
        }
        
        with pytest.raises(ValidationError, match="email em formato inválido"):
            service.criarUsuario(payload)

    def test_criar_usuario_email_sem_dominio(self):
        """Teste 2.7: Criar usuário com email inválido (sem domínio)"""
        service = UserService()
        
        payload = {
            "nome": "João Silva",
            "email": "email@",
            "idade": 25
        }
        
        with pytest.raises(ValidationError, match="email em formato inválido"):
            service.criarUsuario(payload)

    def test_criar_usuario_email_sem_extensao(self):
        """Teste 2.8: Criar usuário com email inválido (sem extensão)"""
        service = UserService()
        
        payload = {
            "nome": "João Silva",
            "email": "email@domain",
            "idade": 25
        }
        
        with pytest.raises(ValidationError, match="email em formato inválido"):
            service.criarUsuario(payload)

    def test_criar_usuario_email_com_espacos(self):
        """Teste 2.9: Criar usuário com email contendo espaços"""
        service = UserService()
        
        payload = {
            "nome": "João Silva",
            "email": "email @domain.com",
            "idade": 25
        }
        
        with pytest.raises(ValidationError, match="email em formato inválido"):
            service.criarUsuario(payload)

    def test_criar_usuario_email_nao_string(self):
        """Teste 2.10: Criar usuário com email não-string"""
        service = UserService()
        
        payload = {
            "nome": "João Silva",
            "email": 12345,
            "idade": 25
        }
        
        with pytest.raises(ValidationError, match="email em formato inválido"):
            service.criarUsuario(payload)

    def test_criar_usuario_idade_nao_inteiro(self):
        """Teste 2.11: Criar usuário com idade não-inteiro"""
        service = UserService()
        
        payload = {
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": "25"
        }
        
        with pytest.raises(ValidationError, match="idade deve ser inteiro"):
            service.criarUsuario(payload)

    def test_criar_usuario_idade_float(self):
        """Teste 2.12: Criar usuário com idade float"""
        service = UserService()
        
        payload = {
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25.5
        }
        
        with pytest.raises(ValidationError, match="idade deve ser inteiro"):
            service.criarUsuario(payload)

    def test_criar_usuario_idade_menor_18(self):
        """Teste 2.13: Criar usuário com idade menor que 18"""
        service = UserService()
        
        payload = {
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 17
        }
        
        with pytest.raises(ValidationError, match="idade mínima é 18 anos"):
            service.criarUsuario(payload)

    def test_criar_usuario_idade_negativa(self):
        """Teste 2.14: Criar usuário com idade negativa"""
        service = UserService()
        
        payload = {
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": -5
        }
        
        with pytest.raises(ValidationError, match="idade mínima é 18 anos"):
            service.criarUsuario(payload)

    def test_criar_usuario_ativo_nao_booleano_string(self):
        """Teste 2.15: Criar usuário com ativo não-booleano (string)"""
        service = UserService()
        
        payload = {
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25,
            "ativo": "true"
        }
        
        with pytest.raises(ValidationError, match="ativo deve ser booleano"):
            service.criarUsuario(payload)

    def test_criar_usuario_ativo_nao_booleano_numero(self):
        """Teste 2.16: Criar usuário com ativo não-booleano (número)"""
        service = UserService()
        
        payload = {
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25,
            "ativo": 1
        }
        
        with pytest.raises(ValidationError, match="ativo deve ser booleano"):
            service.criarUsuario(payload)

    def test_criar_usuario_id_duplicado(self):
        """Teste 2.17: Criar usuário com ID duplicado"""
        service = UserService()
        
        payload = {
            "id": "user-123",
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25
        }
        
        # Primeira criação deve funcionar
        service.criarUsuario(payload)
        
        # Segunda criação deve falhar
        with pytest.raises(ValidationError, match="id já existe"):
            service.criarUsuario(payload)

    def test_buscar_usuario_inexistente(self):
        """Teste 2.18: Buscar usuário inexistente"""
        service = UserService()
        
        usuario = service.buscarUsuario("id-que-nao-existe")
        
        assert usuario is None

    def test_atualizar_usuario_inexistente(self):
        """Teste 2.19: Atualizar usuário inexistente"""
        service = UserService()
        
        with pytest.raises(KeyError, match="usuario não encontrado"):
            service.atualizarUsuario("id-inexistente", {"nome": "Novo Nome"})

    def test_atualizar_usuario_nome_invalido(self):
        """Teste 2.20: Atualizar usuário com nome inválido"""
        service = UserService()
        
        usuario = service.criarUsuario({
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25
        })
        
        with pytest.raises(ValidationError, match="nome deve ter entre 2 e 100 caracteres"):
            service.atualizarUsuario(usuario.id, {"nome": "A"})

    def test_atualizar_usuario_email_invalido(self):
        """Teste 2.21: Atualizar usuário com email inválido"""
        service = UserService()
        
        usuario = service.criarUsuario({
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25
        })
        
        with pytest.raises(ValidationError, match="email em formato inválido"):
            service.atualizarUsuario(usuario.id, {"email": "email-invalido"})

    def test_atualizar_usuario_idade_menor_18(self):
        """Teste 2.22: Atualizar usuário com idade menor que 18"""
        service = UserService()
        
        usuario = service.criarUsuario({
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25
        })
        
        with pytest.raises(ValidationError, match="idade mínima é 18 anos"):
            service.atualizarUsuario(usuario.id, {"idade": 16})

    def test_atualizar_usuario_ativo_invalido(self):
        """Teste 2.23: Atualizar usuário com ativo inválido"""
        service = UserService()
        
        usuario = service.criarUsuario({
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25,
            "ativo": True
        })
        
        with pytest.raises(ValidationError, match="ativo deve ser booleano"):
            service.atualizarUsuario(usuario.id, {"ativo": "false"})

    def test_excluir_usuario_inexistente(self):
        """Teste 2.24: Excluir usuário inexistente"""
        service = UserService()
        
        resultado = service.excluirUsuario("id-que-nao-existe")
        
        assert resultado == False
    
    # GRUPO 3: CASOS DE BORDA
    
    def test_criar_usuario_nome_2_caracteres(self):
        """Teste 3.1: Criar usuário com nome de exatamente 2 caracteres"""
        service = UserService()
        
        payload = {
            "nome": "Ab",
            "email": "teste@example.com",
            "idade": 25
        }
        
        usuario = service.criarUsuario(payload)
        assert usuario is not None
        assert usuario.nome == "Ab"

    def test_criar_usuario_nome_100_caracteres(self):
        """Teste 3.2: Criar usuário com nome de exatamente 100 caracteres"""
        service = UserService()
        
        payload = {
            "nome": "A" * 100,
            "email": "teste@example.com",
            "idade": 25
        }
        
        usuario = service.criarUsuario(payload)
        assert usuario is not None
        assert len(usuario.nome) == 100

    def test_criar_usuario_nome_com_espacos_extremidades(self):
        """Teste 3.3: Criar usuário com nome contendo espaços nas extremidades"""
        service = UserService()
        
        payload = {
            "nome": "  João Silva  ",
            "email": "teste@example.com",
            "idade": 25
        }
        
        usuario = service.criarUsuario(payload)
        assert usuario is not None
        # A validação deve usar strip(), então espaços devem ser removidos
        assert usuario.nome == "João Silva"

    def test_criar_usuario_idade_exatamente_18(self):
        """Teste 3.4: Criar usuário com idade exatamente 18"""
        service = UserService()
        
        payload = {
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 18
        }
        
        usuario = service.criarUsuario(payload)
        assert usuario is not None
        assert usuario.idade == 18

    def test_criar_usuario_idade_muito_alta(self):
        """Teste 3.5: Criar usuário com idade muito alta (ex: 150)"""
        service = UserService()
        
        payload = {
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 150
        }
        
        usuario = service.criarUsuario(payload)
        assert usuario is not None
        assert usuario.idade == 150

    def test_criar_usuario_email_minimo_valido(self):
        """Teste 3.6: Criar usuário com email mínimo válido"""
        service = UserService()
        
        payload = {
            "nome": "João Silva",
            "email": "a@b.c",
            "idade": 25
        }
        
        usuario = service.criarUsuario(payload)
        assert usuario is not None
        assert usuario.email == "a@b.c"

    def test_criar_usuario_email_caracteres_especiais(self):
        """Teste 3.7: Criar usuário com email contendo caracteres especiais válidos"""
        service = UserService()
        
        payload = {
            "nome": "João Silva",
            "email": "user+tag@example.com",
            "idade": 25
        }
        
        usuario = service.criarUsuario(payload)
        assert usuario is not None
        assert usuario.email == "user+tag@example.com"

    def test_criar_usuario_campos_extras_ignorados(self):
        """Teste 3.8: Criar usuário com payload contendo campos extras"""
        service = UserService()
        
        payload = {
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25,
            "campo_extra": "valor",
            "outro_campo": 123
        }
        
        usuario = service.criarUsuario(payload)
        assert usuario is not None
        
        # Verificar que campos extras não estão no objeto User
        assert not hasattr(usuario, 'campo_extra')
        assert not hasattr(usuario, 'outro_campo')

    def test_atualizar_usuario_payload_vazio(self):
        """Teste 3.9: Atualizar usuário com payload vazio"""
        service = UserService()
        
        usuario = service.criarUsuario({
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25
        })
        
        # Atualizar com payload vazio
        service.atualizarUsuario(usuario.id, {})
        
        # Verificar que nada mudou
        usuario_apos_update = service.buscarUsuario(usuario.id)
        assert usuario_apos_update.nome == "João Silva"
        assert usuario_apos_update.email == "joao@example.com"
        assert usuario_apos_update.idade == 25

    def test_atualizar_usuario_tentativa_modificar_id(self):
        """Teste 3.10: Atualizar usuário tentando modificar ID"""
        service = UserService()
        
        usuario = service.criarUsuario({
            "id": "id-original",
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25
        })
        
        # Tentar atualizar incluindo novo ID
        service.atualizarUsuario(usuario.id, {
            "id": "novo-id",
            "nome": "Novo Nome"
        })
        
        # Verificar que ID não mudou
        usuario_atualizado = service.buscarUsuario("id-original")
        assert usuario_atualizado is not None
        assert usuario_atualizado.id == "id-original"
        assert usuario_atualizado.nome == "Novo Nome"  # nome foi atualizado

    def test_excluir_usuario_duas_vezes(self):
        """Teste 3.11: Excluir usuário e tentar excluir novamente"""
        service = UserService()
        
        usuario = service.criarUsuario({
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25
        })
        
        # Primeira exclusão
        resultado1 = service.excluirUsuario(usuario.id)
        assert resultado1 == True
        
        # Segunda exclusão
        resultado2 = service.excluirUsuario(usuario.id)
        assert resultado2 == False

    def test_criar_usuario_id_string_vazia(self):
        """Teste 3.12: Criar usuário com ID vazio string"""
        service = UserService()
        
        payload = {
            "id": "",
            "nome": "João Silva",
            "email": "joao@example.com",
            "idade": 25
        }
        
        usuario = service.criarUsuario(payload)
        # ID deve ser gerado automaticamente (string vazia é falsy)
        assert usuario.id is not None
        assert usuario.id != ""

    def test_buscar_usuario_id_none(self):
        """Teste 3.13: Buscar usuário com ID None"""
        service = UserService()
        
        usuario = service.buscarUsuario(None)
        
        assert usuario is None

    def test_ids_gerados_sao_unicos(self):
        """Teste 3.14: Criar múltiplos usuários e verificar unicidade de IDs"""
        service = UserService()
        
        usuarios = []
        for i in range(10):
            usuario = service.criarUsuario({
                "nome": f"Usuário {i}",
                "email": f"user{i}@example.com",
                "idade": 20 + i
            })
            usuarios.append(usuario)
        
        # Verificar unicidade
        ids = [usuario.id for usuario in usuarios]
        assert len(ids) == len(set(ids))
        
        # Verificar que são UUIDs válidos (se aplicável)
        for id_val in ids:
            assert len(id_val) > 0

    def test_atualizar_usuario_campos_extras_ignorados(self):
        """Teste 3.15: Atualizar usuário com campos extras no payload"""
        service = UserService()
        
        usuario = service.criarUsuario({
            "nome": "Nome Antigo",
            "email": "antigo@example.com",
            "idade": 25
        })
        
        update_payload = {
            "nome": "Novo Nome",
            "campo_invalido": "valor"
        }
        
        service.atualizarUsuario(usuario.id, update_payload)
        
        usuario_atualizado = service.buscarUsuario(usuario.id)
        assert usuario_atualizado.nome == "Novo Nome"
        # Campo extra não deve existir
        assert not hasattr(usuario_atualizado, 'campo_invalido')
    
    # GRUPO 4: TESTES POR MÉTODO - criarUsuario
    
    def test_criar_usuario_parametros_validos(self):
        """Teste 4.1.1: Criar usuário com todos os parâmetros válidos"""
        service = UserService()
        
        payload = {
            "nome": "Pedro Alves",
            "email": "pedro@example.com",
            "idade": 30,
            "ativo": True
        }
        
        usuario = service.criarUsuario(payload)
        
        assert isinstance(usuario, User)
        assert usuario.nome == "Pedro Alves"
        assert usuario.email == "pedro@example.com"
        assert usuario.idade == 30
        assert usuario.ativo == True
        
        # Verificar armazenamento
        usuario_store = service.buscarUsuario(usuario.id)
        assert usuario_store is not None

    def test_criar_usuario_campos_opcionais_omitidos(self):
        """Teste 4.1.2: Criar usuário com campos opcionais omitidos"""
        service = UserService()
        
        payload = {
            "nome": "Maria Silva",
            "email": "maria@example.com",
            "idade": 28
            # ativo omitido - deve usar padrão True
        }
        
        usuario = service.criarUsuario(payload)
        
        assert usuario is not None
        assert usuario.ativo == True  # valor padrão