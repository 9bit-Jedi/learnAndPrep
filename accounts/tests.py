from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from accounts.models import UserMobileNoOTP, UserOTP, User
from django.core.validators import ValidationError
from unittest.mock import patch

class UserModelTest(TestCase):

  def test_create_user(self):
    user = User.objects.create_user(
      email="test@example.com",
      name="Test User",
      mobile_no="1234567890",
      password="strongpassword",
    )
    self.assertEqual(user.email, "test@example.com")
    self.assertEqual(user.name, "Test User")
    self.assertEqual(user.mobile_no, "1234567890")
    self.assertTrue(user.is_active)
    self.assertFalse(user.is_staff)
    self.assertFalse(user.is_superuser)

  def test_create_superuser(self):
    user = User.objects.create_superuser(
      email="admin@example.com",
      name="Admin User",
      mobile_no="9876543210",
      password="adminpassword",
    )
    self.assertEqual(user.email, "admin@example.com")
    self.assertEqual(user.name, "Admin User")
    self.assertEqual(user.mobile_no, "9876543210")
    self.assertTrue(user.is_active)
    self.assertTrue(user.is_staff)
    self.assertTrue(user.is_superuser)

  def test_invalid_email(self):
    with self.assertRaises(ValueError):
      User.objects.create_user(
        email="",
        name="Test User",
        mobile_no="1234567890",
        password="strongpassword",
      )

  def test_invalid_mobile_no(self):
    with self.assertRaises(ValueError):
      User.objects.create_user(
        email="test@example.com",
        name="Test User",
        mobile_no="invalid_number",
        password="strongpassword",
      )


class UserOTPModelTest(TestCase):

  @patch("django.utils.timezone.now")
  def test_otp_creation(self, mock_now):
    mock_now.return_value = timezone.now()
    user_otp = UserOTP.objects.create(
      email="test@example.com",
      otp="123456",
      temp_user_data={"name": "Test User", "mobile_no": "1234567890"},
    )
    self.assertEqual(user_otp.email, "test@example.com")
    self.assertEqual(user_otp.otp, "123456")
    self.assertEqual(
      user_otp.temp_user_data, {"name": "Test User", "mobile_no": "1234567890"}
    )
    self.assertIsNotNone(user_otp.otp_created_at)

  def test_otp_is_expired(self):
    user_otp = UserOTP.objects.create(
      email="test@example.com",
      otp="123456",
      otp_created_at=timezone.now() - timedelta(minutes=11),
    )
    self.assertTrue(user_otp.is_otp_expired())

  def test_otp_is_not_expired(self):
    user_otp = UserOTP.objects.create(
      email="test@example.com",
      otp="123456",
      otp_created_at=timezone.now() - timedelta(minutes=9),
    )
    self.assertFalse(user_otp.is_otp_expired())


class UserMobileNoOTPModelTest(TestCase):

  @patch("django.utils.timezone.now")
  def test_otp_creation(self, mock_now):
    mock_now.return_value = timezone.now()
    user_mobile_no_otp = UserMobileNoOTP.objects.create(
      mobile_no="1234567890",
      otp="123456",
    )
    self.assertEqual(user_mobile_no_otp.mobile_no, "1234567890")
    self.assertEqual(user_mobile_no_otp.otp, "123456")
    self.assertIsNotNone(user_mobile_no_otp.otp_created_at)

  def test_otp_is_expired(self):
    user_mobile_no_otp = UserMobileNoOTP.objects.create(
      mobile_no="1234567890",
      otp="123456",
      otp_created_at=timezone.now() - timedelta(minutes=11),
    )
    self.assertTrue(user_mobile_no_otp.is_otp_expired())

  def test_otp_is_not_expired(self):
    user_mobile_no_otp = UserMobileNoOTP.objects.create(
      mobile_no="1234567890",
      otp="123456",
      otp_created_at=timezone.now() - timedelta(minutes=9),
    )
    self.assertFalse(user_mobile_no_otp.is_otp_expired())

  def test_invalid_mobile_no(self):
    with self.assertRaises(ValidationError):
      UserMobileNoOTP.objects.create(
        mobile_no="invalid_number",
        otp="123456",
      )
