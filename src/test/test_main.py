from src.main.main import main


def test_main():
    assert main() is None, "La funcion main no deberia tener retorno"
