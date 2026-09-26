def test_criar(cliente, cabecalho):
    resposta = cliente.post('/itens/', json={'nome': 'SSD', 'preco': 500, 'em_oferta': True}, headers=cabecalho)
    assert resposta.status_code == 201
    assert resposta.json() == {'id': 1, 'nome': 'SSD', 'preco': 500.0, 'em_oferta': True}
def test_criar_em_oferta_padrao(cliente, cabecalho):
    resposta = cliente.post('/itens/', json={'nome': 'RAM', 'preco': 300}, headers=cabecalho)
    assert resposta.status_code == 201
    assert resposta.json()['em_oferta'] is False
def test_escrita_sem_chave(cliente):
    corpo = {'nome': 'X', 'preco': 1}
    assert cliente.post('/itens/', json=corpo).status_code == 401
    assert cliente.put('/itens/1', json=corpo).status_code == 401
    assert cliente.delete('/itens/1').status_code == 401
def test_escrita_chave_errada(cliente):
    cabecalho_errado = {'X-API-Key': 'errada'}
    corpo = {'nome': 'X', 'preco': 1}
    assert cliente.post('/itens/', json=corpo, headers=cabecalho_errado).status_code == 403
    assert cliente.put('/itens/1', json=corpo, headers=cabecalho_errado).status_code == 403
    assert cliente.delete('/itens/1', headers=cabecalho_errado).status_code == 403
def test_atualizar(cliente, cabecalho):
    criado = cliente.post('/itens/', json={'nome': 'Fonte', 'preco': 400}, headers=cabecalho).json()
    identificador = criado['id']
    resposta = cliente.put(f'/itens/{identificador}', json={'preco': 350}, headers=cabecalho)
    assert resposta.status_code == 200
    assert resposta.json() == {'id': identificador, 'nome': 'Fonte', 'preco': 350.0, 'em_oferta': False}
def test_atualizar_vazio(cliente, cabecalho):
    criado = cliente.post('/itens/', json={'nome': 'Fonte', 'preco': 400}, headers=cabecalho).json()
    identificador = criado['id']
    resposta = cliente.put(f'/itens/{identificador}', json={}, headers=cabecalho)
    assert resposta.status_code == 200
def test_atualizar_inexistente(cliente, cabecalho):
    resposta = cliente.put('/itens/999999', json={'preco': 1}, headers=cabecalho)
    assert resposta.status_code == 404
def test_deletar(cliente, cabecalho):
    criado = cliente.post('/itens/', json={'nome': 'Gabinete', 'preco': 250}, headers=cabecalho).json()
    identificador = criado['id']
    resposta = cliente.delete(f'/itens/{identificador}', headers=cabecalho)
    assert resposta.status_code == 204
    assert cliente.get(f'/itens/{identificador}').status_code == 404
def test_deletar_inexistente(cliente, cabecalho):
    resposta = cliente.delete('/itens/999999', headers=cabecalho)
    assert resposta.status_code == 404
