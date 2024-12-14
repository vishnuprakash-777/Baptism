from django.db import models
from django.utils.timezone import now

class Baptism(models.Model):
    basic_baptism_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=1)  # Default value
    place_of_baptism = models.CharField(max_length=255)
    date_of_baptism = models.DateField()
    time_of_baptism = models.TimeField()
    child_name_first = models.CharField(max_length=255)
    child_name_second = models.CharField(max_length=255)
    dob = models.DateField()
    mother_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=15)
    email = models.EmailField()
    advanced_baptism_id = models.IntegerField(editable=False, null=True)  # Non-editable and nullable
    priest_id = models.IntegerField(default=1)
    created_time = models.DateTimeField(default=now)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def save(self, *args, **kwargs):
        # Automatically increment user_id if not set
        if not self.user_id:
            last_user_id = Baptism.objects.aggregate(models.Max('user_id'))['user_id__max']
            self.user_id = (last_user_id or 0) + 1

        # Only set advanced_baptism_id after creating the record to generate basic_baptism_id
        if not self.pk:  # This block runs only when creating a new record
            super().save(*args, **kwargs)  # First save to generate basic_baptism_id
            self.advanced_baptism_id = self.basic_baptism_id  # Set advanced_baptism_id to basic_baptism_id
        else:
            self.advanced_baptism_id = self.basic_baptism_id  # Update advanced_baptism_id if not a new record

        super().save(*args, **kwargs)  # Final save to commit changes


class ParishDetails(models.Model):
    parish_id = models.AutoField(primary_key=True)
    parent_parish_id = models.IntegerField(default=1)
    name_of_parish = models.CharField(max_length=255)
    place_of_parish = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    contact_no = models.CharField(max_length=15)
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_time = models.DateTimeField(default=now)

    def __str__(self):
        return self.name_of_parish
    
class LoginDetails(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    last_login = models.DateTimeField(default=now)
    contact_no = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    parish_id = models.IntegerField(default=1)

    def __str__(self):
        return self.user_name
    


from django.db import models
from django.utils.timezone import now

class BaptismAdvanced(models.Model):
    advanced_baptism_id = models.AutoField(primary_key=True)
    basic_baptism_id = models.IntegerField()
    q_id = models.IntegerField()
    priest_id = models.IntegerField()
    question = models.TextField()
    QUESTION_CHOICES = [
        ('MULTIPLE', 'MULTIPLE'),
        ('MULTIPLE-SELECT','MULTIPLE-SELECT'),
        ('TEXT-AREA','TEXT-AREA')
    ]
    question_type = models.CharField(max_length=255,choices=QUESTION_CHOICES,default='MULTIPLE')
    compulsary = models.BooleanField()  # True for compulsary, False otherwise
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_time = models.DateTimeField(default=now)
    field_id = models.IntegerField()
    data_varchar = models.CharField(max_length=255)

    def __str__(self):
        return f"Advanced Baptism {self.advanced_baptism_id}"


class FieldTable(models.Model):
    field_id = models.AutoField(primary_key=True)
    order_no = models.IntegerField()
    TYPE_CHOICES = [
        ('READING', 'READING'),
        ('SONG','SONG'),
        ('PRAYER','PRAYER'),
        ('REMARKS','REMARKS'),
        ('AUTHORIZATION','AUTHORIZATION'),
        ('FINANCIAL','FINANCIAL'),
        ('SPECIAL SAINTS','SPECIAL SAINTS'),
    ]
    type = models.CharField(max_length=20,choices=TYPE_CHOICES,default='READING')
    data = models.TextField()
    QUESTION_CHOICES = [
        ('MULTIPLE', 'MULTIPLE'),
        ('MULTIPLE-SELECT','MULTIPLE-SELECT'),
        ('TEXT-AREA','TEXT-AREA'),
    ]
    choice = models.CharField(max_length=20,choices=QUESTION_CHOICES,default='MULTIPLE')
    q_id = models.IntegerField()
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_time = models.DateTimeField(default=now)

    def __str__(self):
        return f"Field {self.field_id}: {self.type} (Order {self.order_no})"
