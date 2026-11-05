from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from .forms import UserRegisterForm
from .forms import CustomerForm
from .forms import TechnicianForm
from .forms import AppliancesForm
from .forms import ComplaintsForm
from .forms import Technician_assignmentForm
from .forms import RepairForm
from .forms import ContactForm
from .forms import FeedbackForm
from .models import Appliances, Technician 
from .models import Technician_assignment
from .models import Repair
from .models import Complaints
from .models import Complaints
from .models import Contact
from .models import Feedback
from .models import Notification
from .forms import ContactForm
from .forms import NotificationForm
from django.core.mail import send_mail,BadHeaderError
from .forms import ReplyForm
from django.shortcuts import render 
from django.shortcuts import redirect

# Home page view
def home(request):
    #Render home page  
    return render(request, 'ARSM/home.html')  

# About page view
def about(request): 
    #Render about page 
    return render(request, 'ARSM/about.html')  


# -------------------- AUTHENTICATION -------------------- #

# Logout user and redirect to login page
def logout_view(request):
    #Logs out the user and redirects to login page
    logout(request)  # Ends user session
    return redirect('login')

def register_customer(request):
    """
    Handles customer registration:
    - Creates User
    - Assigns role = 'customer'
    - Creates related Customer profile
    """
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        customer_form = CustomerForm(request.POST)

        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'customer'
            user.save()  # password already hashed by UserCreationForm

            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()

            return redirect('login')
    else:
        user_form = UserRegisterForm()
        customer_form = CustomerForm()

    return render(request, 'ARSM/signup.html', {
        'user_form': user_form,
        'customer_form': customer_form
    })
    
