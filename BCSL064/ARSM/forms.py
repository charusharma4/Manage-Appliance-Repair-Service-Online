from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Appliances
from .models import Contact
from .models import Notification
from .models import Customer
from .models import Technician
from .models import Complaints
from .models import Technician_assignment
from .models import Repair
from .models import Feedback

# Used for registering new users with basic details
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'password1', 'password2']

# Captures customer-specific information like address, gender, and city
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['address', 'gender', 'city']

# Used to store technician skills
class TechnicianForm(forms.ModelForm):
    class Meta:
        model = Technician
        fields = ['skill']
 
# Handles appliance details such as type, brand, and model       
class AppliancesForm(forms.ModelForm):
    class Meta:
        model = Appliances
        fields = ['type', 'brand_name', 'model']

# Allows users to submit complaints related to appliances 
class ComplaintsForm(forms.ModelForm):
    class Meta:
        model = Complaints
       # Includes priority, description, status, and service address
        fields = ['app_id', 'priority', 'description', 'status', 'service_address']

# Assigns technicians to complaints       
class Technician_assignmentForm(forms.ModelForm):
    class Meta:
        model=Technician_assignment
       # Tracks assignment status and remark
        fields = ['technician_id','status','remark']
        
# Records repair work done by technicians        
class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
       # Includes parts used and cost
        fields = ['work_done','parts_used','cost']
        
# Used for "Contact Us" functionality       
class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields=['cname','email','subject','message']
        
# Simple form for sending replies (subject + message)        
class ReplyForm(forms.Form):
    subject=forms.CharField(max_length=200)
    message=forms.CharField(widget=forms.Textarea)

# Collects customer feedback for completed complaints
class FeedbackForm(forms.ModelForm):
    class Meta:
        model=Feedback
        fields=['email','complaint_id','rating','comment'] 
 
# Used to respond to feedback       
class Replyfeedback(forms.Form):
    rating=forms.CharField(max_length=200)
    comment=forms.CharField(widget=forms.Textarea)

# Handles system/user notifications    
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['email','user_id','title','msg','type']
        

        