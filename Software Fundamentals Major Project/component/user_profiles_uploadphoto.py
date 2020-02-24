# stub function for user_profiles_uploadphoto
from component.data import get_data
from component.general import decode_token, check_http_status, ValueError, id_to_user, authorise_token, invalid_dimension
from PIL import Image
from urllib.request import urlretrieve

'''
Given an image url, crops the image within bounds (x_start, y_start) and (x_end, y_end). 
Position (0,0) is the top left.

ValueErrors when:
1) img_url returns an HTTP status other than 200.
2) x_start, y_start, x_end, y_end aren't all within the dimensions of the image at the URL.
3) Image uploaded is not a JPG

AccessError when:
1) token is invalid (done in the decorator)
returns {}
'''

@authorise_token
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    if not check_http_status(img_url):
        raise ValueError(description="URL does not upload jpeg file or URL is invalid.")
    else:
        filename = "./imgurl/" + img_url.split("/")[-1] 
        urlretrieve(img_url, filename)
        imageObj = Image.open(filename)
        #   actual image dimensions
        #   width = x2
        #   height = y2        
        width, height = imageObj.size

        # check the dimensions are within range
        if width < x_end or height < y_end or invalid_dimension(x_start, y_start, x_end, y_end):
            raise ValueError(description="x_start, y_start, x_end, y_end aren't all within the dimensions of the image\n")
        else:
            box = (x_start, y_start, x_end, y_end)
            cropped = imageObj.crop(box)
            # storing the file locally
            cropped.save(filename)

            return { 'filename': filename, "u_id": decode_token(token) }

# "https://i.kym-cdn.com/entries/icons/original/000/029/000/imbaby.jpg"
# http://www.myconfinedspace.com/wp-content/uploads/tdomf/143612/pikachu.jpg
# https://i.redd.it/gf6a5wyzfvn21.jpg
