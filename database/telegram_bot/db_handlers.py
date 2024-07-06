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


class TopicsHandler:
    """
    TopicsHandler class provides methods to handle operations
    related to topics in the database.

    Methods
    -------
    create_topic(topic_id: int, topic_name: str) -> dict:
        Creates a new topic with the specified topic_id and topic_name,
        and returns information about the created topic in dictionary format.

    get_topic_info(topic_id: int) -> dict:
        Retrieves information about the topic with
        the given topic_id in dictionary format.

    rename_topic(topic_id: int, new_topic_name: str) -> None:
        Renames the topic with the specified topic_id to the new_topic_name.

    delete_topic(topic_id: int) -> None:
        Deletes the topic with the specified topic_id.
    """

    @staticmethod
    async def create_topic(topic_id: int, topic_name: str) -> dict:
        """
        Creates a new topic with the specified topic_id and topic_name,
        and returns information about the created topic in dictionary format.

        Parameters
        ----------
        topic_id : int
            The ID of the topic to create.
        topic_name : str
            The name of the topic.

        Returns
        -------
        dict
            A dictionary containing all information about the created topic.

        Raises
        ------
        DoesNotExist
            If the topic with the given topic_id does not exist.
        """
        topic = await Topics.create(topic_id=topic_id, topic_name=topic_name)

        return {
            'id': topic.id,
            'topic_id': topic.topic_id,
            'topic_name': topic.topic_name
        }

    @staticmethod
    async def get_topic_info(topic_id: int) -> dict:
        """
        Retrieves information about the topic with
        the given topic_id in dictionary format.

        Parameters
        ----------
        topic_id : int
            The ID of the topic to retrieve information for.

        Returns
        -------
        dict
            A dictionary containing all information about the topic.

        Raises
        ------
        DoesNotExist
            If the topic with the given topic_id does not exist.
        """
        topic = await Topics.filter(topic_id=topic_id).first()
        if not topic:
            raise DoesNotExist(
                f"Topic with topic_id {topic_id} does not exist.")

        topic_info = {
            'id': topic.id,
            'topic_id': topic.topic_id,
            'topic_name': topic.topic_name
        }

        return topic_info

    @staticmethod
    async def rename_topic(topic_id: int, new_topic_name: str) -> None:
        """
        Renames the topic with the specified topic_id to the new_topic_name.

        Parameters
        ----------
        topic_id : int
            The ID of the topic to rename.
        new_topic_name : str
            The new name for the topic.

        Raises
        ------
        DoesNotExist
            If the topic with the given topic_id does not exist.
        """
        topic = await Topics.filter(topic_id=topic_id).first()
        if not topic:
            raise DoesNotExist(
                f"Topic with topic_id {topic_id} does not exist.")

        topic.topic_name = new_topic_name
        await topic.save()

    @staticmethod
    async def delete_topic(topic_id: int) -> None:
        """
        Deletes the topic with the specified topic_id.

        Parameters
        ----------
        topic_id : int
            The ID of the topic to delete.

        Raises
        ------
        DoesNotExist
            If the topic with the given topic_id does not exist.
        """
        topic = await Topics.filter(topic_id=topic_id).first()
        if not topic:
            raise DoesNotExist(
                f"Topic with topic_id {topic_id} does not exist.")

        await topic.delete()


class UsersHandler:
    """
    UsersHandler class provides methods to handle operations
    related to users in the database.

    Methods
    -------
    is_user_admin(telegram_id: int) -> bool:
        Checks if the user with the given telegram_id is an admin.

    get_user_info(user_id: int) -> dict:
        Retrieves all information about the user with the given user_id
        in a dictionary format.

    add_users(telegram_ids: list[int]) -> None:
        Adds a list of telegram_ids to the database, skipping existing users.

    delete_user(telegram_id: int) -> None:
        Deletes the user with the given telegram_id from the database.

    update_callsign(telegram_id: int, new_callsign: str) -> Users:
        Updates the callsign of the user with the given telegram_id.

    update_reserved(telegram_id: int) -> Users:
        Toggles the reserved status of the user with the given telegram_id.

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


class EventDetailsHandler:
    pass


class EventPollsHandler:
    pass
