def test_host_invalido_rejeitado(cliente):
    resposta = cliente.get('/itens/', headers={'host': 'evil.com'})
    assert resposta.status_code == 400
def test_host_localhost_ok(cliente):
    assert cliente.get('/').status_code == 200
def test_host_ip_ok(cliente):
    resposta = cliente.get('/', headers={'host': '127.0.0.1'})
    assert resposta.status_code == 200
def test_host_invalido_escrita(cliente, cabecalho):
    resposta = cliente.post('/itens/', json={'nome': 'X', 'preco': 1}, headers={**cabecalho, 'host': 'evil.com'})
    assert resposta.status_code == 400
