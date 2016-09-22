# -*- coding: utf-8 -*-
"""Module: imgloader (programming exercise)

This program takes a plaintext file as an argument and downloads all images,
which are specified in the text file by image urls, storing them on the local hard disk.

Features:
    * The program can be used as a module or called directly via command line.
        
        Example use:
            * In order to call the program via command line, pass the input file as the one and only argument:

                $ python exercise.py urllist.txt

            * When used as a module, the image urls can be passed either
                * in form of a text file: call download_by_text_file(filename)
                * by a list of strings: call download_by_url_list(list)
				
    * Only files under a maximum file size of MAX_FILE_SIZE are downloaded
    * The downloaded file is checked for a valid image format and discarded if the test fails
"""

import sys, os
import imghdr
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# maximum allowed file size for single image download in bytes
MAX_FILE_SIZE = 10000000

def delete_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)

def download_by_url_list(web_url_list):
    """Downloads all images, which are specified by the url strings in the parameter <web_url_list>
    
    Args:
        web_url_list (list of str): containing image urls
    
    Returns:
        int: number of successfully downloaded images
    """
    number_of_downloads = 0
    print('Downloading files...')
    for web_url in web_url_list:
        print('...' + web_url + '...', end="")
        # extract filename and extension
        out_filename = web_url.split('/')[-1]
        out_fileext = out_filename.split('.')[-1]
        if out_filename == out_fileext:
            print('(Warning: No file extension detected)', end="")
        try:
            # request data
            web_req = Request(web_url)
            web_resp = urlopen(web_req)
            # check data
            #print(type(web_resp.headers['Content-Length']))
            web_data_size = int(web_resp.headers['Content-Length'] or 0)
            if web_data_size > MAX_FILE_SIZE:
                print('failed')
                print('Error: Requested data exceeds maximum data size of ' + str(MAX_FILE_SIZE) + ' bytes (skipping)')
                continue
            # fetch data
            out_file = open(out_filename,'wb')
            web_data = web_resp.read()
            # store data
            out_file.write(web_data)
            out_file.close()
            if not imghdr.what(out_filename):
                print('failed')
                print('Error: The specified url does not point to a valid image (skipping)')
                delete_file(out_filename)
                continue
        except ValueError as e:
            print('failed')
            print('Error: The given url is not valid')
            continue
        except HTTPError as e:
            print('failed')
            print('Error: The server could not fulfill the request (Error code: ' + str(e.code) + ')')
            continue
        except URLError as e:
            print('failed')
            print('Error: The server could not be reached (Reason: ' + str(e.reason) + ')')
            continue
        except (OSError, IOError) as e:
            print('failed')
            print('Error: Cannot open file for writing (' + out_filename + ')')
            continue
        else:
            number_of_downloads += 1
            print('done')
    print('completed (' + str(number_of_downloads) + '/' + str(len(web_url_list)) + ').')
    return number_of_downloads

def read_in_file(in_filename):
    """Returns a list of all lines of the file, specified by the parameter <in_filename>
    
    Args:
        in_filename (str): filename of the input file, containing all image urls

    Returns:
        list of str: hopefully containing valid image urls
    """
    print('Loading input file (' + in_filename + ')...', end="")
    try:
        in_file = open(in_filename, 'r')
    except (OSError, IOError) as e:
        print('failed')
        print('Error: Cannot open file for reading (' + in_filename + ')')
        return []
    else:
        print('succeeded')
    # extract lines without trailing line break
    web_url_list = [in_line.rstrip('\n') for in_line in in_file]
    return web_url_list
			
def download_by_text_file(in_filename):
    """Downloads all images specified in the text file, which is defined by the parameter <in_filename>
    
    Args:
        in_filename (str): filename of a valid plain text file containing image urls

    Returns:
        int: number of successfully downloaded images
    """
    web_url_list = read_in_file(in_filename)
    if web_url_list:
        return download_by_url_list(web_url_list)
    else:
        print('Nothing to do')
        return 0
	
def is_valid(argv):
    """Checks the command line parameters for the correct format
    
    Args:
	    argv (list of args): a list of command line parameters

	Returns:
        bool: true, if the command line parameters satisfy the expected form, false otherwise
    """
    # only one command line parameter is allowed
    return len(argv) == 2
	
def main(argv):
    """Main function if the program is called via command line
    
	Checks the number of command line arguments and calls download_by_text_file with argument No. 1
	
    Args:
	    argv (list of args): should contain one (extra) command line argument, which specifies the filename of the input text file containing image urls
    """
    if not is_valid(sys.argv):
        print('Correct usage: ' + sys.argv[0] + ' <inutfile>')
        sys.exit(2)
    in_filename = argv[1]
    download_by_text_file(in_filename)

# only auto-run the program, if it is started directly and not as a module, call download_by_text_file (or download_by_url_list) otherwise
if __name__ == "__main__":
    main(sys.argv[:])