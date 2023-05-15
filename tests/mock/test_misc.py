import requests
import requests_mock

def test_consulta_municipio(uf):
    # Create a mock session
    with requests_mock.Mocker() as mocker:
        # Mock the response for the specific endpoint
        mocker.get(
            f'https://homolog.sisno.com.br/nfe-service/unidades-federativas/{uf}/municipios',
            json=[{'codigo_ibge': 5300108, 'descricao': 'Brasilia'}]
        )

        # Make a request to the mocked endpoint
        response = requests.get(f'https://homolog.sisno.com.br/nfe-service/unidades-federativas/{uf}/municipios')

        # Verify the response
        data = response.json()
        assert data == [{'codigo_ibge': 5300108, 'descricao': 'Brasilia'}]