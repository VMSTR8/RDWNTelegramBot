from datetime import datetime

from typing import Optional, Union

from tortoise.exceptions import (
    IntegrityError,
    DoesNotExist
)

from database.telegram_bot.models import (
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
                f'Topic with topic_id {topic_id} does not exist.')

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
                f'Topic with topic_id {topic_id} does not exist.')

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
                f'Topic with topic_id {topic_id} does not exist.')

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
    """
    EventDetailsHandler class provides methods to handle operations
    related to event details in the database.

    Methods
    -------
    create_event_details(event_data: dict) -> dict:
        Creates a new event details record with the provided data
        and returns information about the created event in dictionary format.

    get_event_details(event_id: int) -> dict:
        Retrieves all information about the event
        with the given event_id in dictionary format.

    update_event_name(event_id: int, new_event_name: str) -> dict:
        Updates the event_name for the event with the specified event_id
        and returns updated information about the event in dictionary format.

    update_event_link(event_id: int, new_event_link: str) -> dict:
        Updates the event_link for the event with the specified event_id
        and returns updated information about the event in dictionary format.

    update_organizer_rules(event_id: int, new_organizer_rules: str) -> dict:
        Updates the organizer_rules for the event with the specified event_id
        and returns updated information about the event in dictionary format.

    update_latitude(event_id: int, new_latitude: float) -> dict:
        Updates the latitude for the event with the specified event_id
        and returns updated information about the event in dictionary format.

    update_longitude(event_id: int, new_longitude: float) -> dict:
        Updates the longitude for the event with the specified event_id
        and returns updated information about the event in dictionary format.

    update_price(event_id: int, new_price: int) -> dict:
        Updates the price for the event with the specified event_id and returns
        updated information about the event in dictionary format.

    update_expire_date(event_id: int, new_expire_date: datetime) -> dict:
        Updates the expire_date for the event with the specified event_id
        and returns updated information about the event in dictionary format.

    delete_event(event_id: int) -> None:
        Deletes the event with the specified event_id from the database.
    """

    @staticmethod
    async def _get_event_info(event) -> dict:
        """
        Helper method to extract and return event information as a dictionary.

        Parameters
        ----------
        event : EventDetails
            The EventDetails instance.

        Returns
        -------
        dict
            A dictionary containing information about the event.
        """
        return {
            'id': event.id,
            'event_name': event.event_name,
            'event_link': event.event_link,
            'organizer_rules': event.organizer_rules,
            'latitude': event.latitude,
            'longitude': event.longitude,
            'price': event.price,
            'expire_date': event.expire_date,
            'topic_id': event.topic.id,
            'topic_name': event.topic.topic_name
        }

    @staticmethod
    async def create_event_details(event_data: dict) -> dict:
        """
        Creates a new event details record with the provided data
        and returns information about the created event in dictionary format.

        Parameters
        ----------
        event_data : dict
            A dictionary containing the following keys:
            - event_name (str): The name of the event.
            - event_link (str, optional): The link associated
            with the event (default is None).
            - organizer_rules (str, optional): Organizer rules
            for the event (default is None).
            - latitude (float): Latitude coordinate of the event location.
            - longitude (float): Longitude coordinate of the event location.
            - price (int): The price of the event.
            - expire_date (str): The expiration date of the event.
            - topic (int): The topic_id of
            the associated topic from the Topics table.

        Returns
        -------
        dict
            A dictionary containing all information about the created event.

        Raises
        ------
        DoesNotExist
            If the topic with the given topic_id does not exist.
        """
        try:
            topic_id = event_data.pop('topic', None)
            topic = await Topics.get(topic_id=topic_id)
        except DoesNotExist:
            raise DoesNotExist(
                f'Topic with topic_id {topic_id} does not exist.')

        event = await EventDetails.create(
            topic=topic,
            event_name=event_data['event_name'],
            event_link=event_data.get('event_link'),
            organizer_rules=event_data.get('organizer_rules'),
            latitude=event_data['latitude'],
            longitude=event_data['longitude'],
            price=event_data['price'],
            expire_date=event_data['expire_date']
        )

        return await EventDetailsHandler._get_event_info(event)

    @staticmethod
    async def get_event_details(event_id: int) -> dict:
        """
        Retrieves all information about the event with
        the given event_id in dictionary format.

        Parameters
        ----------
        event_id : int
            The ID of the event to retrieve information for.

        Returns
        -------
        dict
            A dictionary containing all information about the event.

        Raises
        ------
        DoesNotExist
            If the event with the given event_id does not exist.
        """
        try:
            event = await EventDetails.get(id=event_id)
        except DoesNotExist:
            raise DoesNotExist(f'Event with id {event_id} does not exist.')

        return await EventDetailsHandler._get_event_info(event)

    @staticmethod
    async def update_event_name(event_id: int, new_event_name: str) -> dict:
        """
        Updates the event_name for the event with the specified event_id
        and returns updated information about the event in dictionary format.

        Parameters
        ----------
        event_id : int
            The ID of the event to update.
        new_event_name : str
            The new name for the event.

        Returns
        -------
        dict
            A dictionary containing all updated information about the event.

        Raises
        ------
        DoesNotExist
            If the event with the given event_id does not exist.
        """
        try:
            event = await EventDetails.get(id=event_id)
        except DoesNotExist:
            raise DoesNotExist('Event with id {event_id} does not exist.')

        event.event_name = new_event_name
        await event.save()

        return await EventDetailsHandler._get_event_info(event)

    @staticmethod
    async def update_event_link(event_id: int, new_event_link: str) -> dict:
        """
        Updates the event_link for the event with the specified event_id
        and returns updated information about the event in dictionary format.

        Parameters
        ----------
        event_id : int
            The ID of the event to update.
        new_event_link : str
            The new link for the event.

        Returns
        -------
        dict
            A dictionary containing all updated information about the event.

        Raises
        ------
        DoesNotExist
            If the event with the given event_id does not exist.
        """
        try:
            event = await EventDetails.get(id=event_id)
        except DoesNotExist:
            raise DoesNotExist(f'Event with id {event_id} does not exist.')

        event.event_link = new_event_link
        await event.save()

        return await EventDetailsHandler._get_event_info(event)

    @staticmethod
    async def update_organizer_rules(
            event_id: int, new_organizer_rules: str) -> dict:
        """
        Updates the organizer_rules for the event with the specified event_id
        and returns updated information about the event in dictionary format.

        Parameters
        ----------
        event_id : int
            The ID of the event to update.
        new_organizer_rules : str
            The new organizer rules for the event.

        Returns
        -------
        dict
            A dictionary containing all updated information about the event.

        Raises
        ------
        DoesNotExist
            If the event with the given event_id does not exist.
        """
        try:
            event = await EventDetails.get(id=event_id)
        except DoesNotExist:
            raise DoesNotExist(f'Event with id {event_id} does not exist.')

        event.organizer_rules = new_organizer_rules
        await event.save()

        return await EventDetailsHandler._get_event_info(event)

    @staticmethod
    async def update_latitude(event_id: int, new_latitude: float) -> dict:
        """
        Updates the latitude for the event with the specified event_id
        and returns updated information about the event in dictionary format.

        Parameters
        ----------
        event_id : int
            The ID of the event to update.
        new_latitude : float
            The new latitude coordinate for the event.

        Returns
        -------
        dict
            A dictionary containing all updated information about the event.

        Raises
        ------
        DoesNotExist
            If the event with the given event_id does not exist.
        """
        try:
            event = await EventDetails.get(id=event_id)
        except DoesNotExist:
            raise DoesNotExist(f'Event with id {event_id} does not exist.')

        event.latitude = new_latitude
        await event.save()

        return await EventDetailsHandler._get_event_info(event)

    @staticmethod
    async def update_longitude(event_id: int, new_longitude: float) -> dict:
        """
        Updates the longitude for the event with the specified event_id
        and returns updated information about the event in dictionary format.

        Parameters
        ----------
        event_id : int
            The ID of the event to update.
        new_longitude : float
            The new longitude coordinate for the event.

        Returns
        -------
        dict
            A dictionary containing all updated information about the event.

        Raises
        ------
        DoesNotExist
            If the event with the given event_id does not exist.
        """
        try:
            event = await EventDetails.get(id=event_id)
        except DoesNotExist:
            raise DoesNotExist(f'Event with id {event_id} does not exist.')

        event.longitude = new_longitude
        await event.save()

        return await EventDetailsHandler._get_event_info(event)

    @staticmethod
    async def update_price(event_id: int, new_price: int) -> dict:
        """
        Updates the price for the event with the specified event_id and returns
        updated information about the event in dictionary format.

        Parameters
        ----------
        event_id : int
            The ID of the event to update.
        new_price : int
            The new price for the event.

        Returns
        -------
        dict
            A dictionary containing all updated information about the event.

        Raises
        ------
        DoesNotExist
            If the event with the given event_id does not exist.
        """
        try:
            event = await EventDetails.get(id=event_id)
        except DoesNotExist:
            raise DoesNotExist(f'Event with id {event_id} does not exist.')

        event.price = new_price
        await event.save()

        return await EventDetailsHandler._get_event_info(event)

    @staticmethod
    async def update_expire_date(
            event_id: int, new_expire_date: datetime) -> dict:
        """
        Updates the expire_date for the event with the specified event_id
        and returns updated information about the event in dictionary format.

        Parameters
        ----------
        event_id : int
            The ID of the event to update.
        new_expire_date : datetime
            The new expire date for the event.

        Returns
        -------
        dict
            A dictionary containing all updated information about the event.

        Raises
        ------
        DoesNotExist
            If the event with the given event_id does not exist.
        """
        try:
            event = await EventDetails.get(id=event_id)
        except DoesNotExist:
            raise DoesNotExist(f'Event with id {event_id} does not exist.')

        event.expire_date = new_expire_date
        await event.save()

        return await EventDetailsHandler._get_event_info(event)

    @staticmethod
    async def delete_event(event_id: int) -> None:
        """
        Deletes the event with the specified event_id from the database.

        Parameters
        ----------
        event_id : int
            The ID of the event to delete.

        Raises
        ------
        DoesNotExist
            If the event with the given event_id does not exist.
        """
        try:
            event = await EventDetails.get(id=event_id)
        except DoesNotExist:
            raise DoesNotExist(f'Event with id {event_id} does not exist.')

        await event.delete()


