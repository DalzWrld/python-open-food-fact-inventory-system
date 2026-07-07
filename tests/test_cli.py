from unittest.mock import Mock, patch

from cli import cli


def _mock_response(json_data, status_code=200):
    mock_resp = Mock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = json_data
    return mock_resp


@patch("cli.cli.requests.request")
def test_cmd_list_prints_items(mock_request, capsys):
    mock_request.return_value = _mock_response(
        [{"id": 1, "name": "Almond Milk", "price": 3.99, "quantity": 10}]
    )

    cli.cmd_list(None)

    captured = capsys.readouterr()
    assert "Almond Milk" in captured.out


@patch("cli.cli.requests.request")
def test_cmd_list_prints_empty_message(mock_request, capsys):
    mock_request.return_value = _mock_response([])

    cli.cmd_list(None)

    captured = capsys.readouterr()
    assert "empty" in captured.out.lower()


@patch("cli.cli.requests.request")
def test_cmd_add_success(mock_request, capsys):
    mock_request.return_value = _mock_response(
        {"id": 1, "name": "Almond Milk", "price": 3.99, "quantity": 10}, status_code=201
    )

    args = Mock(brand="Silk", barcode="", price=3.99, quantity=10)
    args.name = "Almond Milk"  # 'name' is a reserved Mock() kwarg, so set it after creation
    cli.cmd_add(args)

    captured = capsys.readouterr()
    assert "Added item" in captured.out


@patch("cli.cli.requests.request")
def test_cmd_delete_success(mock_request, capsys):
    mock_request.return_value = _mock_response({"message": "Item with id 1 deleted"})

    args = Mock(item_id=1)
    cli.cmd_delete(args)

    captured = capsys.readouterr()
    assert "deleted" in captured.out


@patch("cli.cli.requests.request")
def test_cmd_delete_not_found(mock_request, capsys):
    mock_request.return_value = _mock_response({"error": "Item with id 999 not found"}, status_code=404)

    args = Mock(item_id=999)
    cli.cmd_delete(args)

    captured = capsys.readouterr()
    assert "Error" in captured.out


@patch("cli.cli.requests.request")
def test_cmd_find_by_barcode(mock_request, capsys):
    mock_request.return_value = _mock_response(
        {"name": "Organic Almond Milk", "brand": "Silk", "barcode": "0025293001165"}
    )

    args = Mock(barcode="0025293001165")
    args.name = None  # 'name' is a reserved Mock() kwarg, so set it after creation
    cli.cmd_find(args)

    captured = capsys.readouterr()
    assert "Organic Almond Milk" in captured.out


def test_cmd_find_requires_barcode_or_name(capsys):
    args = Mock(barcode=None)
    args.name = None  # 'name' is a reserved Mock() kwarg, so set it after creation
    cli.cmd_find(args)

    captured = capsys.readouterr()
    assert "Provide either" in captured.out
