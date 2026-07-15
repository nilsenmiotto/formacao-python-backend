import pytest
from src.utils import eleva_quadrado


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
