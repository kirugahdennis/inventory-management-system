
from unittest.mock import patch, MagicMock
import cli


@patch("cli.requests.get")
def test_view_all_prints_items(mock_get, capsys):
    mock_resp = MagicMock()
    mock_resp.json.return_value = [
        {"id": 1, "name": "Milk", "quantity": 5, "price": 2.5,
         "brand": "Silk", "barcode": "123"}
    ]
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    cli.view_all()
    out = capsys.readouterr().out
    assert "Milk" in out


@patch("cli.requests.get")
def test_view_all_handles_request_error(mock_get, capsys):
    mock_get.side_effect = cli.requests.RequestException("boom")
    cli.view_all()
    out = capsys.readouterr().out
    assert "Error contacting API" in out


@patch("cli.requests.post")
@patch("builtins.input", side_effect=["Bread", "10", "2.99", "", "", ""])
def test_add_item(mock_input, mock_post, capsys):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "id": 2, "name": "Bread", "quantity": 10, "price": 2.99,
        "brand": None, "barcode": None,
    }
    mock_resp.raise_for_status.return_value = None
    mock_post.return_value = mock_resp

    cli.add_item()
    out = capsys.readouterr().out
    assert "Item added" in out
    mock_post.assert_called_once()


@patch("builtins.input", side_effect=[""])
def test_add_item_requires_name(mock_input, capsys):
    cli.add_item()
    out = capsys.readouterr().out
    assert "Name is required" in out


@patch("cli.requests.delete")
@patch("builtins.input", side_effect=["1"])
def test_delete_item(mock_input, mock_delete, capsys):
    mock_resp = MagicMock()
    mock_resp.status_code = 204
    mock_resp.raise_for_status.return_value = None
    mock_delete.return_value = mock_resp

    cli.delete_item()
    out = capsys.readouterr().out
    assert "Item deleted" in out


@patch("cli.requests.delete")
@patch("builtins.input", side_effect=["999"])
def test_delete_item_not_found(mock_input, mock_delete, capsys):
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    mock_delete.return_value = mock_resp

    cli.delete_item()
    out = capsys.readouterr().out
    assert "Item not found" in out