class EventPollsHandler:
    """
    EventPollsHandler class provides methods to handle
    operations related to event polls in the database.

    Methods
    -------
    create_poll_results(poll_data: dict) -> dict:
        Creates a new poll record with the provided data
        and returns information about the created poll in dictionary format.

    get_poll_results_by_user_id(user_id: int) -> dict:
        Retrieves poll data for the given user_id.
        Returns None if the user has not taken the poll.

    delete_poll_results(poll_id: int) -> None:
        Deletes the poll with the specified poll_id from the database.
    """

    @staticmethod
    async def _get_poll_results_info(poll) -> dict:
        """
        Helper method to extract and return poll results
        information as a dictionary.

        Parameters
        ----------
        poll : EventPolls
            The EventPolls instance.

        Returns
        -------
        dict
            A dictionary containing information about the poll results.
        """
        return {
            'id': poll.id,
            'user_id': poll.user.id,
            'event_id': poll.event.id,
            'visitation': poll.visitation,
            'reason': poll.reason,
            'car': poll.car,
            'hitchhike': poll.hitchhike,
            'start_location': poll.start_location
        }

    @staticmethod
    async def create_poll_results(poll_data: dict) -> dict:
        """
        Creates a new poll record with the provided data
        and returns information about the created poll results
        in dictionary format.

        Parameters
        ----------
        poll_data : dict
            A dictionary containing poll details:
            - user_id (int): The user id of the poll
            - event_id (int): The event id of the poll
            - visitation (bool): The event visitation status
            - reason (str, optional): Why user can not visit the event
            - car (bool): Availability of auto
            - hitchhike (bool, optional): Being able to give someone a ride
            - start_location (str): Start location of the user

        Returns
        -------
        dict
            A dictionary containing all information
            about the created poll results.

        Raises
        ------
        DoesNotExist
            If the user or event with the given IDs does not exist.
        """
        try:
            user = await Users.get(id=poll_data['user_id'])
        except DoesNotExist:
            raise DoesNotExist(
                f"User with id {poll_data['user_id']} does not exist.")

        try:
            event = await EventDetails.get(id=poll_data['event_id'])
        except DoesNotExist:
            raise DoesNotExist(
                f"Event with id {poll_data['event_id']} does not exist.")

        poll = await EventPolls.create(
            user=user,
            event=event,
            visitation=poll_data['visitation'],
            reason=poll_data.get('reason'),
            car=poll_data['car'],
            hitchhike=poll_data.get('hitchhike'),
            start_location=poll_data['start_location']
        )

        return await EventPollsHandler._get_poll_results_info(poll)

    @staticmethod
    async def get_poll_results_by_user_id(
            user_id: int) -> Optional[Union[dict, None]]:
        """
        Retrieves poll results data for the given user_id.
        Returns None if the user has not taken the poll.

        Parameters
        ----------
        user_id : int
            The ID of the user whose poll data is to be retrieved.

        Returns
        -------
        dict or None
            A dictionary containing poll results information if
            the user has taken the poll, otherwise None.

        Raises
        ------
        DoesNotExist
            If the user with the given user_id does not exist.
        """
        try:
            user = await Users.get(id=user_id)
        except DoesNotExist:
            raise DoesNotExist(f'User with id {user_id} does not exist.')

        try:
            poll = await EventPolls.get(user=user)
        except DoesNotExist:
            return None

        return await EventPollsHandler._get_poll_results_info(poll)

    @staticmethod
    async def delete_poll_results(poll_id: int) -> None:
        """
        Deletes the poll results with the specified
        poll_id from the database.

        Parameters
        ----------
        poll_id : int
            The ID of the poll results to delete.

        Raises
        ------
        DoesNotExist
            If the poll results with the given poll_id does not exist.
        """
        try:
            poll = await EventPolls.get(id=poll_id)
        except DoesNotExist:
            raise DoesNotExist(f'Poll with id {poll_id} does not exist.')

        await poll.delete()
