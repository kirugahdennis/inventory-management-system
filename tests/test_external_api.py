
from unittest.mock import patch, MagicMock
import external_api


@patch("external_api.requests.get")
def test_fetch_by_barcode_found(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Almond Milk",
            "brands": "Silk",
            "categories": "Beverages",
            "image_url": "http://example.com/img.jpg",
        },
    }
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    result = external_api.fetch_by_barcode("3760020508174")

    assert result["name"] == "Almond Milk"
    assert result["brand"] == "Silk"
    assert result["barcode"] == "3760020508174"
    mock_get.assert_called_once()


@patch("external_api.requests.get")
def test_fetch_by_barcode_not_found(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"status": 0}
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    result = external_api.fetch_by_barcode("0000000000000")
    assert result is None


@patch("external_api.requests.get")
def test_fetch_by_name(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "products": [
            {"product_name": "Oat Milk", "brands": "Oatly", "code": "111"},
            {"product_name": "Soy Milk", "brands": "Silk", "code": "222"},
        ]
    }
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    results = external_api.fetch_by_name("milk")
    assert len(results) == 2
    assert results[0]["name"] == "Oat Milk"