from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django import forms
from pybtex.database.input import bibtex
import os
import sqlite3
from forms import DocumentForm, QueryForm

""" views.py: contains functions called by urls.py when specific webpages are accessed """

def mainpage(request):
    """ mainpage(request): is called when mainpage.html is accessed. Lists collections if a database exists, otherwise creates a new empty database bibtexinfo.db """
    database_exists = False
    output=os.listdir('.')
    if 'bibtexinfo.db' in os.listdir('.'):
        database_exists = True
        connection = sqlite3.connect("bibtexinfo.db")
        cursor = connection.cursor()
    else:
        connection = sqlite3.connect("bibtexinfo.db")
        cursor = connection.cursor()
        # create new database
        sql_cmd = """CREATE TABLE bib (id INTEGER PRIMARY KEY AUTOINCREMENT,
            collection TEXT, tag TEXT, author_list TEXT, journal TEXT, volume INT, pages TEXT, year INT, title TEXT)"""
        cursor.execute(sql_cmd)
    sql_cmd="SELECT * FROM bib"
    cursor.execute(sql_cmd)
    db_info = cursor.fetchall()
    collections=[]
    for i in db_info:
        collections.append(str(i[1]))
    collections = set(collections) # set containing the collection names
    return render_to_response('mainpage.html',locals())
    connection.commit()
    cursor.close()

def insert_collection(request):
    """ insert_collection(request): called when insert_collections.html is accessed. Contains form that allows user to upload a file for a new collection. Upload is passed to upload_file"""
    form=DocumentForm()
    return render_to_response('insert_collection.html',{'form':form},
                              context_instance=RequestContext(request))

def upload_file(request):
    """ upload_file(request): handles uploaded file. Reads in file, parses the bibtex, and stores values in bibtexinfo.db """
    uploadsuccess = False
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        postee=request.POST
        filess=request.FILES
        if form.is_valid():
            uploadsuccess=True
            # write temporary .bib file here
            destination = open('tmp.bib', 'wb+')
            for chunk in request.FILES['docfile'].chunks():
                destination.write(chunk)
            destination.close()
            # parse .bib file, input into sql database
            parser=bibtex.Parser()
            bib_data=parser.parse_file('tmp.bib')
            tags=bib_data.entries.keys()
            connection = sqlite3.connect("bibtexinfo.db")
            cursor = connection.cursor()
            for a in tags:
                title=str(bib_data.entries[a].fields['title'])[1:-1]
                journal=str(bib_data.entries[a].fields['journal'])[1:]
                volume=(bib_data.entries[a].fields['volume'])
                pages=(bib_data.entries[a].fields['pages'])
                year=(bib_data.entries[a].fields['year'])
                authors=str(bib_data.entries[a].fields['author']).replace('{','').replace('}','')
                # format and upload database entries
                entry=[str(request.POST['title']),str(a),str(authors),str(journal),int(volume),str(pages),int(year),str(title)]
                sql_cmd=("INSERT INTO bib (collection, tag, author_list, journal, volume, pages, year, title) VALUES " + str(tuple(entry)))
                cursor.execute(sql_cmd)
            connection.commit()
            cursor.close()
    else:
        form = DocumentForm() # empty form
    return render_to_response('upload_file.html',locals(),context_instance=RequestContext(request))
                                 
def query(request):
    """ query(request): called when query.html is accessed. Accepts sql-formatted queries and passes request to list_results """
    form=QueryForm()
    return render_to_response('query.html',{'form':form},
                              context_instance=RequestContext(request))

def list_results(request):
    """ list_results(request): called when list_requests.html is accessed. Displays bibtex info in user-friendly format for terms that match query """
    outstring = 'No Results to Display' # if no results, display this to user
    if request.method == 'POST':
        form=QueryForm(request.POST)
        if form.is_valid():
            search=str(request.POST['title'])
            connection = sqlite3.connect("bibtexinfo.db")
            cursor = connection.cursor()
            sql_cmd="SELECT * FROM bib WHERE "+search
            try:
                cursor.execute(sql_cmd)
                db_info = cursor.fetchall()
                if len(db_info)>0: outstring='' # if query successful, no error message is printed
            except:
                outstring = 'Invalid Format! Please Try Again' # if exception is raised, print format error
                db_info = []
    form=QueryForm()
    return render_to_response('list_results.html',locals(),context_instance=RequestContext(request))
