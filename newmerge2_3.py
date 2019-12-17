	#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
import math
import pytesseract
from fractions import gcd
import sys
import re
import MySQLdb
import datetime
from PIL import ImageFilter

def round(obj):
	return((int(obj[0]),int(obj[1]),int(obj[2]),int(obj[3])))

def levenshtein(s1, s2):
    if len(s1) < len(s2):
	return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
	return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
	current_row = [i + 1]
	for j, c2 in enumerate(s2):
	    insertions = previous_row[j + 1] + 1 # j+1 
	    deletions = current_row[j] + 1       # than s2
	    substitutions = previous_row[j] + (c1 != c2)
	    current_row.append(min(insertions, deletions, substitutions))
	previous_row = current_row
    return previous_row[-1]
    


#Initializing Data to Null



def aadharcrop(x):
	###FETCHING IMAGE
	img = Image.open(x)
	img = img.convert('L')
	img = img.point(lambda x: 0 if x<128 else 255, '1')
	###IMAGE SIZE
	iw,ih = img.size
	###IMAGE RATIO CALCULATION
	midval = gcd(iw,ih)
	pw=iw/midval
	ph=ih/midval

	###CO-ORDINATE POSITIONS
	snamepos=((29.687*iw/100, 28.79*ih/100, 75.02*iw/100, 35*ih/100))
	yobpos=((60.8*iw/100, 36*ih/100, 70*iw/100, 42*ih/100))		#small crop
	yobpos=((28*iw/100, 36*ih/100, 70*iw/100, 42*ih/100))		#line crop
	sexpos=((38.5*iw/100, 43*ih/100, 46.08*iw/100, 48.2*ih/100))
	uidpos=((26*iw/100, 72.11*ih/100, 71*iw/100, 81.97*ih/100))
	

	###NAME OCR
	name = img.crop(round(snamepos))
	#name.show()
	global DerivedSName
	DerivedSName = pytesseract.image_to_string(name)
	DNL = len(DerivedSName.split())
	global DerivedSFName
	global DerivedSLName
	global DerivedSMName	
	DerivedSName=DerivedSName.upper()
	
	if DNL == 3:
		DerivedSFName, DerivedSMName, DerivedSLName = DerivedSName.split(' ',2)

	elif DNL == 2:
		DerivedSFName, DerivedSLName = DerivedSName.split(' ',2)
		DerivedSMName = "----------------------------"

	elif DNL == 1:
		DerivedSFName = DerivedSName.split(' ',2)
		DerivedSMName = "----------------------------"
		DerivedSLName = "----------------------------"
	else:
		print "► CANT SPLIT NAME"
	

	###YOB OCR
	yob = img.crop(round(yobpos))

	global DerivedYOB 
	tempYOB = pytesseract.image_to_string(yob)
	DerivedYOB = re.sub("[^0-9]","",tempYOB)
	global dobyyyy
	dobyyyy=str(DerivedYOB)
	if len(dobyyyy)==2 :
		if dobyyyy[0]==0 :
			dobyyyy="20"+dobyyyy
		else:
			dobyyyy="19"+dobyyyy
	elif len(dobyyyy)==3 :
		if dobyyyy[0]==0 :
			dobyyyy="2"+dobyyyy
		else:
			dobyyyy="1"+dobyyyy



	###SEX OCR
	sex = img.crop(round(sexpos))
	#sex.show()
	global DerivedSex 
	DerivedSex= pytesseract.image_to_string(sex)

	###UID OCR
	uid = img.crop(round(uidpos))
	#uid.show()
	global DerivedUID 
	tempUID= pytesseract.image_to_string(uid)
	DerivedUID = re.sub("[^0-9]","",tempUID)

	print"►","SCANNED SELF NAME:     ","\n",(DerivedSFName, DerivedSMName, DerivedSLName),"\n"
	print"►","SCANNED YEAR OF BIRTH: ","\n",dobyyyy,"\n"
	print"►","SCANNED SEX:           ","\n",DerivedSex,"\n"
	print"►","SCANNED UID:           ","\n",DerivedUID



