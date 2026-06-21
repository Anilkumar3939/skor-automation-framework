from utils.db_helper import DBHelper
from utils.queries import *

db = DBHelper()

phone = "8100111179"

# print(get_state(db, 'SC062026000082'))
user_id = 'SC062026000084'

print(get_uw_user_taran(db, user_id))

# print("\n===== CHECK PHONE EXISTS =====")
# print(check_phone_exists(db, phone))

# print("\n===== GET USER ID =====")
# user_id = get_user_id(db, phone)
# print(user_id)

# if user_id:

#     print("\n===== GET USER DETAILS =====")
#     print(get_user_details(db, phone))

#     print("\n===== GET USER SETTINGS =====")
#     print(get_user_settings(db, user_id))

#     print("\n===== GET DEVICE DETAILS =====")
#     print(get_device_details(db, user_id))

#     print("\n===== GET LOCATION DETAILS =====")
#     print(get_location_details(db, user_id))

#     print("\n===== GET APPSFLYER =====")
#     print(get_appsflyer(db, user_id, "FIREBASE"))

#     print("\n===== GET OTP VERIFIED =====")
#     print(get_otp_verified(db, user_id))

#     print("\n===== GET USER PRODUCT MAPPING =====")
#     print(get_user_product_mapping(db, user_id, "BMI"))

#     print("\n===== GET STATE =====")
#     print(get_state(db, user_id))

#     print("\n===== GET STATE AUDIT =====")
#     print(get_state_audit(db, user_id))

#     print("\n===== GET CAMPAIGN =====")
#     print(get_campaign(db, user_id))

#     print("\n===== GET REFERRAL =====")
#     print(get_referral(db, user_id, phone))

# else:
#     print("\n❌ No user_id found")