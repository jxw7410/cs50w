class isbnNullError(Exception):
    """ISBN is not defined"""
    pass

class EmptyInputError(Exception):
    """Expecting Input"""
    pass

class EmptyQueryError(Exception):
    """Query is empty"""
    pass

class dateNullError(Exception):
    """Empty Date"""
    pass