def licrop(x):
	###FETCHING IMAGE
	img = Image.open(x)
	img = img.convert('L')
	#img.show()
	###IMAGE SIZE
	iw,ih = img.size
	###IMAGE RATIO CALCULATION
	midval = gcd(iw,ih)
	pw=iw/midval
	ph=ih/midval

		
	snamepos=((12.5*iw/100, 65*ih/100, 40*iw/100, 69*ih/100))
	fnamepos=((13*iw/100, 69.8*ih/100, 40*iw/100, 73.8*ih/100))
	yobpos=((38*iw/100, 59*ih/100, 54*iw/100, 65*ih/100))
	bgpos=((63.6*iw/100, 60*ih/100, 67.6*iw/100, 65*ih/100))
	addpos=((0.9*iw/100, 73.8*ih/100, 60*iw/100, 85.7*ih/100))
	pinpos=((7.4*iw/100, 85.8*ih/100, 15.6*iw/100, 90*ih/100))

	###SELF NAME OCR
	sname = img.crop(round(snamepos))
	global DerivedSName 
	DerivedSName = pytesseract.image_to_string(sname)
	DNL = len(DerivedSName.split())
	global DerivedSFName
	global DerivedSLName
	global DerivedSMName	
	DerivedSName=DerivedSName.upper()

	if DNL == 3:
		DerivedSFName, DerivedSMName, DerivedSLName = DerivedSName.split(' ',2)

	elif DNL == 2:
		DerivedSFName, DerivedSLName = DerivedSName.split(' ',2)
		DerivedSMName = "----------------------------"

	elif DNL == 1:
		DerivedSFName = DerivedSName.split(' ',2)
		DerivedSMName = "----------------------------"
		DerivedSLName = "----------------------------"
	else:
		print "►"," CANT SPLIT NAME","\n"




	###FATHER NAME OCR
	fname = img.crop(round(fnamepos))
	global DerivedFName 
	DerivedFName= pytesseract.image_to_string(fname)
	DNL = len(DerivedFName.split())
	global DerivedFFName
	global DerivedFLName
	global DerivedFMName	
	DerivedFName=DerivedFName.upper()
	if DNL == 3:
		DerivedFFName, DerivedFMName, DerivedFLName = DerivedFName.split(' ',2)

	elif DNL == 2:
		DerivedFFName, DerivedFLName = DerivedFName.split(' ',2)
		DerivedFMName = "----------------------------"

	elif DNL == 1:
		DerivedFFName = DerivedFName.split(' ',2)
		DerivedFMName = "----------------------------"
		DerivedFLName = "----------------------------"
	else:
		print "►"," CANT SPLIT NAME"



	###YOB OCR
	yob = img.crop(round(yobpos))
	global DerivedYOB
	tempYOB = pytesseract.image_to_string(yob)
	DerivedYOB = re.sub("[^0-9]","",tempYOB)
	global dobdd
	global dobmm
	global dobyyyy
	if len(DerivedYOB)==10:
		dobdd=DerivedYOB[0:2]
		dobmm=DerivedYOB[3:5]
		dobyyyy=DerivedYOB[6:10]	
	else:
		dobdd=DerivedYOB[0:2]
		dobmm=DerivedYOB[2:4]
		dobyyyy=DerivedYOB[4:]			
	dobdd.strip
	dobmm.strip
	dobyyyy.strip
	if len(dobyyyy)==2 :
		if dobyyyy[0]==0 :
			dobyyyy="20"+dobyyyy
		else:
			dobyyyy="19"+dobyyyy
	elif len(dobyyyy)==3 :
		if dobyyyy[0]==0 :
			dobyyyy="2"+dobyyyy
		else:
			dobyyyy="1"+dobyyyy


	###BG OCR
	bg = img.crop(round(bgpos))
	global DerivedBG 
	DerivedBG = pytesseract.image_to_string(bg,config='-psm 7')

	###ADD OCR
	add = img.crop(round(addpos))
	global DerivedAdd
	DerivedAdd = pytesseract.image_to_string(add)


	###PIN OCR
	pin = img.crop(round(pinpos))
	global DerivedPin
	tempPin = pytesseract.image_to_string(pin, config='-psm 7')
	DerivedPin = re.sub("[^0-9]","",tempPin)

	print "►","SCANNED SELF NAME:       ","\n",(DerivedSFName, DerivedSMName, DerivedSLName),"\n"
	print "►","SCANNED FATHER NAME:     ","\n",(DerivedFFName, DerivedFMName, DerivedFLName),"\n"
	print "►","SCANNED DATE OF BIRTH:   ","\n",(dobdd,dobmm,dobyyyy)

