from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, IDCard
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.conf import settings
from threading import Thread

@receiver(post_save, sender=User)
def set_user_inactive(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        if instance.is_active:  # Only set inactive if not already
            instance.is_active = False
            instance.save(update_fields=["is_active"])
        # Send email asynchronously
        def send_pending_email():
            send_mail(
                subject="Welcome to Sule Hamma Library!",
                message=(
                    "Dear {},\n\n"
                    "Thank you for registering with Sule Hamma Library, Northwest University Kano. "
                    "Your account has been created and is pending approval by the library management. "
                    "You will receive another email once your account is approved and activated.\n\n"
                    "Best regards,\nSule Hamma Library Management\nNorthwest University Kano"
                ).format(instance.get_full_name() or instance.username),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=True,
            )
        Thread(target=send_pending_email).start()
    elif not created and instance.is_active:
        # Send email asynchronously when approved
        def send_approved_email():
            send_mail(
                subject="Approval and Congratulations on Gaining Access to Sule Hamma Library",
                message=(
                    "Dear {},\n\n"
                    "On behalf of the Management of Sule Hamma Library, Northwest University Kano, we are pleased to congratulate you on being officially approved as a registered user of our University Library. This approval grants you access to one of the most resourceful academic information centers in the region, designed to support teaching, learning, and research excellence.\n\n"
                    "Your membership symbolizes a commitment to academic integrity, intellectual growth, and responsible use of library resources.\n\n"
                    "Roles and Responsibilities of Registered Users\n"
                    "1. Academic Engagement: Utilize the library for research, study, and academic development only.\n"
                    "2. Resource Protection: Handle books, journals, e-resources, and equipment with utmost care.\n"
                    "3. Information Literacy: Strive to improve your knowledge of information search, citation, and referencing practices.\n"
                    "4. Contribution to Orderliness: Maintain a quiet, conducive learning environment at all times.\n"
                    "5. Collaboration: Cooperate with library staff and fellow users to ensure smooth operations.\n\n"
                    "Rules and Regulations\n"
                    "1. General Conduct\n"
                    "- Silence must be observed within the library premises.\n"
                    "- Use of mobile phones inside reading halls is prohibited.\n"
                    "- Eating, drinking, or smoking in the library is strictly forbidden.\n\n"
                    "2. Borrowing Rights\n"
                    "- Undergraduate students may borrow up to 2 books for 1 week, renewable once.\n"
                    "- Postgraduate and staff users may borrow up to 4 books for 2 weeks.\n"
                    "- Reference materials, rare books, and reserved collections are for in-library use only.\n\n"
                    "3. Use of ICT and E-Resources\n"
                    "- Computers and internet services are provided strictly for academic purposes.\n"
                    "- Users must not attempt to alter library systems or misuse databases.\n"
                    "- E-resources accessed through institutional subscriptions must not be downloaded in bulk or shared externally.\n\n"
                    "4. Discipline and Sanctions\n"
                    "- Late return of borrowed materials attracts fines as determined by the library.\n"
                    "- Loss or damage of materials must be reported immediately and replaced.\n"
                    "- Any form of misconduct, including plagiarism, theft, or vandalism, may result in suspension of library privileges or disciplinary action by the University.\n\n"
                    "Library Services Available to You\n"
                    "- Access to print and electronic resources (books, journals, theses, and reports).\n"
                    "- Digital Library Section with e-databases and online journals.\n"
                    "- Reference and Information Services for research assistance.\n"
                    "- Study carrels, discussion rooms, and ICT facilities.\n"
                    "- Current Awareness Services to keep you informed of new resources.\n\n"
                    "Conclusion\n\n"
                    "Once again, congratulations on being admitted as a user of Sule Hamma Library. We encourage you to maximize these resources to enhance your academic pursuit and uphold the core values of the University.\n\n"
                    "We look forward to supporting you throughout your academic journey.\n\n"
                    "Authorized by:\nAssociate Professor Karimatu Isah Maisango\nUniversity Librarian\nSule Hamma Library\nNorthwest University, Kano"
                ).format(instance.get_full_name() or instance.username),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=True,
            )
        Thread(target=send_approved_email).start()

@receiver(post_save, sender=User)
def create_or_update_id_card(sender, instance, created, **kwargs):
    if not instance.student_id:
        # Don't create IDCard if student_id is missing
        return
    # Only create IDCard if user is active (approved)
    if instance.is_active:
        id_card, created_card = IDCard.objects.get_or_create(
            user=instance,
            defaults={
                'id_number': instance.student_id,
                'faculty': instance.faculty,
                'department': instance.department,
                'student_category': instance.student_category,
            }
        )
        if not created_card:
            id_card.id_number = instance.student_id
            id_card.faculty = instance.faculty
            id_card.department = instance.department
            id_card.student_category = instance.student_category
            id_card.save()



@receiver(post_save, sender=User)
def assign_all_groups_to_staff(sender, instance, created, **kwargs):
    """
    Automatically assign all groups to a user if they are staff.
    """
    if instance.is_staff:
        all_groups = Group.objects.all()
        instance.groups.set(all_groups)  # Assign all groups
    else:
        # Optional: Remove groups if not staff anymore
        instance.groups.clear()