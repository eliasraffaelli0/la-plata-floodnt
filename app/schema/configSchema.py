from marshmallow import Schema, fields


class ConfigSchema(Schema):
    tema_privado = fields.String()


# class EvacuationRoutePaginationSchema(Schema):
#     page = fields.Int()
#     per_page = fields.Int()
#     pages = fields.Int()
#     total = fields.Int()


# evacuation_routes_schema = EvacuationRouteSchema(many=True)
# evacuation_route_schema = EvacuationRouteSchema()
# evacuation_routes_pagination_schema = EvacuationRoutePaginationSchema()
