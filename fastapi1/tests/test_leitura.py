def test_raiz(cliente):
    resposta = cliente.get('/')
    assert resposta.status_code == 200
def test_listar_vazio(cliente):
    resposta = cliente.get('/itens/')
    assert resposta.status_code == 200
    assert resposta.json() == []
def test_criar_e_ler(cliente, cabecalho):
    criado = cliente.post('/itens/', json={'nome': 'Placa Mae', 'preco': 800}, headers=cabecalho)
    assert criado.status_code == 201
    item = criado.json()
    assert item['nome'] == 'Placa Mae'
    assert item['em_oferta'] is False
    identificador = item['id']
    resposta = cliente.get(f'/itens/{identificador}')
    assert resposta.status_code == 200
    assert resposta.json() == item
def test_ler_inexistente(cliente):
    resposta = cliente.get('/itens/999999')
    assert resposta.status_code == 404
    assert resposta.json() == {'detail': 'Item não encontrado'}
def test_paginacao(cliente, cabecalho):
    for nome in ['A', 'B', 'C']:
        cliente.post('/itens/', json={'nome': nome, 'preco': 10}, headers=cabecalho)
    resposta = cliente.get('/itens/')
    assert len(resposta.json()) == 3
    resposta = cliente.get('/itens/', params={'limite': 2})
    assert len(resposta.json()) == 2
    resposta = cliente.get('/itens/', params={'limite': 2, 'deslocamento': 2})
    assert len(resposta.json()) == 1
    resposta = cliente.get('/itens/', params={'deslocamento': 99})
    assert resposta.json() == []
def test_paginacao_invalida(cliente):
    for consulta in [{'limite': 0}, {'limite': 101}, {'limite': 'abc'}, {'deslocamento': -1}]:
        resposta = cliente.get('/itens/', params=consulta)
        assert resposta.status_code == 422
def test_id_invalido(cliente):
    for identificador in ['0', '-1', 'abc']:
        resposta = cliente.get(f'/itens/{identificador}')
        assert resposta.status_code == 422
