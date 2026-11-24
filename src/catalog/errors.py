class CatalogError(Exception):
    pass


class ItemError(CatalogError):
    pass


class InvalidEntityError(CatalogError):
    pass


class DuplicateIDError(CatalogError):
    pass


class EntityNotFound(CatalogError):
    pass


class DamagedFile(CatalogError):
    pass


class NotFoundError(CatalogError):
    pass


class UnsupportedFormatError(CatalogError):
    pass
