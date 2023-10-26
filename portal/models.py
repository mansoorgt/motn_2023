from django.db import models

# Create your models here.


class EventCardType(models.Model):
    name=models.CharField(max_length=100)
    active=models.BooleanField(default=True)
    class Meta:
        db_table='event_cardtype'

class BuildCardType(models.Model):
    name=models.CharField(max_length=100)
    eventcardtype=models.ForeignKey(EventCardType, on_delete=models.CASCADE)
    active=models.BooleanField(default=True)
    class Meta:
        db_table='build_cardtype'

class VappCardType(models.Model):
    name=models.CharField(max_length=100)
    active=models.BooleanField(default=True)
    class Meta:
        db_table='vapp_cardtype'

class VehicleType(models.Model):
    name=models.CharField(max_length=100)
    active=models.BooleanField(default=True)
    class Meta:
        db_table='vehicle_type'        
   
class BuildRegistrations(models.Model):
    first_name=models.TextField()
    last_name=models.TextField()
    mobile=models.TextField(null=True)
    email=models.TextField(null=True)
    company=models.TextField(null=True)
    
    dob=models.DateField(null=True)
    cardtype=models.ForeignKey(BuildCardType, on_delete=models.CASCADE)
    
    remark=models.TextField(default='',null=True)
    collected=models.BooleanField(default=False)
    print_count=models.IntegerField(default=0)
    
    verification=models.CharField(max_length=50,choices=(("Approved",'Approved'),("Rejected","Rejected"),("Pending","Pending")),default="Pending")
    
    active=models.BooleanField(default=True)
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='build_registrations'
  
class VappRegistrations(models.Model):
    first_name=models.TextField()
    last_name=models.TextField()
    company=models.TextField(null=True)
    # jobtitle=models.TextField(null=True)
    mobile=models.TextField(null=True)
    email=models.TextField(null=True)
    
    cardtype=models.ForeignKey(VappCardType, on_delete=models.CASCADE)
    vehicletype=models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    vehicle_number=models.TextField(null=True)
    
    id_proof_front=models.FileField(upload_to='id-proof-front/',null=True)
    id_proof_back=models.FileField(upload_to='id-proof-back/',null=True)
    vehicle_pass=models.FileField(upload_to='vehicle_pass/',null=True)
    
    delivery_date=models.DateField(null=True)
    remark=models.TextField(default='',null=True)
    collected=models.BooleanField(default=False)
    print_count=models.IntegerField(default=0)
    
    verification=models.CharField(max_length=50,choices=(("Approved",'Approved'),("Rejected","Rejected"),("Pending","Pending")),default="Pending")
    
    active=models.BooleanField(default=True)
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='vapp_registrations'

class EventRegistrations(models.Model):
    first_name=models.TextField()
    last_name=models.TextField()
    company=models.TextField(null=True)
    # jobtitle=models.TextField(null=True)
    cardtype=models.ForeignKey(EventCardType, on_delete=models.CASCADE)
    dob=models.DateField(null=True)
    nationality=models.TextField(null=True)
    mobile=models.TextField(null=True)
    email=models.TextField(null=True)
    
    id_proof_expiry=models.DateField(null=True)
    id_proof_type=models.CharField(max_length=50,choices=(("Passport-Id",'Passport-Id'),("Emirates-Id","Emirates-Id")),default="Emirates-Id")
    id_proof_number=models.TextField(null=True)
    id_proof_front=models.FileField(upload_to='id-proof-front/',null=True)
    id_proof_back=models.FileField(upload_to='id-proof-back/',null=True)
    
    badge_photo=models.FileField(upload_to='badge-images/',null=True)
    
    remark=models.TextField(default='',null=True)
    collected=models.BooleanField(default=False)
    print_count=models.IntegerField(default=0)
    
    verification=models.CharField(max_length=50,choices=(("Approved",'Approved'),("Rejected","Rejected"),("Pending","Pending")),default="Pending")
    
    active=models.BooleanField(default=True)
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table='event_registrations'

class Locations(models.Model):
    name=models.CharField(max_length=50)
    active=models.BooleanField(default=True)
    class Meta:
        db_table='event_locations'