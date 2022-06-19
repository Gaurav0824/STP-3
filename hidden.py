# Keep this file separate

# https://apps.twitter.com/
# Create new App and get the four strings
import os
def oauth():
    """ Returns Authentication keys in form of dictionary """

    """  Keys & tokens let Twitter know you who you are.
        Specifically, keys are unique identifiers that authenticate your App's request, while tokens are a type of authorization for an App to gain specific access to data. """

    return {
        "consumer_key":os.environ.get("consumer_key"),
        "consumer_secret":os.environ.get("consumer_secret"),
        "token_key":os.environ.get("token_key"),
        "token_secret":os.environ.get("token_secret")
    }

