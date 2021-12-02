from marshmallow import Schema, fields


class PointSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    address = fields.Str()
    latitude = fields.Str()
    longitude = fields.Str()
    state = fields.Int()
    telephone = fields.Str()
    email = fields.Email()


class PointPaginationSchema(Schema):
    page = fields.Int()
    per_page = fields.Int()
    total = fields.Int()
    items = fields.Nested(PointSchema, many=True, data_key="Points")


points_schema = PointSchema(many=True)
point_schema = PointSchema()
point_pagination_schema = PointPaginationSchema()
