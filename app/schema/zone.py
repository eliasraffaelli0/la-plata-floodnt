class ZoneSchema(object):
    @classmethod
    def dump(cls, obj):
        return cls._serialize(obj)

    @classmethod
    def _serialize(cls, obj):
        # realizar logica para mostrar los datos que quiero que se serialicen
        return {attr.name: getattr(obj, attr.name) for attr in obj.__table__.columns}
