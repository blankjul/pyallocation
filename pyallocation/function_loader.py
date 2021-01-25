import importlib


def get_functions():
    from pyallocation.util import calc_consumed
    from pyallocation.util import calc_cv_2d, calc_cv_1d

    FUNCTIONS = {
        "calc_consumed": {
            "python": calc_consumed, "cython": "pyallocation.cython.util"
        },
        "calc_cv_1d": {
            "python": calc_cv_1d, "cython": "pyallocation.cython.util"
        },
        "calc_cv_2d": {
            "python": calc_cv_2d, "cython": "pyallocation.cython.util"
        }
    }

    return FUNCTIONS


class FunctionLoader:
    # -------------------------------------------------
    # Singleton Pattern
    # -------------------------------------------------
    __instance = None

    @staticmethod
    def get_instance():
        if FunctionLoader.__instance is None:
            FunctionLoader.__instance = FunctionLoader()
        return FunctionLoader.__instance

    # -------------------------------------------------

    def __init__(self) -> None:
        super().__init__()
        self.is_compiled = is_compiled()

    def load(self, func_name=None, _type="auto"):

        FUNCTIONS = get_functions()

        if _type == "auto":
            _type = "cython" if self.is_compiled else "python"

        if func_name not in FUNCTIONS:
            raise Exception("Function %s not found: %s" % (func_name, FUNCTIONS.keys()))

        func = FUNCTIONS[func_name]
        if _type not in func:
            raise Exception("Module not available in %s." % _type)
        func = func[_type]

        # either provide a function or a string to the module (used for cython)
        if not callable(func):
            module = importlib.import_module(func)
            func = getattr(module, func_name)

        return func


def load_function(func_name=None, _type="auto"):
    return FunctionLoader.get_instance().load(func_name, _type=_type)


def is_compiled():
    try:
        from pyallocation.cython.info import info
        if info() == "yes":
            return True
        else:
            return False
    except:
        return False
