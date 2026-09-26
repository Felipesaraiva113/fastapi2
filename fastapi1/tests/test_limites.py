def test_limite_leitura(cliente):
    for _ in range(100):
        resposta = cliente.get('/itens/')
        assert resposta.status_code == 200
    assert cliente.get('/itens/').status_code == 429
def test_limite_criacao(cliente, cabecalho):
    for numero in range(10):
        resposta = cliente.post('/itens/', json={'nome': f'Item {numero}', 'preco': 1}, headers=cabecalho)
        assert resposta.status_code == 201
    resposta = cliente.post('/itens/', json={'nome': 'Extra', 'preco': 1}, headers=cabecalho)
    assert resposta.status_code == 429
def test_limite_atualizacao(cliente, cabecalho):
    criado = cliente.post('/itens/', json={'nome': 'Mouse', 'preco': 90}, headers=cabecalho).json()
    identificador = criado['id']
    for _ in range(10):
        resposta = cliente.put(f'/itens/{identificador}', json={'preco': 95}, headers=cabecalho)
        assert resposta.status_code == 200
    resposta = cliente.put(f'/itens/{identificador}', json={'preco': 95}, headers=cabecalho)
    assert resposta.status_code == 429
def test_limite_remocao(cliente, cabecalho):
    identificadores = []
    for numero in range(10):
        criado = cliente.post('/itens/', json={'nome': f'Item {numero}', 'preco': 1}, headers=cabecalho).json()
        identificadores.append(criado['id'])
    for identificador in identificadores:
        resposta = cliente.delete(f'/itens/{identificador}', headers=cabecalho)
        assert resposta.status_code == 204
    resposta = cliente.delete('/itens/999999', headers=cabecalho)
    assert resposta.status_code == 429
def test_limite_documentacao(cliente, cabecalho):
    for _ in range(5):
        assert cliente.get('/docs', headers=cabecalho).status_code == 200
    assert cliente.get('/docs', headers=cabecalho).status_code == 429
    for _ in range(5):
        assert cliente.get('/openapi.json', headers=cabecalho).status_code == 200
    assert cliente.get('/openapi.json', headers=cabecalho).status_code == 429
