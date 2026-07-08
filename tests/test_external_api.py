from unittest.mock import Mock, patch

from services import external_api


def _mock_response(json_data, status_code=200, raise_error=None):
    mock_resp = Mock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = json_data
    if raise_error:
        mock_resp.raise_for_status.side_effect = raise_error
    else:
        mock_resp.raise_for_status.return_value = None
    return mock_resp


@patch("services.external_api.requests.get")
def test_fetch_by_barcode_success(mock_get):
    mock_get.return_value = _mock_response({
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "code": "0025293001165",
            "ingredients_text": "Filtered water, almonds, cane sugar",
        },
    })

    result = external_api.fetch_by_barcode("0025293001165")

    assert result is not None
    assert result["name"] == "Organic Almond Milk"
    assert result["brand"] == "Silk"
    assert result["source"] == "openfoodfacts"


@patch("services.external_api.requests.get")
def test_fetch_by_barcode_not_found(mock_get):
    mock_get.return_value = _mock_response({"status": 0})

    result = external_api.fetch_by_barcode("0000000000000")

    assert result is None


@patch("services.external_api.requests.get")
def test_fetch_by_barcode_request_error(mock_get):
    import requests
    mock_get.side_effect = requests.RequestException("network down")

    result = external_api.fetch_by_barcode("0025293001165")

    assert result is None


@patch("services.external_api.requests.get")
def test_fetch_by_name_success(mock_get):
    mock_get.return_value = _mock_response({
        "products": [
            {
                "product_name": "Oat Milk",
                "brands": "Oatly",
                "code": "1234567890123",
                "ingredients_text": "Oats, water",
            }
        ]
    })

    result = external_api.fetch_by_name("oat milk")

    assert result is not None
    assert result["name"] == "Oat Milk"
    assert result["brand"] == "Oatly"


@patch("services.external_api.requests.get")
def test_fetch_by_name_no_results(mock_get):
    mock_get.return_value = _mock_response({"products": []})

    result = external_api.fetch_by_name("nonexistent product xyz")

    assert result is None
