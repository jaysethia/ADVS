Automated Document Verification System
Setup Instructions:

1. Server Side Installation

1.1 Minimum System Requirements
Hardware
● RAM - 4GB DDR3
● Processor - Intel based
● Active Internet Connection
Software
● OS - Ubuntu 14.04 or higher
● Python v2.7
Prerequisites
1. Server should have Apache Installed, along with working config of PHP
2. The Python and the PHP files should be kept in the same directory.

1.2 Steps to Setup environment
1. Update Ubuntu:
sudo apt-get update
2. Install PIP for installing python packages:
sudo apt-get install python-pip
3. Install Tesseract-OCR:
sudo apt-get install tesseract-ocr
4. Install Tesseract-OCR languages:
sudo apt-get install tesseract-ocr-hin
5. Install Python Imaging Library:
sudo pip install pillow
6. Install MySQL:
sudo apt-get install python-dev libmysqlclient-dev
sudo pip install MySQL-python

2. Running Android App
2.1 Minimum System Requirements
Hardware
●	RAM - 2GB
●	Processor - Snapdragon based
●	Active Internet Connection
Software
●	OS - Android Lollipop 5.0 or higher
2.2 Steps
1.	Install the APK file, "ADVSF.apk", on the Android phone.
2.	Before running the application, go to Settings > Apps > ADVSF > Permissions, and turn on "Storage" permission.
3.	Active internet connection is required
4.	Run the application.

3. Android SDK Environment Setup
3.1 Minimum System Requirements
Hardware
●	RAM - 4GB DDR3
●	Processor - Intel based
●	Active Internet Connection
Software
●	OS - Windows 10
3.2 Steps
1.	Add the dependencies in build.gradle (module:app)
compile 'com.google.android.gms:play-services:7.8+'
compile 'com.android.volley:volley:1.0.'
2.	Add the required permission to Manifest
	<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.INTERNET" />

4. Troubleshooting

SERVER:
●	Unable to install PIP
Alternatively, enter these set of commands in your terminal:
1.	sudo apt-get install python-setuptools python-dev build-essential
2.	sudo easy_install pip
3.	sudo pip install --upgrade virtualenv

APPLICATION:
●	Image preview is unavailable
Go to Settings > Apps > ADVSF > Permissions, and turn on "Storage" permission.
●	Pop-up shows "Some Error".
Its a result of loss of an Active Internet Connection. Make sure you are connected to the internet, and try again.
●	Unexpected Result, shows Traceback ….… has no attribute '__getitem__'
The Applicant ID entered does not exist. Enter a valid Applicant ID.
