from django.db import models
from django.contrib.auth.models import AbstractUser
#-------User Table
class User(AbstractUser):
    username = None  # remove username

    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('technician', 'Technician'),
        ('admin', 'Admin'),
    )

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=2000, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone']

    def __str__(self):
        return f"{self.full_name} ({self.role})"

#-------Customer Table
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    address = models.TextField()
    gender = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100)
    email =models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Customer: {self.user.full_name}"

#-------Technician Table
class Technician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="technician_profile")
    skill = models.TextField()

    def __str__(self):
        return f"Technician: {self.user.full_name}"

#-------Appliances Table  
class Appliances(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=200)
    brand_name = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand_name} {self.model} ({self.type})"
    
#-------Complaints Table   
class Complaints(models.Model):
    priority = (
        ('high','High'),
        ('low','Low'),
    )

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    app_id = models.ForeignKey(Appliances, on_delete=models.CASCADE)
    priority = models.CharField(max_length=100, choices=priority)
    description = models.CharField(max_length=200)
    
    status = models.CharField(max_length=200, default='pending')

    service_address = models.CharField(max_length=2000)
    Complaint_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint #{self.id} - {self.user_id.full_name}"

#-------Technician Assignment Table   
class Technician_assignment(models.Model):
    complaint_id=models.OneToOneField(Complaints, on_delete=models.CASCADE, related_name="complaint_profile")
    technician_id=models.ForeignKey(Technician, on_delete=models.CASCADE)
    assign_date=models.DateTimeField(auto_now_add=True)
    Complaint_date=models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=2000)
    remark= models.CharField(max_length=2000)
    
    def __str__(self):
        return f"Technician_assignment:{self.complaint_id}"

#-------Repair Table     
class Repair(models.Model):
    complaint_id=models.OneToOneField(Complaints, on_delete=models.CASCADE, related_name="repair_profile")
    technician_id=models.ForeignKey(Technician, on_delete=models.CASCADE,related_name="repair_tech")
    work_done=models.CharField(max_length=2000)
    parts_used=models.CharField(max_length=2000)
    cost=models.IntegerField()
    repair_date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Repair:{self.complaint_id} {self.work_done}{self.parts_used} ({self.cost})" 
    
#-------Contact Table     
class Contact(models.Model):
    cname=models.CharField(max_length=100)
    email=models.EmailField()
    subject=models.CharField(max_length=100)
    message=models.TextField()
    status=models.TextField(default="not reply")
    create_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.cname
    
#-------Feedback Table   
class Feedback(models.Model):
    complaint_id=models.OneToOneField(Complaints, on_delete=models.CASCADE, related_name="feedback_profile")
    email=models.EmailField()
    rating = models.IntegerField()
    comment=models.CharField(max_length=100)
    admin_reply=models.TextField(default="not reply")
    Feedback_date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback:{self.complaint_id}"
 
class Notification(models.Model):
    email=models.EmailField(default="null")
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=300)
    msg=models.CharField(max_length=300)
    send_date=models.DateTimeField(auto_now_add=True)
    type=models.CharField(max_length=300)
    
    def __str__(self):
        return f"Notification:{self.email} {self.user_id} {self.title} {self.msg} ({self.type})"
  

class Payment(models.Model):
    #Choices for payment modes
    PAYMENT_MODES = [
        ('COD','Cash on Delivery'),
        ('UPI','UPI/GPay'),
        ('CARD','Credit/Debit Card'),
        ('NET_BANKTNG','Net Banking'),
    ]
    
    complaint_id=models.OneToOneField(Complaints, on_delete=models.CASCADE, related_name="payment_profile")
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    pmode=models.CharField(max_length=20,choices=PAYMENT_MODES)
    pdate=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=20,default='Pending')
    
    def __str__(self):
        return f"Payment{self.id} for Order {self.complaint_id.id}"
    
