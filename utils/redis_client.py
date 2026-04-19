import redis
from core.config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

# Token blacklist using Redis
def blacklist_token(token: str, expire_seconds: int):
    redis_client.setex(token, expire_seconds, "blacklisted")

def is_token_blacklisted(token: str):
    return redis_client.exists(token) == 1