def pancrop(x):

	###FETCHING IMAGE
	img = Image.open(x)
	img = img.convert('L')
	#img = img.point(lambda x: 0 if x<128 else 255, '1')

	###IMAGE SIZE
	iw,ih = img.size
	###IMAGE RATIO CALCULATION
	midval = gcd(iw,ih)
	pw=iw/midval
	ph=ih/midval
	snamepos=((3.194*iw/100, 26.7*ih/100, 72.89*iw/100, 34.2*ih/100))
	fnamepos=((3.194*iw/100, 38*ih/100, 70.5*iw/100, 49*ih/100))
	yobpos=((2.5*iw/100, 50.15*ih/100, 23*iw/100, 60.6*ih/100))
	uidpos=((3.194*iw/100, 65.4*ih/100, 32.73*iw/100, 75.3*ih/100))

	###SELF NAME OCR
	sname = img.crop(round(snamepos))
	global DerivedSName
	DerivedSName = pytesseract.image_to_string(sname)
	DNL = len(DerivedSName.split())
	global DerivedSFName
	global DerivedSLName
	global DerivedSMName	
	DerivedSName=DerivedSName.upper()
	if DNL == 3:
		DerivedSFName, DerivedSMName, DerivedSLName = DerivedSName.split(' ',2)

	elif DNL == 2:
		DerivedSFName, DerivedSLName = DerivedSName.split(' ',2)
		DerivedSMName = "----------------------------"

	elif DNL == 1:
		DerivedSFName = DerivedSName.split(' ',2)
		DerivedSMName = "----------------------------"
		DerivedSLName = "----------------------------"
	else:
		print "►"," CANT SPLIT NAME","\n"
	


	###FATHER NAME OCR
	fname = img.crop(round(fnamepos))
	global DerivedFName
	DerivedFName = pytesseract.image_to_string(fname)
	DNL = len(DerivedFName.split())
	global DerivedFFName
	global DerivedFLName
	global DerivedFMName	
	DerivedFName=DerivedFName.upper()
		
	if DNL == 3:
		DerivedFFName, DerivedFMName, DerivedFLName = DerivedFName.split(' ',2)

	elif DNL == 2:
		DerivedFFName, DerivedFLName = DerivedFName.split(' ',2)
		DerivedFMName = "----------------------------"

	elif DNL == 1:
		DerivedFFName = DerivedFName.split(' ',2)
		DerivedFMName = "----------------------------"
		DerivedFLName = "----------------------------"
	else:
		print "►"," CANT SPLIT NAME"
	
	###YOB OCR
	yob = img.crop(round(yobpos))
	#yob.show()
	global DerivedYOB
	tempYOB = pytesseract.image_to_string(yob)
	DerivedYOB = re.sub("[^0-9]","",tempYOB)
	global dobdd
	global dobmm
	global dobyyyy
	if len(DerivedYOB)==10:
		dobdd=DerivedYOB[0:2]
		dobmm=DerivedYOB[3:5]
		dobyyyy=DerivedYOB[6:10]	
	else:
		dobdd=DerivedYOB[0:2]
		dobmm=DerivedYOB[2:4]
		dobyyyy=DerivedYOB[4:]	
	if len(dobyyyy)==2 :
		if dobyyyy[0]==0 :
			dobyyyy="20"+dobyyyy
		else:
			dobyyyy="19"+dobyyyy
	elif len(dobyyyy)==3 :
		if dobyyyy[0]==0 :
			dobyyyy="2"+dobyyyy
		else:
			dobyyyy="1"+dobyyyy



	###UID OCR
	uid = img.crop(round(uidpos))

	global DerivedUID
	tempUID = pytesseract.image_to_string(uid)
	DerivedUID = re.sub(" ","",tempUID)
	print "►","SCANNED SELF NAME:       ","\n",(DerivedSFName, DerivedSMName, DerivedSLName),"\n"
	print "►","SCANNED FATHER NAME:     ","\n",(DerivedFFName, DerivedFMName, DerivedFLName),"\n"
	print "►","SCANNED DATE OF BIRTH:   ","\n",(dobdd,dobmm,dobyyyy),"\n"
	print "►","SCANNED UID:             ","\n",DerivedUID


