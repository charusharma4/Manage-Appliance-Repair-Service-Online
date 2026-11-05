from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # -------------------- Home & Static Pages -------------------- #
    path('', views.home, name='home'),  # Homepage
    path('about/', views.about, name='about'),  # About page
    path('contact/', views.contact_view, name='contact'),  # Contact form
    path('reply/<int:id>/', views.reply_message, name='reply_message'),  # Reply to contact message
    path('contact-list/', views.contact_list, name="contact_list"),  # Admin view of contact messages

    # -------------------- Authentication -------------------- #
    path('signup/', views.register_customer, name='signup'),  # User registration
    path('login/', views.login_view, name='login'),  # Login page
    path('logout/', views.logout_view, name='logout'),  # Logout user
    path('success/', views.success, name='success'),  # Success page after actions

    # -------------------- Dashboards -------------------- #
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),  # Customer dashboard
    path('technician_dashboard/', views.technician_dashboard, name='technician_dashboard'),  # Technician dashboard
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('technician_dashboard/', views.technician_dashboard, name='technician_dashboard'),
    path('register_technician/', views.register_technician_by_admin, name='register_technician_admin'),  # Admin registers technician

    # -------------------- Password Reset -------------------- #
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),  # Enter email
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),  # Email sent
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # Reset confirmation
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  # Reset complete

    # -------------------- Appliances -------------------- #
    path('appliances/', views.appliances_view, name='appliances'),  # Add/view appliances
    path('appliances/update/<int:pk>/', views.update_appliances, name='update_appliances'),  # Update appliance
    path('appliances/delete/<int:pk>/', views.delete_appliances, name='delete_appliances'),  # Delete appliance
    path('appliances_list/', views.appliances_list, name='appliances_list'),  # List appliances

    # -------------------- Complaints -------------------- #
    path('complaints/', views.complaints_view, name='complaints'),  # Submit complaint
    path('complaint_tech_list/', views.complaint_tech_list, name='complaint_tech_list'),  # Technician complaint list
    path('complaint_list/', views.complaint_list, name='complaint_list'),  # Customer complaint list
    path('complaint/admin_list/', views.complaint_admin_list, name='complaint_admin_list'),  # Admin complaint list

    # -------------------- Technician Assignment -------------------- #
    path('technician_assignment_view/<int:id>/', views.technician_assignment_view, name='technician_assignment_view'),  # Assign technician
    path('update/technician_assignment/<int:pk>/', views.update_technician_assignment, name='update_technician_assignment'),  # Update assignment
    path('delete/technician_assignment/<int:pk>/', views.delete_technician_assignment, name='delete_technician_assignment'),  # Delete assignment
    path('technician_assignment_list/', views.technician_assignment_list, name='technician_assignment_list'),  # Assignment list


    # -------------------- Repair (Admin) -------------------- #
    path('update_repair/<int:pk>/', views.update_repair, name='update_repair'),  # Update repair
    path('delete_repair/<int:pk>/', views.delete_repair, name='delete_repair'),  # Delete repair
    path('repair_admin_list/', views.repair_admin_list, name='repair_admin_list'),  # Admin repair list

    # -------------------- Repair (Technician) -------------------- #
    path('repair_view/<int:id>/', views.repair_view, name='repair_view'),  # Technician repair view
    
    
    path('update_repairs/<int:pk>/', views.update_repairs, name='update_repairs'),  # Update repair (technician)
    path('repair_tech_list/', views.repair_tech_list, name='repair_tech_list'),  # Technician repair list

    # Cancel complaint
    path('cancel-complaint/<int:complaint_id>/', views.cancel_complaint, name='cancel_complaint'),

    # -------------------- Feedback -------------------- #
    path('feedback/', views.feedback_view, name='feedback'),  # Submit feedback
    path('admin_dashboard/feedback_list/', views.feedback_list, name='feedback_list'),  # Admin feedback list
    path('feedback_reply/<int:id>/', views.feedback_reply, name='feedback_reply'),  # Reply to feedback

    # -------------------- Notifications -------------------- #
    path('notification/', views.notification_view, name='notification'),  # Create notification
    path('customer_dashboard/notification_list/', views.notification_list, name='notification_list'),  # Customer notifications
    path('delete_notification/<int:pk>/', views.delete_notification, name='delete_notification'),  # Delete notification
    # URL for generating repair invoice based on complaint ID
    path('complaint_list/invoice/<int:complaint_id>/',views.repair_invoice, name='repair_invoice'),
    # URL for viewing the service report page
    path('service-report/', views.service_report, name='service_report'),
]