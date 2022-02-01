from marshmallow import Schema, fields


class ReportSchema(Schema):
    title = fields.String()
    latitude = fields.String()
    longitude = fields.String()
    category = fields.String()
    complainant_name = fields.String()
    complainant_last_name = fields.String()
    complainant_email = fields.String()
    complainant_telephone = fields.String()
    description = fields.String()


class ReportPaginationSchema(Schema):
    page = fields.Int()
    per_page = fields.Int()
    pages = fields.Int()
    total = fields.Int()
    items = fields.Nested(ReportSchema, many=True, data_key="Reports")


reportss_schema = ReportSchema(many=True)
report_schema = ReportSchema()
report_pagination_schema = ReportPaginationSchema()
