import os
from dotenv import load_dotenv

load_dotenv()
# print(
#     f"sqlite:///"
#     + os.path.join(str(os.path.abspath("instance")), os.getenv("SQLALCHEMY_DATABASE_URI"))
# )

print(str(os.getenv("FOLDER")))
print(os.path.abspath(str(os.getenv("FOLDER"))))
print(os.getenv("SQLALCHEMY_DATABASE_URI"))
