from http import HTTPStatus

import pytest

from src.utils import required_role, eleva_quadrado


@pytest.mark.parametrize(
    "role_user, role_required, expected",
    [
        ("admin", "admin", "success"),
        ("user", "admin", ({"message": "User not allowed"}, HTTPStatus.FORBIDDEN)),
    ],
)
def test_required_role(mocker, role_user, role_required, expected):
    # Given
    mock_user = mocker.Mock()
    mock_user.role.name = role_user

    mocker.patch("src.utils.get_jwt_identity", return_value=1)
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)
    decorated_function = required_role(role_required)(lambda: expected)

    # When
    result = decorated_function()

    # Then
    assert result == expected


@pytest.mark.parametrize("test_input,expected", [(2, 4), (3, 9), (10, 100)])
def test_eleva_quadrado_sucesso(test_input, expected):
    resultado = eleva_quadrado(test_input)
    assert resultado == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("a", "unsupported operand type(s) for ** or pow(): 'str' and 'int'"),
        (None, "unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'"),
    ],
)
def test_eleva_quadrado_falha(test_input, expected):
    with pytest.raises(TypeError) as exec:
        eleva_quadrado(test_input)
    assert str(exec.value) == expected
