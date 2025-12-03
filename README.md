# RESUMO
Este estudo compara cinco Modelos de Linguagem de Grande Porte (LLMs), Gemini 1.5 Flash, Claude Sonnet 4.5, GPT-4o mini, Copilot Smart (GPT-5) e DeepSeek-V3, em sua capacidade de gerar automaticamente casos de teste para um módulo de gerenciamento de usuários com regras de validação e operações CRUD. Cada modelo recebeu o mesmo prompt, e os testes gerados foram avaliados por métricas quantitativas e qualitativas.
Os resultados mostram grande variabilidade entre os modelos. O Gemini 1.5 obteve o melhor desempenho, gerando testes de sucesso, erro e borda, enquanto Claude Sonnet produziu mais testes e cobertura completa de métodos, mas sem casos negativos ou de borda. Os outros modelos focaram principalmente em caminhos de sucesso.
O estudo conclui que LLMs podem melhorar a geração de testes, mas ainda exigem supervisão humana para garantir correção e completude, indicando limitações atuais e oportunidades para aprimorar a confiabilidade da automação de testes de software.

# PROMPT PADRÃO
Tarefa: A partir do target system abaixo, gere um conjunto completo e
detalhado de casos de teste.

### Regras do Sistema: 
1. nome deve ser string entre 2 e 100 caracteres. 
2. email deve ter formato válido. 
3. idade deve ser inteiro ≥ 18.
4. Ativo deve ser booleano.
5. O ID é gerado automaticamente caso não seja fornecido. 
6. criarUsuario lança erro se o ID já existir. 
7. buscarUsuario retorna usuário ou None. 
8. atualizarUsuario lança erro se o usuário não existir. 
9. excluirUsuario retorna True/False.

### Grupos de Testes: 
1.  Testes de Sucesso 
2. Testes de Erro
3. Casos de Borda 
4. Testes por Método (criarUsuario, buscarUsuario, atualizarUsuario, excluirUsuario)

### Formato obrigatório de cada teste: 
- Nome do teste: 
- Método testado: 
- Entrada: 
- Passos: 
- Resultado esperado:

#### Instruções: 
- Não omita casos. 
- Não invente regras. 
- Seja detalhado e sistemático.
