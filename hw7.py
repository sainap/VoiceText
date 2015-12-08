import urllib, urllib2, webbrowser, json, operator

### Utility functions you may want to use
def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)


def safeGet(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print "The server couldn't fulfill the request." 
        print "Error code: ", e.code
    except urllib2.URLError, e:
        print "We failed to reach a server"
        print "Reason: ", e.reason
    return None

#### Main Assignment ##############

## Don't forget, you need to get your own api_key from Flickr, following the
#procedure in session 10 slides. Put it in the file flickr_key.py
# Then, UNCOMMENT the api_key line AND the params['api_key'] line in the function below.
import flickr_key
def flickrREST(baseurl = 'https://api.flickr.com/services/rest/',
    method = 'flickr.photos.search',
    api_key = flickr_key.key,
    format = 'json',
    params={},
    printurl = False
    ):
    params['method'] = method
    params['api_key'] = api_key
    params['format'] = format
    params['extras'] = 'url_o'
    if format == "json": params["nojsoncallback"]=True
    url = baseurl + "?" + urllib.urlencode(params)
    if printurl:
        print url
    else:
        return safeGet(url)

### This is where you should start filling in code...

## Building block 1 ###
# Define a function called get_photo_ids() which uses the flickr API to search
# for photos with a given tag, and return a list of photo IDs for the
# corresponding photos. Use a list comprehension to generate the list.
# Hints: Use flickrREST(). You may wish to use print & pretty() to inspect
#       the data returned by flickr to figure out what fields to extract. You
#       may find useful code to copy and edit in s10.py, but make sure you
#       understand what it's doing!
#
#       flickrREST() defaults to the flickr.photos.search method, documented
#       at https://www.flickr.com/services/api/flickr.photos.search.html
#       This method will work for building block 1, but see the documentation
#       for what parameters you might pass.
#
# Inputs:
#   tag: a tag to search for
#   n: the number of search results per page (default value should be 100)
# Returns: a list of (at most) n photo ids, or None if an error occured
def get_photo_ids(tag, n=5):
    idList = []
    photos = json.load(flickrREST(params={'tags': tag,'per_page':n}))
    for photo in photos['photos']['photo']:
        idList.append(photo['id'])
    return idList



def get_photo_url(tag):
    urls = {}
    photos = json.load(flickrREST(params={'tags': tag, 'extras': 'url_o', 'per_page': 520}))
    for photo in photos['photos']['photo']:
        if len(photo) > 11:
            print photo['url_o']
            if str(photo['url_o']).endswith('.gif'):
                urls[photo['title']] = photo['url_o']
    return urls


## Building block 2 ###
## Define a function called get_photo_info() which uses the flickr API to
# get information about a particular photo id.  The information should be
# returned as a python dictionary Hint: use flickrREST and the flickr API method
# flickr.photos.getInfo, documented at
# http://www.flickr.com/services/api/flickr.photos.getInfo.html
# Inputs:
#   photo_id: the id of the photo you to get information about
# Returns: a dictionary with photo info, or None if an error occurred
def get_photo_info(identifier):
    return json.load(flickrREST(method = 'flickr.photos.getInfo', params={'photo_id': identifier}))['photo']

## Building block 3 ###
## Define a class called Photo to represent flickr photos
# It should have at least three methods:
# (a) a constructor (init__())
# (b) a string representation (__str__())
# (c) a function that opens the photo in your web browser (open_url())

## (a) __init__():
# The constructor (remember, the __init__() method is called the constructor)
# should take a dictionary representing photo info  and initialize
# four instance variables:
#  -title: the title of the photo (Use "_content"!)
#  -author: the user that posted the photo (use username!)
#  -userid: the user nsid (####@N##, for example)
#  -tags: a list of tags (strings) associated with the photo (Use "_content"!)
#  -commentcount: a count with the number of comments on the photo
#  -num_views: the number of times the photo was viewed
#  -url: the location of the photo on flickr
# Your constructor should use a list comprehension to create the tags list.
# Hint: You may wish to use print and pretty() to determine which fields in
#       the photo info dictionary to extract.
#       If a field needs to be converted to a number from a different type
#       (i.e. num_views), be sure to do that in the body of the constructor.

class Photo:
    def __init__(self, info):
        self.title = info['title']['_content']
        self.author = info['owner']['username']
        self.userid = info['owner']['nsid']

        self.tags = []
        for x in info['tags']['tag']:
            self.tags.append(x['_content'])

        self.commentcount = int(info['comments']['_content'])
        self.num_views = int(info['views'])
        self.url = info['urls']['url'][0]['_content']

## (b) __str__()
# The __str__() method should return a string with the following format:
#   ~~~ <TITLE> ~~~
#   author: <AUTHOR>
#   number of tags: <NUMBER OF TAGS IN TAGS INSTANCE VARIABLE>
#   views <NUMBER OF VIEWS>
#   comments: <NUMBER OF COMMENTS>
# Look at HW 5 if you need reminders about doing this.
# Tip: use .encode('utf-8') on the title and author in case either
#          string contains unicode characters (strings that look like
#          u'something')

    def __str__(self):
        string = '~~~ ' + self.title.encode('utf-8') + ' ~~~\n'
        string += 'author: ' + self.author.encode('utf-8') + '\n'
        string += 'number of tags: ' + str(len(self.tags)) + '\n'
        string += 'views ' + str(self.num_views) + '\n'
        string += 'comments: ' + str(self.commentcount) + '\n'
        return string

    def open_url(self):
        webbrowser.open_new(self.url)

## (c) open_url()
# The open_url() method should take your web browser to the location
# specified by the url instance variable.
# The variable called url has a string value stored in it, a url, or address.
# The open_url method of this class shoud use that url: it should open
#     that URL in a web browser.
    def open_url(self):
        webbrowser.open_new(self.url)



if __name__ == '__main__':
    ### Testing your building blocks
    print '\n\nTesting your building blocks\n------------'
    # test get_photo_ids() with the following line of code, which will give
    # note the ids you get may be different than what's in the sample screenshot.
    # print get_photo_ids('hamster', n=4)

    # Test get_photo_info() with the following two lines of code:
    pd = get_photo_info(5140736446)
    print pd

    # Test your Photo class with the following lines of code: Check the format
    # of your output against sample output in the PDF file, and make adjustments
    # to your __init__ and __str__ methods as needed
    po = Photo(pd)
    print po
    print po.tags
    po.open_url()


    ### Part 1 #########
    # Use your get_photo_ids function to get a list of 100 photo ids with a tag of your choosing.
    # Convert the list of ids into a list of Photo objects using a list comprehension
    # Pro tip: You may want to start out with the first 10 or 20 photos while
    #          testing. It takes a while to run.
    # Note: nothing gets printed out in this part. But you might want to do some
    # printing to check if it's working
    cuties =  get_photo_ids('proud', 100)

    
    images = []
    for cute in cuties:
        images.append(Photo(get_photo_info(cute)))

    ### Part 2 #########
    # (a) Order the photo objects by number of views. Print the 5 most viewed photos
    # and open the top one in your web browser using open_url()
    print "\nTop Five Photos by Views"
    print "------------"

    def printSorted(view):
        sortedByView = sorted(images, key=view, reverse=True)
        for i in range(0, 5):
            print sortedByView[i]
            if (i == 0):
                sortedByView[i].open_url()
        return sortedByView


    def getView(custom):
        return custom.num_views

    printSorted(getView)



    # (b) Order the photo objects by number of tags. Print the 5 most tagged photos
    # and open the top one in your web browser using open_url()
    print "\nTop Five Photos by Number of Tags"
    print "------------"
    def getTag(custom):
        return len(custom.tags)

    printSorted(getTag)
    
    # (c) Order the photo objects by number of tags. Print the 5 most commented photos
    # and open the top one in your web browser using open_url()
    # NOTE: it is completely possible that you will have no photos with comments in your data set.
    print "\nTop Five Photos by Number of Comments"
    print "------------"
    def getComment(custom):
        return custom.commentcount

    printSorted(getComment)

    # Based on the photos you get, which do you think is a better way to find
    # good photos, the ones with the most views or the most tags?
    # the photos with most views
    print "------------"

    ### Part 3 #########
    # Compute the total number of views received by each author in the photo
    # object list.  Then, print out the username of the author along with
    # the total number of views their photos had received, for the top five
    # users, ranked in order of number of views, in the following format:
    # (1) Johnny 5: 1221
    # (2) Aravind: 134
    # (3) Sid: 120
    # (4) Korn: 113
    # (5) Stephanie: 108
    # (6) Cole: 104
    # (7) Ben: 98
    # (8) Tsuki: 54
    # (9) Joanna: 12
    # (10) Sean: 1
    print "\nTop ten authors by number of views"
    print "------------"
    # authors is a dictionary of authors and the views they have for their images
    authors = {}
    for image in images:
        author = image.author
        if author in authors:
            authors[author] += int(image.num_views)
        else:
            authors[author] = int(image.num_views)


    # prints authors in reverse order by the value
    for i, author in enumerate(sorted(authors, key=authors.get, reverse=True)):
        if i > 9:
            break
        print '(' + str(i+1) + ') ' +  author + ': ' + str(authors[author])









