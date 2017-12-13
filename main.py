# -*- coding: utf-8 -*-
# Module: default
# Author: Roman V. M.
# Created on: 28.11.2014
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
import sys
from urllib import urlencode
from urllib2 import urlopen
from urllib2 import Request
from json import load
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin
import re
import urlresolver

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

VIDEOS = {}
VIDEOS['Bangla'] = []
VIDEOS['Hindi'] = []

def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def get_categories():
    """
    Get the list of video categories.

    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or server.

    .. note:: Consider using `generator functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :return: The list of video categories
    :rtype: list
    """
    return VIDEOS.iterkeys()

def resolve_url(url):
    duration=3500   #in milliseconds
    message = "Cannot Play URL"
    stream_url = urlresolver.HostedMediaFile(url=url).resolve()
    # If urlresolver returns false then the video url was not resolved.
    if not stream_url:
        dialog = xbmcgui.Dialog()
        dialog.notification("URL Resolver Error", message, xbmcgui.NOTIFICATION_INFO, duration)
        return False
    else:        
        return stream_url

def get_links():
    VIDEOS['Bangla'].append( { 'name': 'Maasranga TV', 'video': 'http://103.9.114.165:1935/tvprogram/MAASRANGA-TV/playlist.m3u8', 'genre': 'Bangla', 'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/04/crab-screenshot.jpg' } )

    ntvutube = 'https://www.youtube.com/watch?v=c2DqheGGwMI'
    ntvstream = resolve_url(ntvutube)
    VIDEOS['Bangla'].append( { 'name': 'NTV Tube', 'video': ntvstream, 'genre': 'Bangla', 'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/04/crab-screenshot.jpg' } )

    boishakhijago = 'http://www.jagobd.com/boishakhitv'
    boishakhistream = urlresolver.resolve(boishakhijago) 
    VIDEOS['Bangla'].append( { 'name': 'Boishakhi Jago', 'video': boishakhistream, 'genre': 'Bangla', 'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/04/crab-screenshot.jpg' } )

    url = 'http://app.jagobd.com/jagobd_app/index10.php'

    post_fields = {'tag': 'get_all_channel_free'}
    params = urlencode(post_fields)
    headers = {'jbd-token': '8388e6b188295130aa432ae250e3e3bb'}

    req = Request(url, params, headers)
    response = urlopen(req)

    x = load(response)
    churl = 'news24local.stream'
    for channel in x['channel'] :
        cname = channel["name"].split("|")[0]
        churl = channel["stream_url"]
        if cname.startswith('Boishakhi'):
            churl = re.sub('\d+.\d+.\d+.\d+:\d+','us.jagobd.com:1937',churl)
        VIDEOS['Bangla'].append( { 'name': cname, 'video': churl, 'genre': 'Bangla', 'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/04/crab-screenshot.jpg' } )
    
    churl = re.sub('[a-zA-Z0-9\-]+.stream','ekusheytv-8-org.stream',churl)
    VIDEOS['Bangla'].append( { 'name': 'Ekushaey TV', 'video': churl, 'genre': 'Bangla', 'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/04/crab-screenshot.jpg' } )

def get_links_from_app():
    url = 'http://mrrainp.info/tvsworld/api.php?search='
    req = Request(url)
    response = urlopen(req)
    x = load(response)
    for channel in x['LIVETV'] :
        if channel['cat_id'] == '104':
            VIDEOS['Bangla'].append( { 'name': channel['channel_title'], 'video': channel['channel_url'], 'genre': 'Bangla', 'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/04/crab-screenshot.jpg' } )
        if channel['cat_id'] == '99':
            VIDEOS['Hindi'].append( { 'name': channel['channel_title'], 'video': channel['channel_url'], 'genre': 'Hindi', 'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/04/crab-screenshot.jpg' } )

def get_videos(category):
    """
    Get the list of videofiles/streams.

    Here you can insert some parsing code that retrieves
    the list of video streams in the given category from some site or server.

    .. note:: Consider using `generators functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :param category: Category name
    :type category: str
    :return: the list of videos in the category
    :rtype: list
    """
    return VIDEOS[category]


def list_categories():
    """
    Create the list of video categories in the Kodi interface.
    """
    # Get video categories
    categories = get_categories()
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category)
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': VIDEOS[category][0]['thumb'],
                          'icon': VIDEOS[category][0]['thumb'],
                          'fanart': VIDEOS[category][0]['thumb']})
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        list_item.setInfo('video', {'title': category, 'genre': category})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='listing', category=category)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def list_videos(category):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: Category name
    :type category: str
    """
    # Get the list of videos in the category.
    videos = get_videos(category)
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['name'])
        # Set additional info for the list item.
        list_item.setInfo('video', {'title': video['name'], 'genre': video['genre']})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/vids/crab.mp4
        url = get_url(action='play', video=video['video'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    #get_links()
    get_links_from_app()
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos(params['category'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