def docDet(fileName):
	class Template:
		standardTexts=[]
		name=''
		def __init__(self,n,st):
			self.name=n
			self.standardTexts=st

	#defination of document templates
	AadharMah=Template('Aadhar Card of Maharashtra',[('आधार - सामान्य माणसाचा अधिकार','hin')])
	AadharUP=Template('Aadhar Card of UP',[('आधार - आम आदमी कडा अधिकार','hin')])
	pan=Template('Pan Card',[('INCOMETAXDEPARTMENT GOVT. OF INDIA','eng'),('INCOME TAX DEPARTMENT','eng'),('Permanent Account Number','eng')])
	mahDL=Template('Maharastra State Driving Licence',[('MAHARASHTRA STATE MOTOR DRIVING LICENCE','eng')])
	upDL=Template('Uttar Pradesh State Driving Licence',[('UNION OF INDIA Driving Licence . @','eng')])
	votCard=Template('Voter''s card',[('ELECTION COMMTSSION OF INDIA','eng')])

	templates=[AadharMah,AadharUP,pan,mahDL,upDL,votCard]

	#defination of standard text stings
	stEng=['MAHARASHTRA STATE MOTOR DRIVING LICENCE','Permanent Account Number','INCOMETAXDEPARTMENT GOVT. OF INDIA','ELECTION COMMTSSION OF INDIA','INCOME TAX DEPARTMENT','UNION OF INDIA Driving Licence . @']

	stHin=['आधार - सामान्य माणसाचा अधिकार','आधार - आम आदमी कडा अधिकार']

	#def p(str):
		#print(str,end='')
	def pnl(str):
		print(str)

	
	#search algo
	def search(str,st):
		for text in str.split('\n'):
			for s in st:
				if levenshtein(text,s)<10:
					return(s)

	#detection function

	def detect(fileName):
		img=Image.open(fileName)
		img=img.convert("L")
		str=pytesseract.image_to_string(img,lang='eng')
		res=search(str,stEng)
		if res==None:
			str=pytesseract.image_to_string(img,lang='hin+eng')
			return(search(str,stHin))
		else:	
			return(res)

	#Comparing Detected String accross defined Templates
	def templateCompare(fileName):
		string=detect(fileName)
		for t in templates:
			for st in t.standardTexts:
				if st[0]==string:
					return(t.name)
	return(templateCompare(fileName))

def dbcon():
        global sid
	db = MySQLdb.connect("ec2-52-5-15-233.compute-1.amazonaws.com","root","ignitesql","aligarh_db" )
	cursor = db.cursor()
	query="select first_name,last_name,aadhar_id,user_dob from user_details where user_name='"+sid+"';"
	#print query;
	cursor.execute(query)
	data = cursor.fetchone()
	dbsfn=data[0]
	dbsln=data[1]
	dbAUID=data[2]
	tempYOB=data[3]
	dbYOB=str(tempYOB)	
	dbdobyyyy=dbYOB[0:4]
	dbdobmm=dbYOB[5:7]
	dbdobdd=dbYOB[8:10]
	return (dbsfn, dbsln, dbAUID, dbdobdd, dbdobmm, dbdobyyyy)
	db.close()
def res(x):
	if x<2:
		return( "Perfect Match " )
	elif x<5:
		return( "Partial Match " )
	else:
		return( "Mismatch " )
	
