class Permissions:

    @staticmethod
    def is_admin(user):
          return user.role.lower().strip() == "system administrator"


    @staticmethod
    def is_store(user):
        return user.role.lower().strip() == "store user"

    @staticmethod
    def is_inventory(user):
        return user.role.lower().strip() == "inventory users"