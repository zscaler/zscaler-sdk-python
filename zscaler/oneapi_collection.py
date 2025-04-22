class ZscalerCollection:
    "Class to build lists composed of ZscalerObject datatypes"

    @staticmethod
    def form_list(collection: list, data_type: type):
        if not collection:
            # If empty list or None
            return []
        for index in range(len(collection)):
            if not ZscalerCollection.is_formed(collection[index], data_type):
                collection[index] = data_type(collection[index])
        return collection

    @staticmethod
    def is_formed(value, data_type: type):
        return isinstance(value, data_type)
