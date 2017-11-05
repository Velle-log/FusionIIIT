from django import utils
from django.contrib.auth.models import User
from django.db import models

VISITOR_CATEGORY = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    )

ROOM_TYPE = (
    ('SingleBed', 'SingleBed'),
    ('DoubleBed', 'DoubleBed'),
    )

ROOM_FLOOR = (
    ('GroundFloor', 'GroundFloor'),
    ('FirstFloor', 'FirstFloor'),
    ('SecondFloor', 'SecondFloor'),
    ('ThirdFloor', 'ThirdFloor'),
    )

ROOM_STATUS = (
    ('Booked', 'Booked'),
    ('CheckedIn', 'Occupied'),
    ('Available', 'Available'),
    ('UnderMaintenance', 'UnderMaintenance'),
    )

BOOK_ROOM = (
    ('Confirm', 'Confirm'),
    ('Pending', 'Pending'),
    ('Cancelled', 'Cancelled'),
    )


class Visitor(models.Model):
    visitor_name = models.CharField(max_length=40)
    visitor_email = models.CharField(max_length=40)
    visitor_phone = models.CharField(max_length=12)
    visitor_address = models.TextField()
    nationality = models.CharField(max_length=20)
    intender = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.visitor_name


class Book_room(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    room_count = models.IntegerField(default=1)
    visitor_category = models.CharField(max_length=1, choices=VISITOR_CATEGORY)
    person_count = models.IntegerField(default=1)
    purpose = models.TextField()
    booking_from = models.DateField()
    booking_to = models.DateField()
    status = models.CharField(max_length=10, choices=BOOK_ROOM, default="Pending")
    remark = models.CharField(max_length=40, blank=True)
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.visitor.visitor_name)


class Visitor_bill(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    caretaker = models.OneToOneField(User, on_delete=models.CASCADE)
    meal_bill = models.IntegerField(default=0)
    room_bill = models.IntegerField(default=0)
    payment_status = models.BooleanField(default=False)


class Room(models.Model):
    room_number = models.CharField(max_length=4, unique=True)
    room_type = models.CharField(max_length=12, choices=ROOM_TYPE)
    room_floor = models.CharField(max_length=12, choices=ROOM_FLOOR)

    def __str__(self):
        return self.room_number


class Visitor_room(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)


class Meal(models.Model):
    visitor_id = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    meal_date = models.DateField()
    morning_tea = models.BooleanField(default=False)
    eve_tea = models.BooleanField(default=False)
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)
    persons = models.IntegerField(default=0)


class Inventory(models.Model):
    item_name = models.CharField(max_length=20)
    opening_stock = models.IntegerField(default=0)
    addition_stock = models.IntegerField(default=0)
    total_stock = models.IntegerField(default=0)
    serviceable = models.IntegerField(default=0)
    non_serviceable = models.IntegerField(default=0)
    inuse = models.IntegerField(default=0)
    total_usable = models.IntegerField(default=0)
    remark = models.TextField()


class Room_Status(models.Model):
    date = models.DateField(default=utils.timezone.now, null=False)
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    status = models.CharField(max_length=12, choices=ROOM_STATUS, default="Available")
    br_id = models.ForeignKey(Book_room,
                              on_delete=models.CASCADE,
                              unique=False,
                              null=True,
                              blank=True)

    def __str__(self):
        return str(self.room.room_number)
