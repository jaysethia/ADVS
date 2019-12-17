#!/usr/bin/python
# -*- coding: utf-8 -*-
import zbarlight
import xml.etree.ElementTree as ET
import sys
import MySQLdb
import datetime
name=sys.argv[2]
tree= ET.parse(name)
root=tree.getroot()

namearr=(root.attrib['name']).split(" ")

global DerivedSFName
global DerivedSLName
global DervedUID
global dobyyyy
DerivedSFName,DerivedSLName,DerivedUID,dobyyyy=namearr[0],namearr[2],root.attrib['uid'],root.attrib['yob']

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




def dbcon():
	sid=sys.argv[1]
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
	global DerivedSFName
	global DerivedSLName
	global DervedUID
	global dobyyyy
	db = MySQLdb.connect("ec2-52-5-15-233.compute-1.amazonaws.com","root","ignitesql","aligarh_db" )
	dbSFName,dbSLName,dbUID, dbdobdd,dbdobmm,dbdobyyyy=dbcon()
	dbSFName=dbSFName.upper()
	dbSLName=dbSLName.upper()
	print "_______________________________________________\n\n►FROM Database Data :\n", dbSFName,dbSLName,dbUID, dbdobdd,dbdobmm,dbdobyyyy,"\n"
	print "►FROM Scanned Data  :\n", DerivedSFName,DerivedSLName,DerivedUID,dobyyyy,"\n_______________________________________________\n"
	
	sfnamescore=levenshtein(DerivedSFName,dbSFName)
	slnamescore=levenshtein(DerivedSLName,dbSLName)
	uidscore=levenshtein(DerivedUID,dbUID)
	yearscore=levenshtein(dobyyyy,dbdobyyyy)
	
	if sfnamescore>=0:
		print"►",res(sfnamescore),"in First name ","\n"," (",DerivedSFName,") / (",dbSFName,")","\n" 
	if slnamescore>=0:
		print"►",res(slnamescore),"in Last name  ","\n"," (",DerivedSLName,") / (",dbSLName,")","\n"
	if uidscore>=0:
		print"►",resint(uidscore),"in UID        ","\n"," (",DerivedUID,") / (",dbUID,")","\n"
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

#CODE

verify()



