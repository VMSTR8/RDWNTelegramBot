from tortoise.exceptions import (
    IntegrityError,
    DoesNotExist
)

from models import (
    Topics,
    Users,
    EventDetails,
    EventPolls,
)


class UsersHandler:
    """
    UsersHandler class provides methods to handle operations
    related to users in the database.

    Methods
    -------
    is_user_admin(telegram_id: int) -> bool:
        Checks if the user with the given telegram_id is an admin.

    add_users(telegram_ids: list[int]) -> None:
        Adds a list of telegram_ids to the database, skipping existing users.

    delete_user(telegram_id: int) -> None:
        Deletes the user with the given telegram_id from the database.

    update_callsign(telegram_id: int, new_callsign: str) -> Users:
        Updates the callsign of the user with the given telegram_id.

    get_reserved(telegram_id: int) -> bool:
        Gets the reserved status of the user with the given telegram_id.

    update_reserved(telegram_id: int) -> Users:
        Toggles the reserved status of the user with the given telegram_id.

    get_warn(telegram_id: int) -> int:
        Gets the warn count of the user with the given telegram_id.

    update_warn(telegram_id: int, warn: int) -> Users:
        Updates the warn count of the user with the given telegram_id.
    """

    @staticmethod
    async def is_user_admin(telegram_id: int) -> bool:
        """
        Checks if the user with the given telegram_id is an admin.

        Parameters
        ----------
        telegram_id : int
            The ID of the user to check.

        Returns
        -------
        bool
            True if the user is an admin, False otherwise.
        """
        user = await Users.filter(telegram_id=telegram_id).first()
        return user.admin if user else False

    @staticmethod
    async def get_user_info(telegram_id: int) -> dict:
        """
        Retrieves all information about the user with the given
        telegram_id in a dictionary format.

        Parameters
        ----------
        telegram_id : int
            The ID of the user to retrieve information for.

        Returns
        -------
        dict
            A dictionary containing all information about the user.

        Raises
        ------
        DoesNotExist
            If the user with the given telegram_id does not exist.
        """
        user = await Users.filter(telegram_id=telegram_id).first()
        if not user:
            raise DoesNotExist(f'User with id {telegram_id} does not exist.')

        user_info = {
            'id': user.id,
            'telegram_id': user.telegram_id,
            'admin': user.admin,
            'reserved': user.reserved,
            'warn': user.warn,
            'callsign': user.callsign
        }

        return user_info

    @staticmethod
    async def add_users(users_ids: list[int]) -> list[Users]:
        """
        Adds a list of telegram_ids to the database,
        skipping existing users.

        Parameters
        ----------
        telegram_ids : list[int]
            The list of user IDs to add.
        """
        added_users = []
        for telegram_id in users_ids:
            user = Users.filter(telegram_id=telegram_id).first()
            if not user:
                user = await Users.create(telegram_id=telegram_id)
                added_users.append(user)
        return added_users

    @staticmethod
    async def delete_user(telegram_id: int) -> None:
        """
        Deletes the user with the given telegram_id from the database.

        Parameters
        ----------
        telegram_id : int
            The ID of the user to delete.

        Raises
        ------
        DoesNotExist
            If the user with the given telegram_id does not exist.
        """
        user = await Users.filter(telegram_id=telegram_id).first()
        if not user:
            raise DoesNotExist(f'User with id {telegram_id} does not exist.')
        await user.delete()

    @staticmethod
    async def update_callsign(telegram_id: int, new_callsign: str) -> Users:
        """
        Updates the callsign of the user with the given telegram_id.

        Parameters
        ----------
        telegram_id : int
            The ID of the user to update.
        new_callsign : str
            The new callsign for the user.

        Returns
        -------
        Users
            The updated user object.

        Raises
        ------
        DoesNotExist
            If the user with the given telegram_id does not exist.
        """
        user = await Users.filter(telegram_id=telegram_id).first()
        if not user:
            raise DoesNotExist(f'User with id {telegram_id} does not exist.')

        existing_user = await Users.filter(callsign=new_callsign).first()
        if existing_user:
            raise IntegrityError('Callsign already exists.')

        user.callsign = new_callsign
        await user.save()
        return user

    # @staticmethod
    # async def get_reserved(telegram_id: int) -> bool:
    #     """
    #     Gets the reserved status of the user with the given telegram_id.

    #     Parameters
    #     ----------
    #     telegram_id : int
    #         The ID of the user to get the reserved status for.

    #     Returns
    #     -------
    #     bool
    #         The reserved status of the user.

    #     Raises
    #     ------
    #     DoesNotExist
    #         If the user with the given telegram_id does not exist.
    #     """
    #     user = await Users.filter(telegram_id=telegram_id).first()
    #     if not user:
    #         raise DoesNotExist(f'User with id {telegram_id} does not exist.')
    #     return user.reserved

    @staticmethod
    async def update_reserved(telegram_id: int) -> Users:
        """
        Toggles the reserved status of the user with the given telegram_id.

        Parameters
        ----------
        telegram_id : int
            The ID of the user to update.

        Returns
        -------
        Users
            The updated user object.

        Raises
        ------
        DoesNotExist
            If the user with the given telegram_id does not exist.
        """
        user = await Users.filter(telegram_id=telegram_id).first()
        if not user:
            raise DoesNotExist(f'User with id {telegram_id} does not exist.')
        user.reserved = not user.reserved
        await user.save()
        return user

    # @staticmethod
    # async def get_warn(telegram_id: int) -> int:
    #     """
    #     Gets the warn count of the user with the given telegram_id.

    #     Parameters
    #     ----------
    #     telegram_id : int
    #         The ID of the user to get the warn count for.

    #     Returns
    #     -------
    #     int
    #         The warn count of the user.

    #     Raises
    #     ------
    #     DoesNotExist
    #         If the user with the given telegram_id does not exist.
    #     """
    #     user = await Users.filter(telegram_id=telegram_id).first()
    #     if not user:
    #         raise DoesNotExist(f'User with id {telegram_id} does not exist.')
    #     return user.warn

    @staticmethod
    async def update_warn(telegram_id: int, warn: int) -> Users:
        """
        Updates the warn count of the user with the given telegram_id.

        Parameters
        ----------
        telegram_id : int
            The ID of the user to update.
        warn : int
            The new warn count for the user.

        Returns
        -------
        Users
            The updated user object.

        Raises
        ------
        DoesNotExist
            If the user with the given telegram_id does not exist.
        """
        user = await Users.filter(telegram_id=telegram_id).first()
        if not user:
            raise DoesNotExist(f'User with id {telegram_id} does not exist.')
        user.warn = warn
        await user.save()
        return user
