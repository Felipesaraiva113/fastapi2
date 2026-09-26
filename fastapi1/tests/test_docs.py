def test_docs_sem_chave(cliente):
    assert cliente.get('/docs').status_code == 401
    assert cliente.get('/openapi.json').status_code == 401
def test_docs_chave_errada(cliente):
    cabecalho_errado = {'X-API-Key': 'errada'}
    assert cliente.get('/docs', headers=cabecalho_errado).status_code == 403
def test_docs_com_chave(cliente, cabecalho):
    resposta = cliente.get('/docs', headers=cabecalho)
    assert resposta.status_code == 200
    assert 'swagger' in resposta.text.lower()
def test_docs_chave_na_url(cliente, chave):
    resposta = cliente.get('/docs', params={'api_key': chave})
    assert resposta.status_code == 200
def test_esquema_com_chave(cliente, cabecalho):
    resposta = cliente.get('/openapi.json', headers=cabecalho)
    assert resposta.status_code == 200
    assert '/itens/' in resposta.json()['paths']
def test_redoc_inexistente(cliente):
    assert cliente.get('/redoc').status_code == 404