def login_view(request):
    """
    Handles login:
    - Authenticates user using email & password
    - Redirects based on role (customer/technician/admin)
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            if user.role == 'customer':
                return redirect('customer_dashboard')
            elif user.role == 'technician':
                return redirect('technician_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
        else:
            return render(request, 'ARSM/login.html', {
                'error': 'Invalid email or password'
            })

    return render(request, 'ARSM/login.html')


@login_required
def register_technician_by_admin(request):
    
    #Allows only admin to register a technician
    if request.user.role != 'admin':
        return HttpResponse("Only admins allowed", status=403)

    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        technician_form = TechnicianForm(request.POST)

        if user_form.is_valid() and technician_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'technician'
            user.save()  # password already hashed

            technician = technician_form.save(commit=False)
            technician.user = user
            technician.save()

            return redirect('admin_dashboard')
    else:
        user_form = UserRegisterForm()
        technician_form = TechnicianForm()

    return render(request, 'ARSM/register_technician.html', {
        'user_form': user_form,
        'technician_form': technician_form
    })
    
#-----------****-------Dashboards------*****--------------# 

#-----------------Customer Dashboards---------------------#
@login_required 
def customer_dashboard(request): 
    #Customer dashboard access
    if getattr(request.user, 'role', None) != 'customer': 
        return HttpResponse("Sorry! You are not allowed to access the Customer Dashboard.", status=403) 
    return render(request, 'ARSM/customer_dashboard.html') 

#-----------------Techincian Dashboards---------------------#

@login_required 
def technician_dashboard(request):
    #Technician dashboard access 
    if getattr(request.user, 'role', None) != 'technician': 
        return HttpResponse("Sorry! You are not allowed...", status=403) 
    return render(request, 'ARSM/technician_dashboard.html') 

#------------------Admin Dashboards---------------------#

@login_required 
def admin_dashboard(request):
    #Admin dashboard access
    if getattr(request.user, 'role', None) != 'admin': 
        return HttpResponse("Sorry! You are not allowed...", status=403) 
    return render(request, 'ARSM/admin_dashboard.html')



from django.contrib.auth.decorators import login_required

#------------ F O R   A P P L I A N C E S --------------#

@login_required
def appliances_view(request):
    # Check if the user is sending data
    if request.method == 'POST':
        form = AppliancesForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user_id = request.user  # Automatically sets the logged-in user
            instance.save()
            messages.success(request, 'Appliance saved!')
            return redirect('success')
    else:
        form = AppliancesForm()
    return render(request, 'ARSM/appliances.html', {'form': form})

#----------------- Update Appliances ---------------------#

def update_appliances(request, pk):
    
    #Update existing appliance
    appliances=get_object_or_404(Appliances,pk=pk)
    
    if request.method == 'POST':
        form = AppliancesForm(request.POST , instance=appliances)
        if form.is_valid():
            form.save()
            return redirect('appliances_list')
    else:
        form = AppliancesForm(instance=appliances)
        
    return render(request, 'ARSM/update_appliances.html' , {'form': form})

#-------- If appliance update successfully ----------#

def success(request):
    return render(request,'ARSM/success.html')

#---------------- Delete Appliances record ----------------------#

def delete_appliances(request, pk):
    appliances = get_object_or_404(Appliances, pk=pk)
    
    if request.method == 'POST':
        appliances.delete()
        return redirect('appliances_list')
    
    return render(request,'ARSM/delete_appliances.html',{'appliances':appliances})

#----------------- Appliances Record ---------------------#

def appliances_list(request):
    # Fetching all appliances from the database
    appliances = Appliances.objects.filter(user_id=request.user)
    return render(request,'ARSM/appliances_list.html',{'appliances':appliances})



#---------------- F O R   C O M P L A I T S --------------------#

#----------------- For Customer Complaints ---------------------#

@login_required
def complaints_view(request):
    # Check if the user is sending data
    if request.method == 'POST':
        form = ComplaintsForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user_id = request.user  #sets the logged-in user
            complaint.save()
            send_email_notification(request.user, "Your complaint has been Saved. we will resolve it in 24 Hours!")
            return redirect('complaint_list')
    else:
        form = ComplaintsForm()
    return render(request, 'ARSM/complaints.html', {'form': form})


#----------------- For Technician Complaint --------------------#

def update_complaints_view(request,pk):
    complaints=get_object_or_404(Complaints,pk=pk)
    # Check if the user is sending data
    if request.method == 'POST':
        form = ComplaintsForm(request.POST , instance=complaints)
        if form.is_valid():
            form.save()
        return redirect('technician_dashboard')
    
    else:
        form = ComplaintsForm(instance=complaints)
        
    return render(request, 'ARSM/update_complaints.html' , {'form': form})

#-------------- customer cancel own complaint --------------#

def cancel_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaints, id=complaint_id)#define relationship with complaint model
    complaint.status = 'cancelled'
    complaint.save()
    return redirect('complaint_list')

#------ If technician complaint update successfull --------#

def success(request):
    return render(request,'ARSM/success.html')

#-------- technician check complaint record ----------# 

def complaint_tech_list(request):
    # Fetching all complaints from the database
    complaints= Complaints.objects.all()
    return render(request,'ARSM/complaint_tech_list.html',{'complaints':complaints})

#------------For customer complaint list-------------#
 
def complaint_list(request):
     # Fetching all complaints from the database
    complaint= Complaints.objects.filter(user_id=request.user)
    return render(request,'ARSM/complaint_list.html',{'complaint':complaint})



#------------ Cancel complaint by customer -------------#

def delete_complaint(request, pk):
    complaint = get_object_or_404(Complaints, pk=pk)
    
    if request.method == 'POST':
        complaint.delete()
        return redirect('complaint_list.html')
    
    return render(request,'ARSM/delete_complaint.html',{'complaint':complaint})

# -------- Admin check complaint record ----------#

def complaint_admin_list(request):
    # Fetching all complaints from the database
    complaint_admin= Complaints.objects.all()
    return render(request,'ARSM/complaint_admin_list.html',{'complaint_admin':complaint_admin})

#-----------For admin update complaint -----------#  

def update_complaints_admin(request,pk):
    complaint_admin=get_object_or_404(Complaints,pk=pk)
    
    if request.method == 'POST':
        form = ComplaintsForm(request.POST , instance=complaint_admin)
        if form.is_valid():
            form.save()
        return redirect('admin_dashboard')
    
    else:
        form = ComplaintsForm(instance=complaint_admin)
        
    return render(request, 'ARSM/update_complaints_admin.html' , {'complaint_admin': complaint_admin})

#------ If admin complaint update successfully --------#

def success(request):
    return render(request,'ARSM/success.html')

#-------------- Admin delete complaint ----------------#

def delete_complaints_admin(request, pk):
    complaint_admin = get_object_or_404(Complaints, pk=pk)
    
    if request.method == 'POST':
        complaint_admin.delete()
        return redirect('admin_dashboard')
    return render(request,'ARSM/delete_complaints_admin.html',{'complaint_admin':complaint_admin})

#------ F O R   T E C H N I C I A N   A S S I G N M E N T -------#

from django.shortcuts import render, get_object_or_404, redirect
from .models import Complaints


def technician_assignment_view(request, id):
    
   # Assign technician to complaint (admin)
    complaint = get_object_or_404(Complaints, id=id)
    
    if request.method == 'POST':
        form = Technician_assignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.complaint_id = complaint  
            assignment.save()
            return redirect('complaint_admin_list')  
        else:
            print("Form errors:", form.errors)  
    else:
        form = Technician_assignmentForm()
    
    return render(request, 'ARSM/technician_assignment_view.html', {
        'form': form,
        'complaint': complaint,
    })


#-------- For technician update technichian assignment -----------# 

def update_technician_assignment(request, pk):
    technician_assignment=get_object_or_404(Technician_assignment,pk=pk)
    
    if request.method == 'POST':
        form = Technician_assignmentForm(request.POST , instance=technician_assignment)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = Technician_assignmentForm(instance=technician_assignment)
        
    return render(request, 'ARSM/update_technician_assignment.html' , {'form': form})

#------ If technician assignment update successfully --------#

def success(request):
    return render(request,'ARSM/success.html')

#---------------- Delete technician assignment record ----------------------#

def delete_technician_assignment(request, pk):
    technician_assignment = get_object_or_404(Technician_assignment, pk=pk)
    
    if request.method == 'POST':
        technician_assignment.delete()
        return redirect('admin_dashboard')
    
    return render(request,'ARSM/delete_technician_assignment.html',{'technician_assignment':technician_assignment})

# -------- Admin check technician assignment record ----------#

def technician_assignment_list(request):
    # Fetching all technician assignment from the database
    technician_assignment= Technician_assignment.objects.all()
    return render(request,'ARSM/technician_assignment_list.html',{'technician_assignment':technician_assignment})

#-------------R E P A I R-------------#

#---------------- Admin update repair ------------------# 

def update_repair(request,pk):
    repair=get_object_or_404(Repair,pk=pk)
    
    if request.method == 'POST':
        form = RepairForm(request.POST , instance=repair)
        if form.is_valid():
            form.save()
        return redirect('admin_dashboard')
    
    else:
        form = RepairForm(instance=repair)
        
    return render(request, 'ARSM/update_repair.html' , {'form': form})

#------ If admin repair update successfully --------#

def success(request):
    return render(request,'ARSM/success.html')

#---------------- Delete repair record ----------------------#

def delete_repair(request, pk):
    repair = get_object_or_404(Repair, pk=pk)
    
    if request.method == 'POST':
        repair.delete()
        return redirect('admin_dashboard')
    return render(request,'ARSM/delete_repair.html',{'repair':repair})

# -------- Admin check repair record ----------#

def repair_admin_list(request):
    # Fetching all repair from the database
    repair= Repair.objects.all()
    return render(request,'ARSM/repair_admin_list.html',{'repair':repair})

#----------------- For technician Repair ----------------------#
@login_required
def repair_view(request, id):
    
   # Technician submits repair details:
    # Links to complaint
    # Updates complaint status to completed
    
    complaint = get_object_or_404(Complaints, id=id)

    if request.method == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():
            repair = form.save(commit=False)

            # Assign complaint correctly
            repair.complaint_id = complaint 

            # Assign technician instance
            try:
                technician = Technician.objects.get(user=request.user)
                repair.technician_id = technician
            except Technician.DoesNotExist:
                return HttpResponse("You are not a registered technician.", status=403)

            repair.save()
             # Update complaint status
            complaint.status = 'Completed' 
            complaint.save()
            send_email_notification(request.user, "Your complaint has bee resolved Successfully!")
            return redirect('complaint_tech_list')
        else:
            print(form.errors)  # debug form errors
    else:
        form = RepairForm()

    return render(request, 'ARSM/repair_view.html', {
        'form': form,
        'complaint': complaint,
    })

#----------- technician update repair -----------# 

def update_repairs(request,pk):
    repairs=get_object_or_404(Repair,pk=pk)
    
    if request.method == 'POST':
        form = RepairForm(request.POST , instance=repairs)
        if form.is_valid():
            form.save()
        return redirect('technician_dashboard')
    
    else:
        form = RepairForm(instance=repairs)
        
    return render(request, 'ARSM/update_repairs.html' , {'form': form})

#------ If technician repair update successfully --------#

def success(request):
    return render(request,'ARSM/success.html')

# -------- technician check repair record ----------#

def repair_tech_list(request):
    # Fetching all repairs from the database
    repairs= Repair.objects.all()
    return render(request,'ARSM/repair_tech_list.html',{'repairs':repairs})


#------------------- E M A I L  --------------#

#----------- F O R     C O N T A C T ------------#
def contact_view(request):
    # Check if the user is sending data
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('success')
        else:
            print(form.errors)   # show errors in terminal
    else:
        form = ContactForm()

    return render(request, 'ARSM/contact.html', {'form': form})

# -------- Admin check contact record ----------# 

def contact_list(request):
     # Fetching all contacts from the database
    contacts = Contact.objects.all().order_by('-create_at')
    return render(request, "ARSM/contact_list.html", {"contacts": contacts})


#------- Admin reply message of customer -------#
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from .models import Contact

def reply_message(request, id):
    contact = get_object_or_404(Contact, id=id)

    if request.method == "POST":
        reply = request.POST.get("reply")

        try:
            # Try sending the email
            send_mail(
                subject=f"Reply: {contact.subject}",
                message=reply,
                from_email="charu4440@gmail.com",
                recipient_list=[contact.email],
                fail_silently=False,
            )
        except BadHeaderError:
            messages.error(request, "Invalid header detected. Email not sent.")
            return render(request, "ARSM/reply_message.html", {"contact": contact})
        except Exception as e:
            messages.error(request, f"Error sending email: {str(e)}")
            return render(request, "ARSM/reply_message.html", {"contact": contact})

        try:
            # Update the contact status
            contact.status = "replied"
            contact.save()
        except Exception as e:
            messages.warning(request, f"Email sent but could not update status: {str(e)}")
            return render(request, "ARSM/reply_message.html", {"contact": contact})

        messages.success(request, "Reply sent successfully.")
        return redirect("contact_list")

    return render(request, "ARSM/reply_message.html", {"contact": contact})

#---------- F O R   F E E D B A C K ----------#

def feedback_view(request):
    # Check if the user is sending data
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,' thank you for Feedback !')
            return redirect('success')
    else:
        form = FeedbackForm()
    return render(request,'ARSM/feedback.html',{'form': form})

#-------- Admin check feedback record ----------#

def feedback_list(request):
    # Fetching all feedbacks from the database
    feedback= Feedback.objects.all()
    return render(request,'ARSM/feedback_list.html',{'feedback':feedback})

#------- Admin reply message of customer -------#

def feedback_reply(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    if request.method == "POST":
        reply = request.POST.get("reply")
        try:
            # Attempt to send the email
            send_mail(
             "Reply of Feedback: ",
                reply,
                "charu4440@gmail.com",
                [feedback.email],
                fail_silently=False,
             )
        except BadHeaderError:
            messages.error(request, "Invalid header found. Email not sent.")
            return render(request, "ARSM/feedback_reply.html", {"feedback": feedback})
        except Exception as e:
            # Catch any other exceptions (like connection issues)
            messages.error(request, f"An error occurred while sending email: {str(e)}")
            return render(request, "ARSM/feedback_reply.html", {"feedback": feedback})

        # If email sent successfully, update feedback status
        feedback.admin_reply = "replied"
        feedback.save()

        return redirect("feedback_list")

    return render(request, "ARSM/feedback_reply.html", {"feedback": feedback})

#------- N O T I F I C A T I O N ---------#

def notification_view(request):
    # Check if the user is sending data
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,' thank you !')
            return redirect('success')
    else:
        form = NotificationForm()
    return render(request,'ARSM/notification.html',{'form': form})

#-------- Admin check feedback record ----------#
def notification_list(request):
    # Fetching all feedbacks from the database
    notification = Appliances.objects.filter(user_id=request.user)
    return render(request,'ARSM/notification_list.html',{'notification':notification})

def delete_notification(request,pk):
    notification=get_object_or_404(Notification, pk=pk)

    if request.method == 'POST':
        notification.delete()
        return redirect('notification_list')
    
    return render(request,'ARSM/delete_notification.html',{'notification':notification})
    
from django.core.mail import send_mail
from django.conf import settings
from .models import Notification


def send_email_notification(user, message):
    notification = Notification.objects.create(
        user_id=user,   
        title="Complaint Update",
        msg=message,
        type='email'
    )

    try:
        send_mail(
            subject='Microfinance Loan Update',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

    except Exception as e:
        print("Email failed:", e)
        
#------------------- P A Y M E M E N T ------------------#
    
from django.shortcuts import render, get_object_or_404
from .models import Repair

from django.shortcuts import get_object_or_404, render

def repair_invoice(request, complaint_id):
    complaint = get_object_or_404(Complaints, id=complaint_id)

    repair = complaint.repair_profile

    return render(request, 'ARSM/invoice.html', {
        'complaint': complaint,
        'repair': repair
    })
    
    
    

def service_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    complaints = Complaints.objects.all()

    if start_date and end_date:
        complaints = complaints.filter(
            Complaint_date__date__gte=start_date,
            Complaint_date__date__lte=end_date
        )

    context = {
        'complaints': complaints,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, "ARSM/service_report.html", context)