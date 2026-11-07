class ReglaDeNegocioError(Exception):
    """Se violó una regla de negocio (ej. transición inválida, cliente inactivo)."""


class EntidadNoEncontradaError(Exception):
    """No existe la entidad pedida (pedido, cliente o producto)."""