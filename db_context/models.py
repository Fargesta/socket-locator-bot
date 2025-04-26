from tortoise import fields, models
from db_context.custom_validators import EmptyValueValidator

class TG_user(models.Model):
    id = fields.BigIntField(primary_key=True, generated=False)
    first_name = fields.CharField(max_length=255, null=False, validators=[EmptyValueValidator()])
    last_name = fields.CharField(max_length=255, null=True, validators=[EmptyValueValidator()])
    username = fields.CharField(max_length=255, null=True, validators=[EmptyValueValidator()])
    language_code = fields.CharField(max_length=10, null=True, validators=[EmptyValueValidator()])
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    is_active = fields.BooleanField(default=False)
    user_role = fields.ForeignKeyField("models.TG_role", related_name="users", null=False, on_delete=fields.CASCADE)

    locations_created = fields.ReverseRelation["TG_location"]
    locations_updated = fields.ReverseRelation["TG_location"]
    images_created = fields.ReverseRelation["TG_image"]

    def __str__(self):
        return self.id

class TG_location(models.Model):
    id = fields.IntField(primary_key=True, generated=True)
    latitude = fields.FloatField(null=False)
    longitude = fields.FloatField(null=False)
    name = fields.CharField(max_length = 255, null=True, validators=[EmptyValueValidator()])
    socket_type = fields.CharField(max_length=4, null=False, validators=[EmptyValueValidator()])
    description = fields.CharField(max_length = 2000, null=True, validators=[EmptyValueValidator()])
    layer = fields.CharField(max_length=500, null=True, validators=[EmptyValueValidator()])
    is_active = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_by = fields.ForeignKeyField("models.TG_user", related_name="locations_created", null=False, on_delete=fields.CASCADE)
    updated_by = fields.ForeignKeyField("models.TG_user", related_name="locations_updated", null=False, on_delete=fields.CASCADE)

    images = fields.ReverseRelation["TG_image"]
    user = fields.ReverseRelation["TG_user"]

    def __str__(self):
        return f"{self.latitude}, {self.longitude}"

class TG_image(models.Model):
    id = fields.IntField(primary_key=True, generated=True)
    url = fields.CharField(max_length=10000, null=False, validators=[EmptyValueValidator()])
    file_name = fields.CharField(max_length=1000, null=True, validators=[EmptyValueValidator()])
    file_id = fields.CharField(max_length=1000, null=False, validators=[EmptyValueValidator()])
    file_size = fields.IntField(null=False, default=0)
    location = fields.ForeignKeyField("models.TG_location", related_name="images", null=False, on_delete=fields.CASCADE)
    description = fields.CharField(max_length=1000, null=True, validators=[EmptyValueValidator()])
    is_active = fields.BooleanField(default=True)
    file_saved = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.ForeignKeyField("models.TG_user", related_name="images_created", null=False, on_delete=fields.CASCADE)

    def __str__(self):
        return self.id

class TG_role(models.Model):
    id = fields.IntField(primary_key=True, generated=True)
    name = fields.CharField(max_length=255, null=False, validators=[EmptyValueValidator()])
    code = fields.CharField(max_length=5, null=False, unique=True, validators=[EmptyValueValidator()])
    description = fields.CharField(max_length=1000, null=True, validators=[EmptyValueValidator()])
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    users = fields.ReverseRelation["TG_user"]

    def __str__(self):
        return self.name