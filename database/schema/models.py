from tortoise import fields
from tortoise.models import Model
from tortoise.validators import MinValueValidator, MaxValueValidator


class Topics(Model):
    id = fields.IntField(pk=True)
    topic_id = fields.IntField()
    topic_name = fields.CharField(max_length=255)

    class Meta:
        table = 'Topics'

    def __str__(self):
        return self.topic_name


class Users(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.IntField()
    admin = fields.BooleanField(default=False)
    reserved = fields.BooleanField(default=False)
    warn = fields.IntField(default=0)
    callsign = fields.CharField(max_length=255, null=True, unique=True)

    class Meta:
        table = 'Users'

    def __str__(self):
        return self.callsign if self.callsign else 'Callsign not set'


class EventDetails(Model):
    id = fields.IntField(pk=True)
    topic = fields.ForeignKeyField("models.Topics", related_name="events")
    event_name = fields.CharField(max_length=255)
    event_link = fields.CharField(max_length=255, null=True)
    organizer_rules = fields.TextField(null=True)
    latitude = fields.FloatField(
        validators=[
            MinValueValidator(-90.0),
            MaxValueValidator(90.0)
        ]
    )
    longitude = fields.FloatField(
        validators=[
            MinValueValidator(-90.0),
            MaxValueValidator(90.0)
        ]
    )
    price = fields.IntField()
    expire_date = fields.DatetimeField()

    class Meta:
        table = 'Events'

    def __str__(self):
        return self.event_name


class EventPollResults(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.Users", related_name="polls", on_delete=fields.CASCADE)
    event = fields.ForeignKeyField(
        "models.EventDetails", related_name="polls", on_delete=fields.CASCADE)
    visitation = fields.BooleanField()
    reason = fields.TextField(null=True)
    car = fields.BooleanField()
    hitchhike = fields.BooleanField(null=True)
    start_location = fields.TextField()

    class Meta:
        table = 'Polls'

    def __str__(self):
        return self.event.event_name if self.event else 'No Event'
