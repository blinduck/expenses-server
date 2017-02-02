from ..serializers import UserSerializer

def run():
  data = {
    'household': 'something',
    "username": "whee",
    "password": "password",
    "password_repeat": "password"}
  ser = UserSerializer(data=data)
  try:
    print(ser.is_valid())
    print(ser.errors)
    user = ser.save()
    print(user, user.password)
  except Exception as e:
    print("exception", e)
