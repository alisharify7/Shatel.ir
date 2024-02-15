# cli commands

from flask.cli import AppGroup

MakeCommands = AppGroup("make", help="make and create default operation commands.")

# @MakeCommands.command("all")
# def backup_all_database():
#     """
#     """
#     permissions = current_app.config.get("ADMIN_DEFAULT_PERMISSION", None)
#     if not permissions:
#         print("there is no permission found")
#         sys.exit()
#
#     for permission in permissions:
#         print(f"{permission["Permission"]}:{permission["Description"]}")
#
#         permissionDB = Permission()
#         permissionDB.Permission = permission["Permission"]
#         permissionDB.Description = permission["Description"]
#         permissionDB.SetPublicKey()
#         permissionDB.save()
#
