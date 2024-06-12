from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import phonenumbers

# Create your models here.
# custom user manager
class MyUserManager(BaseUserManager):
    def normalize_mobile_no(self, mobile_no):
        try:
            parsed_no = phonenumbers.parse(mobile_no, "IN")  # Replace "US" with your default region if needed
            if not phonenumbers.is_valid_number(parsed_no):
                raise ValueError("Invalid mobile number")
            return phonenumbers.format_number(parsed_no, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException as e:
            raise ValueError(f"Error parsing phone number: {str(e)}")
        
    def create_user(self, email, name , mobile_no , password=None , password2 = None):
        """
        Creates and saves a User with the given email, name, mobile and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name = name,
            mobile_no = self.normalize_mobile_no(mobile_no),
           

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name , mobile_no , password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name = name,
            mobile_no=mobile_no,
            password2=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# custom user model
class User(AbstractBaseUser):
    

    name = models.CharField(max_length=30 ,blank = False)
    mobile_no = models.CharField(verbose_name="Mobile Number",max_length=15 , blank = False)
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
        blank = False,
    )


    # fields for selecting classes
    is_class_11th = models.BooleanField(default=False)
    is_class_12th = models.BooleanField(default=False)
    is_dropper = models.BooleanField(default=False)


    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    create_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "mobile_no"]

    # CREATING OBJECT OF USER MANAGER 
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

