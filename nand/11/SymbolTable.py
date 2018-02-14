############################################################
# Globals
############################################################
FIELD_COUNTER = 0
STATIC_COUNTER = 0
ARG_COUNTER = 0
LOCAL_COUNTER = 0


class SymbolTable:
    def __init__(self):
        self.list_of_vars = dict()
        self.subroutine_vars = dict()

    def start_subroutine(self):
        global ARG_COUNTER, LOCAL_COUNTER
        self.subroutine_vars = dict()
        ARG_COUNTER, LOCAL_COUNTER = 0, 0

    def restart_table(self):
        global FIELD_COUNTER, STATIC_COUNTER
        FIELD_COUNTER, STATIC_COUNTER = 0, 0
        self.list_of_vars = dict()

    def define(self, name, var_type, kind):
        number = self.var_count(kind)
        if kind == "static":
            self.list_of_vars[name] = [var_type, kind, number]
        elif kind == "field":
            self.list_of_vars[name] = [var_type, "this", number]
        else:
            self.subroutine_vars[name] = [var_type, kind, number]
        self.var_inc(kind)  # counter of kind (var) + 1

    @staticmethod
    def var_count(kind):
        global FIELD_COUNTER, STATIC_COUNTER, ARG_COUNTER, LOCAL_COUNTER
        if kind == "this" or kind == "field":
            return FIELD_COUNTER
        elif kind == "static":
            return STATIC_COUNTER
        elif kind == "argument":
            return ARG_COUNTER
        return LOCAL_COUNTER

    @staticmethod
    def var_inc(kind):
        global FIELD_COUNTER, STATIC_COUNTER, ARG_COUNTER, LOCAL_COUNTER
        if kind == "field":
            FIELD_COUNTER += 1
        elif kind == "static":
            STATIC_COUNTER += 1
        elif kind == "argument":
            ARG_COUNTER += 1
        else:
            LOCAL_COUNTER += 1

    def kind_of(self, name):
        if name in self.list_of_vars:
            return self.list_of_vars[name][1]
        elif name in self.subroutine_vars:
            return self.subroutine_vars[name][1]
        return None

    def type_of(self, name):
        if name in self.list_of_vars:
            return self.list_of_vars[name][0]
        return self.subroutine_vars[name][0]

    def index_of(self, name):
        if name in self.list_of_vars:
            return self.list_of_vars[name][2]
        return self.subroutine_vars[name][2]