def resint(x):
	if x<1:
		return( "Perfect Match " )
	elif x<2:
		return( "Partial Match " )
	else:
		return( "Mismatch " )
	


def verify():

	db = MySQLdb.connect("ec2-52-5-15-233.compute-1.amazonaws.com","root","ignitesql","aligarh_db" )
	dbSFName,dbSLName,dbUID, dbdobdd,dbdobmm,dbdobyyyy=dbcon()
	dbSFName=dbSFName.upper()
	dbSLName=dbSLName.upper()
	print "_______________________________________________\n\n►FROM Database Data :\n", dbSFName,dbSLName,dbUID, dbdobdd,dbdobmm,dbdobyyyy,"\n"
	print "►FROM Scanned Data  :\n", DerivedSFName,DerivedSLName,DerivedUID,dobdd,dobmm,dobyyyy,"\n_______________________________________________\n"
	
	sfnamescore=levenshtein(DerivedSFName,dbSFName)
	slnamescore=levenshtein(DerivedSLName,dbSLName)
	uidscore=levenshtein(DerivedUID,dbUID)
	datescore=levenshtein(dobdd,dbdobdd)
	monthscore=levenshtein(dobmm,dbdobmm)
	yearscore=levenshtein(dobyyyy,dbdobyyyy)
	
	if sfnamescore>=0:
		print"►",res(sfnamescore),"in First name ","\n"," (",DerivedSFName,") / (",dbSFName,")","\n" 
	if slnamescore>=0:
		print"►",res(slnamescore),"in Last name  ","\n"," (",DerivedSLName,") / (",dbSLName,")","\n"
	if uidscore>=0:
		print"►",resint(uidscore),"in UID        ","\n"," (",DerivedUID,") / (",dbUID,")","\n"
	if datescore>=0:
		print "►",resint(datescore),"in DOB(Date)  ","\n"," (",dobdd,") / (",dbdobdd,")","\n"
	if monthscore>=0:
		print "►",resint(monthscore),"in DOB(Month) ","\n"," (",dobmm,") / (",dbdobmm,")","\n"
	if yearscore>=0:
		print "►",resint(yearscore),"in DOB(Year)  ","\n"," (",dobyyyy,") / (",dbdobyyyy,")"
	print "_______________________________________________\n"	
	if yearscore>0:
		yeardiff=int(dobyyyy)-int(dbdobyyyy)
		print "►","AGE DIFFERS BY ",  yeardiff, "YEARS"
		
	systime=datetime.datetime.now().date().strftime("%Y")
	global realage
	realage=int(systime)-int(dobyyyy)	
	if realage<18:
		print "★ Underage by", realage," years (acc. to document)","\n"
	else:
		print realage," years old (acc. to document)"
	

#x=["../LICROP/liparas.jpg","../LICROP/liakash.jpg","../PANCROP/panricha.jpg","../PANCsROP/panakash.jpg","../LICROP/liricha.jpg","../LICROP/lijay.jpg","../AADHARCROP/aadharjay.jpg"]
global sid
sid=str(sys.argv[1])
userinputimage = str(sys.argv[2])
x=[userinputimage]

for i in x:
	DerivedSFName=''
	DerivedSMName=''
	DerivedSLName=''
	DerivedFFName=''
	DerivedFMName=''
	DerivedFLName=''
	DerivedSex=''
	DerivedYOB=''
	DerivedUID=''
	dobdd='--'
	dobmm='--'
	dobyyyy=''
	DerivedBG=''
	DerivedAdd=''
	DerivedPin=''
	realage=''		
	#print "_______________________________________________\nReading ",  i,"..."
	typ=docDet(i)
	print "\n_______________________________________________\n\n★DOCUMENT TYPE: ",typ,"\n_______________________________________________" 
	print	
	if typ=='Aadhar Card of Maharashtra':
		aadharcrop(i)
		verify()
		print
		print
	elif typ=='Maharastra State Driving Licence':
		licrop(i)
		verify()
		print
		print
	elif typ=='Pan Card':
		pancrop(i)
		verify()
		print
		print
	else:
		print("Cropper Unavailable")
		print
		print
