ORIGEM = 'http://localhost:3000'
def test_preflight_permitido(cliente):
    resposta = cliente.options('/itens/', headers={'Origin': ORIGEM, 'Access-Control-Request-Method': 'GET'})
    assert resposta.status_code == 200
    assert resposta.headers['access-control-allow-origin'] == ORIGEM
def test_preflight_negado(cliente):
    resposta = cliente.options('/itens/', headers={'Origin': 'https://evil.com', 'Access-Control-Request-Method': 'GET'})
    assert resposta.status_code == 400
def test_resposta_origem_permitida(cliente):
    resposta = cliente.get('/itens/', headers={'Origin': ORIGEM})
    assert resposta.status_code == 200
    assert resposta.headers['access-control-allow-origin'] == ORIGEM
def test_resposta_origem_negada_sem_cabecalho(cliente):
    resposta = cliente.get('/itens/', headers={'Origin': 'https://evil.com'})
    assert resposta.status_code == 200
    assert 'access-control-allow-origin' not in resposta.headers
def test_sem_origem_sem_cabecalho(cliente):
    resposta = cliente.get('/itens/')
    assert resposta.status_code == 200
    assert 'access-control-allow-origin' not in resposta.headers
