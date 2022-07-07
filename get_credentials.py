#
# from google.cloud import secretmanager
# # Instantiate the Secret Manager client.
# sm_client = secretmanager.SecretManagerServiceClient()
#
# # Load secrets
# name = sm_client.secret_version_path("stone-lodge-353709","db_name", 1)
# response = sm_client.access_secret_version(name)
# secrets_pass = response.payload.data.decode('UTF-8')
# passwords = [secrets_pass]
# print(passwords)
from google.cloud import storage
from google.cloud import storage
# def implicit():
#
#
#     # If you don't specify credentials when constructing the client, the
#     # client library will look for credentials in the environment.
#     storage_client = storage.Client()
#
#     # Make an authenticated API request
#     buckets = list(storage_client.list_buckets())
#     print(buckets)
#
# implicit()