from utils.api_helpers import APIHelper

response = APIHelper.initiate_taran(
    'SC052026000122',
    '995fb22e-5a1e-4bcf-84a3-b679a40e6bea'
    
)
print(response.status_code)