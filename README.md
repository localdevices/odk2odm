# PyODKCentralClient

A utility to manage data from Open Data Kit's ODK Central aggregation server, particularly for use with [OpenDroneMap](opendronemap.org) (ODM).

ODK Central provides a Web interface to manage forms, submissions, and media (photos etc). However, when faced with hundreds of GB of media, the Web interface can be tricky. Specifically, if a lot of media is submittted to a single form, ODK Central's Web interface only provides methods to download a single file at a time, or _the entire set_ as a zipfile&mdash;the former is time-consuming, and the latter is prone to failed downloads.

To create a [3DStreetView](3dstreetview.org) digital twin, users routinely gather thousands of photographs per day. If multiple users are submitting to the same form, it almost immediately becomes difficult to access the media on the server.

PyODKCentralClient is intended to provide automated tools to access data on ODK Central servers and get them to ODM.

## Setup
If on Ubuntu, run ```sudo script/setup.sh``` and it'll likely set up a Python virtual environment, download and install the relevant dependencies in that venv, and exit with the exhortation to activate the virtual environment.

Otherwise get yourself a Python environment that contains ```requests``` and ```exifread```, and carry on.

## Usage
### Accessing data from ODK Central
You'll need your credentials (username, usually an email address) and password to the relevant ODK Central server. Having the URL of the server is also helpful.

From there, you can:
- Get a list of projects in the server
- Get a list of forms in a specific project
- Get a list of submissions to a specific form
- Get a list of attachment filenames in a specific submission
- Download any attachment by filename

These functions are all contained in the ```fetch.py``` module. The ```attachments.py``` utility uses the functions in ```fetch.py``` to download all of the attachments in all submissions to a given form from the command line, like so:

```
python3 attachments.py -url https://myodkcentral.org -u myusername@email.com -pw mypassword -p 3 -f my_form_v2-1-4 -od /home/myself/centraldata
```

Assuming your server is at myodkcentral.org, your username and password are correct, your project is number 3 on the server, the form you want the attachments from is called my_form_v2-1-4, there exists a directory you have write access to at ```/home/myself/centraldata```, you have an Internet connection, and [Mercury is in Capricorn while Neptune goes Station Retrograde in Pisces](https://www.theplanetstoday.com/astrology.html), this will download every single attachment in that form.



