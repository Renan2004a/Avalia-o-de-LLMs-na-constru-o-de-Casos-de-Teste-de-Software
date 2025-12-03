import unittest
from test import UserService, User, ValidationError

class TestUserService(unittest.TestCase):
    
    def setUp(self):
        """Executado antes de cada teste. Garante um ambiente limpo."""
        self.service = UserService()
        self.payload_padrao = {
            "nome": "Usuario Padrao",
            "email": "padrao@teste.com",
            "idade": 30,
            "ativo": True
        }

    # ==========================================================================
    # GRUPO 1: TESTES DE SUCESSO (Happy Path)
    # ==========================================================================

    def test_TC01_criar_usuario_valido_id_automatico(self):
        """Verifica criação básica com geração automática de UUID."""
        user = self.service.criarUsuario(self.payload_padrao)
        
        self.assertIsInstance(user, User)
        self.assertIsInstance(user.id, str)
        self.assertTrue(len(user.id) > 0)
        self.assertTrue(user.ativo)
        
        # Verifica se foi salvo no store
        salvo = self.service.buscarUsuario(user.id)
        self.assertEqual(salvo, user)

    def test_TC02_criar_usuario_com_id_e_status_fornecidos(self):
        """Verifica se o sistema respeita ID e status 'False' passados no payload."""
        payload = self.payload_padrao.copy()
        payload["id"] = "id-personalizado-123"
        payload["ativo"] = False
        
        user = self.service.criarUsuario(payload)
        
        self.assertEqual(user.id, "id-personalizado-123")
        self.assertFalse(user.ativo)

    def test_TC03_buscar_usuario_existente(self):
        """Verifica a recuperação de um usuário criado."""
        user_criado = self.service.criarUsuario(self.payload_padrao)
        user_buscado = self.service.buscarUsuario(user_criado.id)
        
        self.assertIsNotNone(user_buscado)
        self.assertEqual(user_buscado.email, self.payload_padrao["email"])

    def test_TC04_atualizar_usuario_sucesso(self):
        """Verifica atualização parcial de dados."""
        user = self.service.criarUsuario(self.payload_padrao)
        
        # Atualiza apenas o nome
        novo_nome = "Nome Atualizado"
        updated = self.service.atualizarUsuario(user.id, {"nome": novo_nome})
        
        self.assertEqual(updated.nome, novo_nome)
        self.assertEqual(updated.idade, self.payload_padrao["idade"]) # Idade não mudou
        
        # Verifica persistência
        no_banco = self.service.buscarUsuario(user.id)
        self.assertEqual(no_banco.nome, novo_nome)

    def test_TC05_excluir_usuario_existente(self):
        """Verifica exclusão e retorno True."""
        user = self.service.criarUsuario(self.payload_padrao)
        
        resultado = self.service.excluirUsuario(user.id)
        self.assertTrue(resultado)
        
        buscado = self.service.buscarUsuario(user.id)
        self.assertNone(buscado)

    # ==========================================================================
    # GRUPO 2: TESTES DE ERRO (Validações)
    # ==========================================================================

    def test_TC06_erro_nome_muito_curto(self):
        payload = self.payload_padrao.copy()
        payload["nome"] = "A"
        with self.assertRaisesRegex(ValidationError, "nome deve ter entre 2 e 100 caracteres"):
            self.service.criarUsuario(payload)

    def test_TC07_erro_nome_muito_longo(self):
        payload = self.payload_padrao.copy()
        payload["nome"] = "A" * 101
        with self.assertRaisesRegex(ValidationError, "nome deve ter entre 2 e 100 caracteres"):
            self.service.criarUsuario(payload)

    def test_TC08_erro_nome_tipo_invalido(self):
        payload = self.payload_padrao.copy()
        payload["nome"] = 12345
        with self.assertRaisesRegex(ValidationError, "nome deve ser string"):
            self.service.criarUsuario(payload)

    def test_TC09_erro_email_formato_invalido(self):
        payload = self.payload_padrao.copy()
        payload["email"] = "email_sem_arroba.com"
        with self.assertRaisesRegex(ValidationError, "email em formato inválido"):
            self.service.criarUsuario(payload)

    def test_TC10_erro_idade_menor_que_18(self):
        payload = self.payload_padrao.copy()
        payload["idade"] = 17
        with self.assertRaisesRegex(ValidationError, "idade mínima é 18 anos"):
            self.service.criarUsuario(payload)

    def test_TC11_erro_idade_tipo_invalido(self):
        payload = self.payload_padrao.copy()
        payload["idade"] = "20"
        with self.assertRaisesRegex(ValidationError, "idade deve ser inteiro"):
            self.service.criarUsuario(payload)

    def test_TC12_erro_ativo_tipo_invalido(self):
        payload = self.payload_padrao.copy()
        payload["ativo"] = "sim"
        with self.assertRaisesRegex(ValidationError, "ativo deve ser booleano"):
            self.service.criarUsuario(payload)

    def test_TC13_erro_id_duplicado(self):
        payload = self.payload_padrao.copy()
        payload["id"] = "id-fixo"
        
        self.service.criarUsuario(payload) # Primeiro sucesso
        
        with self.assertRaisesRegex(ValidationError, "id já existe"):
            self.service.criarUsuario(payload) # Segundo falha

    def test_TC14_erro_atualizar_usuario_inexistente(self):
        with self.assertRaisesRegex(KeyError, "usuario não encontrado"):
            self.service.atualizarUsuario("fantasma", {"nome": "Novo"})

    # ==========================================================================
    # GRUPO 3: CASOS DE BORDA (Limites)
    # ==========================================================================

    def test_TC15_borda_nome_limites_exatos(self):
        """Testa limites inferior (2) e superior (100) do nome."""
        # Limite inferior
        p_min = self.payload_padrao.copy()
        p_min["nome"] = "Bo"
        self.service.criarUsuario(p_min) # Não deve falhar

        # Limite superior
        p_max = self.payload_padrao.copy()
        p_max["nome"] = "x" * 100
        self.service.criarUsuario(p_max) # Não deve falhar

    def test_TC16_borda_idade_exata_18(self):
        """Testa idade mínima exata."""
        p = self.payload_padrao.copy()
        p["idade"] = 18
        self.service.criarUsuario(p) # Não deve falhar

    def test_TC17_borda_nome_com_espacos(self):
        """
        O código faz len(name.strip()). 
        Entrada '  A  ' tem len 5, mas stripada tem len 1.
        Deve falhar.
        """
        p = self.payload_padrao.copy()
        p["nome"] = "  A  "
        with self.assertRaisesRegex(ValidationError, "nome deve ter entre 2 e 100 caracteres"):
            self.service.criarUsuario(p)

    # ==========================================================================
    # GRUPO 4: TESTES ESPECÍFICOS DE LÓGICA E MÉTODO
    # ==========================================================================

    def test_TC18_normalizacao_payload_campos_extras(self):
        """Campos extras no payload devem ser ignorados silenciosamente."""
        payload = self.payload_padrao.copy()
        payload["campo_malicioso"] = "drop database"
        
        user = self.service.criarUsuario(payload)
        
        # Verifica se o campo não existe no objeto ou no dict
        dicionario = user.to_dict()
        self.assertNotIn("campo_malicioso", dicionario)
        self.assertFalse(hasattr(user, "campo_malicioso"))

    def test_TC19_buscar_usuario_inexistente(self):
        """Deve retornar None, não erro."""
        resultado = self.service.buscarUsuario("nao-existe")
        self.assertIsNone(resultado)

    def test_TC20_excluir_usuario_inexistente(self):
        """Deve retornar False, não erro."""
        resultado = self.service.excluirUsuario("nao-existe")
        self.assertFalse(resultado)

if __name__ == '__main__':
    unittest.main()