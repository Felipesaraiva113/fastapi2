def test_criar_sem_nome(cliente, cabecalho):
    resposta = cliente.post('/itens/', json={'preco': 10}, headers=cabecalho)
    assert resposta.status_code == 422
def test_criar_sem_preco(cliente, cabecalho):
    resposta = cliente.post('/itens/', json={'nome': 'Y'}, headers=cabecalho)
    assert resposta.status_code == 422
def test_criar_preco_invalido(cliente, cabecalho):
    for preco in [0, -5, 'abc']:
        resposta = cliente.post('/itens/', json={'nome': 'Y', 'preco': preco}, headers=cabecalho)
        assert resposta.status_code == 422
def test_criar_nome_invalido(cliente, cabecalho):
    resposta = cliente.post('/itens/', json={'nome': 'a' * 101, 'preco': 1}, headers=cabecalho)
    assert resposta.status_code == 422
    resposta = cliente.post('/itens/', json={'nome': '   ', 'preco': 1}, headers=cabecalho)
    assert resposta.status_code == 422
def test_criar_campo_extra(cliente, cabecalho):
    resposta = cliente.post('/itens/', json={'nome': 'Y', 'preco': 1, 'hackeavel': True}, headers=cabecalho)
    assert resposta.status_code == 422
    resposta = cliente.post('/itens/', json={'id': 99, 'nome': 'Y', 'preco': 1}, headers=cabecalho)
    assert resposta.status_code == 422
def test_atualizar_nulo(cliente, cabecalho):
    criado = cliente.post('/itens/', json={'nome': 'Cooler', 'preco': 120}, headers=cabecalho).json()
    identificador = criado['id']
    resposta = cliente.put(f'/itens/{identificador}', json={'preco': None}, headers=cabecalho)
    assert resposta.status_code == 422
    resposta = cliente.put(f'/itens/{identificador}', json={'nome': None}, headers=cabecalho)
    assert resposta.status_code == 422
def test_atualizar_invalido(cliente, cabecalho):
    criado = cliente.post('/itens/', json={'nome': 'Cooler', 'preco': 120}, headers=cabecalho).json()
    identificador = criado['id']
    resposta = cliente.put(f'/itens/{identificador}', json={'preco': -1}, headers=cabecalho)
    assert resposta.status_code == 422
