import unittest
import uuid
from test import User, UserService, ValidationError


class TestUserService(unittest.TestCase):
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.service = UserService()
    
    def test_1_1_criar_usuario_dados_validos(self):
        """Teste 1.1 - Criar usuário com dados válidos"""
        # Entrada
        dados = {"nome": "João Silva", "email": "joao@email.com", "idade": 25}
        
        # Passos
        usuario = self.service.criarUsuario(dados)
        
        # Resultado esperado
        self.assertEqual(usuario.nome, "João Silva")
        self.assertEqual(usuario.email, "joao@email.com")
        self.assertEqual(usuario.idade, 25)
        self.assertTrue(usuario.ativo)
        self.assertIsNotNone(usuario.id)
    
    def test_1_2_criar_usuario_com_id_fornecido(self):
        """Teste 1.2 - Criar usuário com ID fornecido"""
        # Entrada
        dados = {"id": "123", "nome": "Maria Santos", "email": "maria@email.com", "idade": 30}
        
        # Passos
        usuario = self.service.criarUsuario(dados)
        
        # Resultado esperado
        self.assertEqual(usuario.id, "123")
        self.assertEqual(usuario.nome, "Maria Santos")
        self.assertEqual(usuario.email, "maria@email.com")
        self.assertEqual(usuario.idade, 30)
    
    def test_1_3_buscar_usuario_existente(self):
        """Teste 1.3 - Buscar usuário existente"""
        # Passos
        dados = {"nome": "João", "email": "joao@email.com", "idade": 25}
        usuario_criado = self.service.criarUsuario(dados)
        usuario_buscado = self.service.buscarUsuario(usuario_criado.id)
        
        # Resultado esperado
        self.assertEqual(usuario_buscado, usuario_criado)
    
    def test_1_4_atualizar_usuario_dados_validos(self):
        """Teste 1.4 - Atualizar usuário com dados válidos"""
        # Passos
        dados_originais = {"nome": "João", "email": "joao@email.com", "idade": 25}
        usuario = self.service.criarUsuario(dados_originais)
        
        dados_atualizacao = {"nome": "Novo Nome", "email": "novo@email.com", "idade": 35}
        usuario_atualizado = self.service.atualizarUsuario(usuario.id, dados_atualizacao)
        
        # Resultado esperado
        self.assertEqual(usuario_atualizado.id, usuario.id)
        self.assertEqual(usuario_atualizado.nome, "Novo Nome")
        self.assertEqual(usuario_atualizado.email, "novo@email.com")
        self.assertEqual(usuario_atualizado.idade, 35)
    
    def test_1_5_excluir_usuario_existente(self):
        """Teste 1.5 - Excluir usuário existente"""
        # Passos
        dados = {"nome": "João", "email": "joao@email.com", "idade": 25}
        usuario = self.service.criarUsuario(dados)
        resultado = self.service.excluirUsuario(usuario.id)
        
        # Resultado esperado
        self.assertTrue(resultado)
        self.assertIsNone(self.service.buscarUsuario(usuario.id))
    
    def test_2_1_criar_usuario_nome_invalido_curto(self):
        """Teste 2.1 - Criar usuário com nome inválido (curto)"""
        # Entrada
        dados = {"nome": "A", "email": "teste@email.com", "idade": 20}
        
        # Passos e Resultado esperado
        with self.assertRaises(ValidationError) as context:
            self.service.criarUsuario(dados)
        self.assertEqual(str(context.exception), "nome deve ter entre 2 e 100 caracteres")
    
    def test_2_2_criar_usuario_nome_invalido_longo(self):
        """Teste 2.2 - Criar usuário com nome inválido (longo)"""
        # Entrada
        dados = {"nome": "A" * 101, "email": "teste@email.com", "idade": 20}
        
        # Passos e Resultado esperado
        with self.assertRaises(ValidationError) as context:
            self.service.criarUsuario(dados)
        self.assertEqual(str(context.exception), "nome deve ter entre 2 e 100 caracteres")
    
    def test_2_3_criar_usuario_email_invalido(self):
        """Teste 2.3 - Criar usuário com email inválido"""
        # Entrada
        dados = {"nome": "João", "email": "email-invalido", "idade": 20}
        
        # Passos e Resultado esperado
        with self.assertRaises(ValidationError) as context:
            self.service.criarUsuario(dados)
        self.assertEqual(str(context.exception), "email em formato inválido")
    
    def test_2_4_criar_usuario_idade_menor_18(self):
        """Teste 2.4 - Criar usuário com idade menor que 18"""
        # Entrada
        dados = {"nome": "João", "email": "joao@email.com", "idade": 17}
        
        # Passos e Resultado esperado
        with self.assertRaises(ValidationError) as context:
            self.service.criarUsuario(dados)
        self.assertEqual(str(context.exception), "idade mínima é 18 anos")
    
    def test_2_5_criar_usuario_id_duplicado(self):
        """Teste 2.5 - Criar usuário com ID duplicado"""
        # Passos
        dados1 = {"id": "123", "nome": "João", "email": "joao@email.com", "idade": 25}
        self.service.criarUsuario(dados1)
        
        dados2 = {"id": "123", "nome": "Maria", "email": "maria@email.com", "idade": 30}
        
        # Resultado esperado
        with self.assertRaises(ValidationError) as context:
            self.service.criarUsuario(dados2)
        self.assertEqual(str(context.exception), "id já existe")
    
    def test_2_6_atualizar_usuario_inexistente(self):
        """Teste 2.6 - Atualizar usuário inexistente"""
        # Entrada
        dados = {"nome": "Novo Nome"}
        
        # Passos e Resultado esperado
        with self.assertRaises(KeyError) as context:
            self.service.atualizarUsuario("id_inexistente", dados)
        self.assertEqual(str(context.exception), "'usuario não encontrado'")
    
    def test_3_1_nome_comprimento_minimo(self):
        """Teste 3.1 - Nome com comprimento mínimo (2 caracteres)"""
        # Entrada
        dados = {"nome": "Ab", "email": "teste@email.com", "idade": 18}
        
        # Passos
        usuario = self.service.criarUsuario(dados)
        
        # Resultado esperado
        self.assertEqual(usuario.nome, "Ab")
        self.assertEqual(usuario.idade, 18)
    
    def test_3_2_nome_comprimento_maximo(self):
        """Teste 3.2 - Nome com comprimento máximo (100 caracteres)"""
        # Entrada
        dados = {"nome": "A" * 100, "email": "teste@email.com", "idade": 18}
        
        # Passos
        usuario = self.service.criarUsuario(dados)
        
        # Resultado esperado
        self.assertEqual(len(usuario.nome), 100)
        self.assertEqual(usuario.idade, 18)
    
    def test_3_3_idade_minima(self):
        """Teste 3.3 - Idade mínima (18 anos)"""
        # Entrada
        dados = {"nome": "João", "email": "joao@email.com", "idade": 18}
        
        # Passos
        usuario = self.service.criarUsuario(dados)
        
        # Resultado esperado
        self.assertEqual(usuario.idade, 18)
    
    def test_3_4_buscar_usuario_inexistente(self):
        """Teste 3.4 - Buscar usuário inexistente"""
        # Passos
        resultado = self.service.buscarUsuario("id_inexistente")
        
        # Resultado esperado
        self.assertIsNone(resultado)
    
    def test_3_5_excluir_usuario_inexistente(self):
        """Teste 3.5 - Excluir usuário inexistente"""
        # Passos
        resultado = self.service.excluirUsuario("id_inexistente")
        
        # Resultado esperado
        self.assertFalse(resultado)
    
    def test_3_6_atualizacao_parcial_usuario(self):
        """Teste 3.6 - Atualização parcial de usuário"""
        # Passos
        dados_originais = {"nome": "João", "email": "joao@email.com", "idade": 25, "ativo": False}
        usuario = self.service.criarUsuario(dados_originais)
        
        dados_atualizacao = {"nome": "Novo Nome"}
        usuario_atualizado = self.service.atualizarUsuario(usuario.id, dados_atualizacao)
        
        # Resultado esperado
        self.assertEqual(usuario_atualizado.nome, "Novo Nome")
        self.assertEqual(usuario_atualizado.email, "joao@email.com")  # Mantém original
        self.assertEqual(usuario_atualizado.idade, 25)  # Mantém original
        self.assertFalse(usuario_atualizado.ativo)  # Mantém original
    
    def test_4_1_criar_usuario_campo_ativo_padrao(self):
        """Teste 4.1 - criarUsuario: Campo ativo padrão"""
        # Entrada
        dados = {"nome": "João", "email": "joao@email.com", "idade": 25}
        
        # Passos
        usuario = self.service.criarUsuario(dados)
        
        # Resultado esperado
        self.assertTrue(usuario.ativo)
    
    def test_4_2_criar_usuario_filtro_campos_nao_permitidos(self):
        """Teste 4.2 - criarUsuario: Filtro de campos não permitidos"""
        # Entrada
        dados = {"nome": "João", "email": "joao@email.com", "idade": 25, "campo_extra": "valor"}
        
        # Passos
        usuario = self.service.criarUsuario(dados)
        
        # Resultado esperado
        self.assertFalse(hasattr(usuario, 'campo_extra'))
    
    def test_4_3_buscar_usuario_desativado(self):
        """Teste 4.3 - buscarUsuario: Usuário desativado"""
        # Passos
        dados = {"nome": "João", "email": "joao@email.com", "idade": 25, "ativo": False}
        usuario = self.service.criarUsuario(dados)
        usuario_buscado = self.service.buscarUsuario(usuario.id)
        
        # Resultado esperado
        self.assertEqual(usuario_buscado, usuario)
        self.assertFalse(usuario_buscado.ativo)
    
    def test_4_4_atualizar_usuario_mantencao_id(self):
        """Teste 4.4 - atualizarUsuario: Manutenção do ID"""
        # Passos
        dados_originais = {"id": "original", "nome": "João", "email": "joao@email.com", "idade": 25}
        usuario = self.service.criarUsuario(dados_originais)
        
        dados_atualizacao = {"id": "novo_id", "nome": "Novo Nome"}
        usuario_atualizado = self.service.atualizarUsuario(usuario.id, dados_atualizacao)
        
        # Resultado esperado
        self.assertEqual(usuario_atualizado.id, "original")  # Mantém ID original
        self.assertEqual(usuario_atualizado.nome, "Novo Nome")
    
    def test_4_5_excluir_usuario_verificacao_remocao(self):
        """Teste 4.5 - excluirUsuario: Verificação de remoção"""
        # Passos
        dados = {"nome": "João", "email": "joao@email.com", "idade": 25}
        usuario = self.service.criarUsuario(dados)
        
        # Excluir e verificar
        resultado_exclusao = self.service.excluirUsuario(usuario.id)
        resultado_busca = self.service.buscarUsuario(usuario.id)
        
        # Resultado esperado
        self.assertTrue(resultado_exclusao)
        self.assertIsNone(resultado_busca)
    
    def test_4_6_validacao_tipo_nome_nao_string(self):
        """Teste 4.6 - Validação de tipo: nome não string"""
        # Entrada
        dados = {"nome": 123, "email": "teste@email.com", "idade": 20}
        
        # Passos e Resultado esperado
        with self.assertRaises(ValidationError) as context:
            self.service.criarUsuario(dados)
        self.assertEqual(str(context.exception), "nome deve ser string")
    
    def test_4_7_validacao_tipo_idade_nao_inteiro(self):
        """Teste 4.7 - Validação de tipo: idade não inteiro"""
        # Entrada
        dados = {"nome": "João", "email": "teste@email.com", "idade": "vinte"}
        
        # Passos e Resultado esperado
        with self.assertRaises(ValidationError) as context:
            self.service.criarUsuario(dados)
        self.assertEqual(str(context.exception), "idade deve ser inteiro")
    
    def test_4_8_validacao_tipo_ativo_nao_booleano(self):
        """Teste 4.8 - Validação de tipo: ativo não booleano"""
        # Entrada
        dados = {"nome": "João", "email": "teste@email.com", "idade": 20, "ativo": "sim"}
        
        # Passos e Resultado esperado
        with self.assertRaises(ValidationError) as context:
            self.service.criarUsuario(dados)
        self.assertEqual(str(context.exception), "ativo deve ser booleano")
    
    def test_4_9_formato_email_valido_com_subdominio(self):
        """Teste 4.9 - Formato de email válido com subdomínio"""
        # Entrada
        dados = {"nome": "João", "email": "joao@empresa.co.uk", "idade": 25}
        
        # Passos
        usuario = self.service.criarUsuario(dados)
        
        # Resultado esperado
        self.assertEqual(usuario.email, "joao@empresa.co.uk")
    
    def test_4_10_uuid_gerado_automaticamente(self):
        """Teste 4.10 - UUID gerado automaticamente"""
        # Entrada
        dados = {"nome": "João", "email": "joao@email.com", "idade": 25}
        
        # Passos
        usuario = self.service.criarUsuario(dados)
        
        # Resultado esperado
        try:
            uuid.UUID(usuario.id, version=4)
            uuid_valido = True
        except ValueError:
            uuid_valido = False
        
        self.assertTrue(uuid_valido)


if __name__ == '__main__':
    unittest.main(verbosity=2)