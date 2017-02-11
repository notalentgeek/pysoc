import warnings as warn

def c_warning(
    _object_name:str,
    _object_type:str,
    _function_where_convention_defined:str,
    _file_where_convention_defined:str
):
    warn.warn(
        "{} {} is not accroding to the naming convention in {} in {}".format(
            _object_type,
            _object_name,
            _function_where_convention_defined,
            _file_where_convention_defined
        ),
        ConventionWarning
    )

def cd_warning(
    _object_name:str,
    _object_type:str,
    _created_or_deleted:bool,
    _function_where_convention_defined:str,
    _file_where_convention_defined:str
):
    _created_or_deleted = "created" if _created_or_deleted else "deleted"

    warn.warn(
        "{} {}".format(
            "{} {} is not {} due to string".format(
                _object_name,
                _object_type,
                _created_or_deleted
            ),
            "check retuning false in `{}` in `{}.py`.".format(
                _function_where_convention_defined,
                _file_where_convention_defined
            )
        ),
        CreationDeletionWarning
    )

class ConventionWarning(Warning):
    pass

class CreationDeletionWarning(Warning):
    pass

class TestWarning(Warning):
    pass
