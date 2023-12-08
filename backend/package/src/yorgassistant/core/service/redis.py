from ...utils.singleton import Singleton
from ..common_models import UserProperties, RedisKeyType
import redis
from pathlib import Path
import json
from enum import Enum


@Singleton
class Redis:
    """
    A class for interacting with Redis database.
    """

    def __init__(self):
        """
        Initialize a Redis client instance.
        """
        self.redis = redis.Redis(host="redis", port=6379, decode_responses=True)

    def get(self, key: str) -> str:
        """
        Get the value of a key from Redis.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            str: The value of the key.
        """
        return self.redis.get(key)

    def set(self, key: str, value: str, save: bool = True) -> str:
        """
        Set the value of a key in Redis.

        Args:
            key (str): The key to set the value for.
            value (str): The value to set for the key.
            save (bool, optional): Whether to save the changes to disk, by default True.

        Returns:
            Optional[str]: If `save` is True, returns the Redis response to the SAVE command.
        """
        self.redis.set(key, value)
        if save:
            return self.redis.save()

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in Redis.

        Args:
            key (str): The key to check for existence.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        return self.redis.exists(key)

    def save(self) -> str:
        """
        Export all key-value pairs to an RDB file.

        Returns:
            Optional[str]: The Redis response to the SAVE command.
        """
        return self.redis.save()

    def safe_get(self, key: str) -> str:
        """
        Get the value of a key from Redis and json loads the value.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            str: The value of the key.
        """
        return json.loads(self.redis.get(key))

    def safe_set(self, key: str, value, save: bool = True):
        """
        Set the value of a key in Redis and dumps into json before setting.

        Args:
            key (str): The key to set the value for.
            value (str): The value to set for the key.
            save (bool, optional): Whether to save the changes to disk, by default True.

        Returns:
            Optional[str]: If `save` is True, returns the Redis response to the SAVE command.
        """
        self.redis.set(key, json.dumps(value))
        if save:
            return self.redis.save()

    def print_all(self):
        """
        Print all keys and their corresponding values in Redis.
        """
        for key in self.redis.keys():
            print(f"{key}: {self.redis.get(key)}")

    def exists_with_key_type(self, user_properties: UserProperties, type: RedisKeyType):
        """
        Check if a key exists in Redis with a specific key type.

        Args:
            user_properties (UserProperties): The user properties.
            type (RedisKeyType): The Redis key type.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        return self.redis.exists(user_properties.generate_redis_key_with_type(type))

    def safe_get_with_key_type(
        self, user_properties: UserProperties, type: RedisKeyType
    ):
        """
        Get the value of a key from Redis with a specific key type and json loads the value.

        Args:
            user_properties (UserProperties): The user properties.
            type (RedisKeyType): The Redis key type.

        Returns:
            str: The value of the key.
        """
        return json.loads(
            self.redis.get(user_properties.generate_redis_key_with_type(type))
        )

    def safe_set_with_key_type(
        self,
        user_properties: UserProperties,
        type: RedisKeyType,
        value,
        save: bool = True,
    ):
        """
        Set the value of a key in Redis with a specific key type and dumps into json before setting.

        Args:
            user_properties (UserProperties): The user properties.
            type (RedisKeyType): The Redis key type.
            value (str): The value to set for the key.
            save (bool, optional): Whether to save the changes to disk, by default True.

        Returns:
            Optional[str]: If `save` is True, returns the Redis response to the SAVE command.
        """
        self.redis.set(
            user_properties.generate_redis_key_with_type(type), json.dumps(value)
        )
        if save:
            return self.redis.save()
