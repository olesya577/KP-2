import pytest
from src.api_key import APIAdapter
from src.aeroplanes import JSONSaver


@pytest.fixture
def sample_data() -> List[Dict[str, Any]]:
    """Фикстура: 5 самолётов над Канадой"""
    return [
        {"callsign": "CFTAB", "origin_country": "Canada", "velocity": 132.27, "baro_altitude": 1310.64},
        {"callsign": "WJA793", "origin_country": "Canada", "velocity": 111.3, "baro_altitude": 1226.82},
        {"callsign": "CJT566", "origin_country": "Canada", "velocity": 86.43, "baro_altitude": 1165.86},
        {"callsign": "ACA840", "origin_country": "Canada", "velocity": 85.12, "baro_altitude": 1463.04},
        {"callsign": "ANT773", "origin_country": "Canada", "velocity": 67.91, "baro_altitude": 1196.34},
    ]



@pytest.fixture
def adapter() -> APIAdapter:
    """Фикстура: экземпляр APIAdapter"""
    return APIAdapter()


@pytest.fixture
def nominatim_response() -> list:
    """Фикстура: ответ от Nominatim"""
    return [
        {
            "place_id": "123456",
            "display_name": "Canada",
            "boundingbox": ["41.67598", "83.11386", "-141.00187", "-52.61785"],
            "lat": "60.0",
            "lon": "-100.0",
        }
    ]


@pytest.fixture
def opensky_response() -> Dict[str, Any]:
    """Фикстура: ответ от OpenSky"""
    return {
        "time": 1704067200,
        "states": [
            ["c05f5d", "WEN3645 ", "Canada", 1704067200, 1704067200,
             37.6173, 55.7558, 10000.0, False, 250.5, 90.0, 5.0,
             None, 10100.0, "1234", False, 0],
            ["a12345", "ACA123 ", "Canada", 1704067200, 1704067200,
             -73.5673, 45.5017, 9500.0, False, 240.0, 180.0, -3.0,
             None, 9600.0, "5678", False, 0],
        ]
    }


@pytest.fixture
def mock_get_success(nominatim_response, opensky_response):
    """Фикстура: мок requests.get с двумя разными ответами"""
    def _mock_get(url, params=None, headers=None):
        mock_response = Mock()
        if 'nominatim' in url:
            mock_response.json.return_value = nominatim_response
        else:
            mock_response.json.return_value = opensky_response
        return mock_response
    return _mock_get



@pytest.fixture
def api_adapter() -> APIAdapter:
    """Фикстура: адаптер API"""
    return APIAdapter()


@pytest.fixture
def json_saver(tmp_path) -> JSONSaver:
    """Фикстура: JSON-хранилище во временной папке"""
    file_path = tmp_path / "response.json"
    return JSONSaver(str(file_path))


@pytest.fixture
def mock_file_worker(tmp_path) -> JSONSaver:
    """Фикстура: JSON-хранилище во временной папке"""
    file_path = tmp_path / "vacancies.json"
    return JSONSaver(str(file_path))


@pytest.fixture
def hh(mock_file_worker) -> HH:
    """Фикстура: экземпляр класса HH"""
    return HH(mock_file_worker)


@pytest.fixture
def sample_vacancies() -> List[Dict[str, Any]]:
    """Фикстура: список тестовых вакансий"""
    return [
        {
            "id": "1",
            "name": "Python разработчик",
            "alternate_url": "https://hh.ru/vacancy/1",
            "salary": {"from": 100000, "to": 150000, "currency": "RUB"},
            "area": {"name": "Москва"},
            "employer": {"name": "Компания А"},
        },
        {
            "id": "2",
            "name": "Java разработчик",
            "alternate_url": "https://hh.ru/vacancy/2",
            "salary": {"from": 120000, "to": 180000, "currency": "RUB"},
            "area": {"name": "Санкт-Петербург"},
            "employer": {"name": "Компания Б"},
        },
        {
            "id": "3",
            "name": "Python аналитик",
            "alternate_url": "https://hh.ru/vacancy/3",
            "salary": None,
            "area": {"name": "Москва"},
            "employer": {"name": "Компания В"},
        },
        {
            "id": "4",
            "name": "Data Scientist",
            "alternate_url": "https://hh.ru/vacancy/4",
            "salary": {"from": 150000, "to": 200000, "currency": "RUB"},
            "area": {"name": "Москва"},
            "employer": {"name": "Компания Г"},
        },
    ]


@pytest.fixture
def mock_hh_response(sample_vacancies) -> Dict[str, Any]:
    """Фикстура: мок-ответ от API HH"""
    return {
        "items": sample_vacancies,
        "found": len(sample_vacancies),
        "pages": 20,
        "page": 0,
        "per_page": 100,
    }
