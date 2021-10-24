class Accumulator:

    def evaluate_to_dict(self):
        functions = [func for func in dir(self) if callable(getattr(self, func)) and 'get_' in func]
        return {function[4:]: getattr(self, function)() for function in functions}
