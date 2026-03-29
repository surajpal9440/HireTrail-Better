from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models.job import JobStatus


class JobCreateSchema(Schema):
    company = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    position = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    location = fields.Str(load_default=None, validate=validate.Length(max=150))
    status = fields.Str(
        load_default=JobStatus.APPLIED,
        validate=validate.OneOf(JobStatus.ALL),
    )
    applied_date = fields.Date(required=True)
    salary_range = fields.Str(load_default=None, validate=validate.Length(max=50))
    job_url = fields.Url(load_default=None)
    notes = fields.Str(load_default=None)

    @validates("company")
    def validate_company(self, value):
        if not value.strip():
            raise ValidationError("Company name cannot be blank.")

    @validates("position")
    def validate_position(self, value):
        if not value.strip():
            raise ValidationError("Position cannot be blank.")


class JobUpdateSchema(Schema):
    company = fields.Str(validate=validate.Length(min=1, max=150))
    position = fields.Str(validate=validate.Length(min=1, max=150))
    location = fields.Str(allow_none=True, validate=validate.Length(max=150))
    status = fields.Str(validate=validate.OneOf(JobStatus.ALL))
    applied_date = fields.Date()
    salary_range = fields.Str(allow_none=True, validate=validate.Length(max=50))
    job_url = fields.Url(allow_none=True)
    notes = fields.Str(allow_none=True)
