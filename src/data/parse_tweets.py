# -- coding: utf-8 --
# adapted from https://raw.githubusercontent.com/DocNow/twarc/master/twarc/json2csv.py


from typing import Dict, Union
from src.utils import recursive_get


def text(t: Dict) -> str:
    """
    Get text of tweet
    """
    return t.get('full_text') or t.get('extended_tweet',
                                       {}).get('full_text') or t['text']


def coordinates(t: Dict) -> Union[str, None]:
    """
    Get location coordinates in the form [longitude, latitude] (if available)
    """
    try:
        return '%f %f' % tuple(recursive_get(t, 'coordinates', 'coordinates'))
    except AttributeError:
        return None


def place(t: Dict) -> Union[str, None]:
    """
    Full human-readable representation of the place’s name (if available)
    """
    try:
        return recursive_get(t, 'place', 'full_name')
    except AttributeError:
        return None


def hashtags(t: Dict) -> str:
    """
    Get hashtags found in body of tweet, minus # sign
    """
    return ' '.join([h['text'] for h in t['entities']['hashtags']])


# noinspection PyTypeChecker
def media(t: Dict) -> Union[str, None]:
    """
    An expanded version of display_url. Links to the media display page
    """
    m = recursive_get(t, 'entities', 'media')
    if m:
        return ' '.join([h['expanded_url'] for h in m])
    else:
        m = recursive_get(t, 'entities', 'media')
        if m:
            return ' '.join([h['expanded_url'] for h in t])
        else:
            return None


def urls(t: Dict) -> str:
    """
    URLs included in the text of a Tweet.
    """
    return ' '.join([h['expanded_url'] or '' for h in t['entities']['urls']])


def retweet_id(t: Dict) -> Union[str, None]:
    """
    integer value Tweet ID of the retweeted or quoted Tweet
    """
    try:
        return recursive_get(t, 'retweeted_status', 'id_str')
    except AttributeError:
        pass
    try:
        return recursive_get(t, 'quoted_status', 'id_str')
    except AttributeError:
        return None


def retweet_screen_name(t: Dict) -> Union[str, None]:
    """
    Name of Original Tweeter
    """
    try:
        return recursive_get(t, 'retweeted_status', 'user', 'screen_name')
    except AttributeError:
        pass

    try:
        return recursive_get(t, 'quoted_status', 'user', 'screen_name')
    except AttributeError:
        return None


def retweet_user_id(t: Dict) -> Union[str, None]:
    """
    Integer value Tweet ID of the Original Tweeter
    """
    try:
        return recursive_get(t, 'retweeted_status', 'user', 'id_str')
    except AttributeError:
        pass

    try:
        return recursive_get(t, 'quoted_status', 'user', 'id_str')
    except AttributeError:
        return None


def tweet_url(t: Dict) -> str:
    return "https://twitter.com/%s/status/%s" % (t['user']['screen_name'],
                                                 t['id_str'])


def user_urls(t: Dict) -> Union[str, None]:
    """
    url of the Tweeter
    """
    try:
        u = recursive_get(t, 'user', 'entities', 'url', 'urls')
        # noinspection PyTypeChecker,PyTypeChecker
        return " ".join([url[
            'expanded_url'] for url in u if url['expanded_url']])
    except AttributeError:
        return None


def tweet_type(t: Dict) -> str:
    """
    Type of tweet (Reply, retweet, quote, original
    """
    if t.get('in_reply_to_status_id'):
        return 'reply'
    if 'retweeted_status' in t:
        return 'retweet'
    if 'quoted_status' in t:
        return 'quote'
    return 'original'
