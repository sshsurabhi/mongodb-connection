from pymongo import MongoClient
from pprint import pprint
import json, datetime

#connect to MongoDB via pymongo
client = MongoClient(
    host="127.0.0.1",
    port=27017,
    username="datascientest",
    password="dst123",
    authSource="admin"
)

# Access the database
# db = client.sample
db = client['sample']

# list of available databases
available_databases = client.list_database_names()
pprint('available dbs are:')
pprint(available_databases)

# list of collections available in database
collections = db.list_collection_names()
pprint('total colections are:')
pprint(collections)

# Display one of the document in collections.
one_document = db.books.find_one()
pprint('one of the documents in the books collection')
pprint(one_document)

# Display the number of documents in collection
total_documents = db.books.count_documents({})
pprint('total number of documents in the books collection')
pprint(total_documents)

#####################################################################################

# number of books with more than 400 pages
books_over_400 = db.books.count_documents({"pageCount": {"$gt": 400}})
pprint('books_over_400')
pprint(books_over_400)

# number of books with more than 400 pages that are published
published_books_over_400 = db.books.count_documents({
    "pageCount": {"$gt": 400},
    "status": "PUBLISH"
})
pprint('published_books_over_400')
pprint(published_books_over_400)
######################################################################################

# number of books with the keyword Android in their description
android_books = db.books.count_documents({
    "$or": [
        {"shortDescription": {"$regex": ".*Android.*", "$options": "i"}},
        {"longDescription": {"$regex": ".*Android.*", "$options": "i"}}
    ]
})
pprint('books with "Android" in their description')
pprint(android_books)
######################################################################################

# Display the 2 distinct category lists (depending of the index 0 and 1)
categories = list(db.books.aggregate([
    {"$group": {
        "_id": None,
        "Category1": {"$addToSet": {"$arrayElemAt": ["$categories", 0]}},
        "Category2": {"$addToSet": {"$arrayElemAt": ["$categories", 1]}}
    }}
]))
pprint('\ndistint category books list')
pprint(categories)
#######################################################################################

# number of books containing the Python, Java, C++, Scala language names in their long description 
languages_count = db.books.count_documents({
    "longDescription": {
        "$regex": ".*(Python|Java|C\+\+|Scala).*",
        "$options": "i"
    }
})
pprint('books with specific programming languages')
pprint(languages_count)
#######################################################################################

#Statistical information about average number of pages per category
stats_per_category = list(db.books.aggregate([
    {"$unwind": "$categories"},
    {"$group": {
        "_id": "$categories",
        "max_pages": {"$max": "$pageCount"},
        "min_pages": {"$min": "$pageCount"},
        "avg_pages": {"$avg": "$pageCount"}
    }}
]))
pprint('List of Statistical information about average number of pages per category:')
pprint(stats_per_category)
########################################################################################

#Extract year, month, day from the publication date
date_info = list(db.books.aggregate([
    {"$match": {"publishedDate": {"$exists": True}}},
    {"$project": {
        "_id": 0,
        "title": 1,
        "year": {"$year": "$publishedDate"},
        "month": {"$month": "$publishedDate"},
        "day": {"$dayOfMonth": "$publishedDate"}
    }},
    {"$match": {"year": {"$gt": 2009}}},
    {"$limit": 20}
]))
print('The year, month, day from the publication date', date_info)
########################################################################################

# Creating new attributes for list of authors
authors_info = list(db.books.aggregate([
    {"$project": {
        "title": 1,
        "author_1": {"$arrayElemAt": ["$authors", 0]},
        "author_2": {"$arrayElemAt": ["$authors", 1]},
        "author_3": {"$arrayElemAt": ["$authors", 2]}
    }},
    {"$sort": {"publishedDate": 1}},
    {"$limit": 20}
]))
pprint('new attributes for authors')
pprint(authors_info)
#########################################################################################

# displaying number of publications for top 10 most prolific authors.
author_publications = list(db.books.aggregate([
    {"$project": {"first_author": {"$arrayElemAt": ["$authors", 0]}}},
    {"$group": {"_id": "$first_author", "publications": {"$sum": 1}}},
    {"$sort": {"publications": -1}},
    {"$limit": 10}
]))
pprint('publications per first author')
pprint(author_publications)
##########################################################################################
"""
Optional
"""
# distribution of the number of authors
author_count = list(db.books.aggregate([
    {"$project": {
        "title": 1,
        "num_authors": {"$size": "$authors"}
    }},
    {"$group": {
        "_id": "$num_authors",
        "count": {"$sum": 1}
    }}
]))
pprint('distribution of Number of authors per book')
pprint(author_count)
#########################################################################################

#Count occurrence of each author by index
author_occurrence = list(db.books.aggregate([
    {"$unwind": "$authors"},
    {
        "$match": {
            "authors": {"$ne": ""}  # Make sure author names are not empty
        }
    },
    {"$group": {
        "_id": "$authors",
        "occurrence": {"$sum": 1}
    }},
    {"$sort": {"occurrence": -1}},
    {"$limit": 20}
]))
pprint('Count occurrence of each author by index')
pprint(author_occurrence)
###########################################################################################

with open("result.txt", "w") as file:
    file.write("Available Databases:\n")
    file.write(f"{available_databases}\n\n")

    file.write("Collections in 'sample' Database:\n")
    file.write(f"{collections}\n\n")

    file.write("One Document:\n")
    file.write(f"{one_document}\n\n")

    file.write("Total Documents:\n")
    file.write(f"{total_documents}\n\n")

    file.write("Books with >400 Pages:\n")
    file.write(f"{books_over_400}\n")
    file.write("Published Books with >400 Pages:\n")
    file.write(f"{published_books_over_400}\n\n")

    file.write("Books with 'Android' in Description:\n")
    file.write(f"{android_books}\n\n")

    file.write("Distinct Categories:\n")
    file.write(f"{categories}\n\n")

    file.write("Books with Specific Languages:\n")
    file.write(f"{languages_count}\n\n")

    file.write("Page Statistics by Category:\n")
    file.write(f"{stats_per_category}\n\n")

    file.write("Books Published After 2009 with Dates:\n")
    file.write(f"{date_info}\n\n")

    file.write("Authors Information:\n")
    file.write(f"{authors_info}\n\n")

    file.write("Top 10 Most Prolific Authors:\n")
    file.write(f"{author_publications}\n\n")

    file.write("Number of Authors per Book:\n")
    file.write(f"{author_count}\n\n")

    file.write("Author Occurrences by Index:\n")
    file.write(f"{author_occurrence}\n")