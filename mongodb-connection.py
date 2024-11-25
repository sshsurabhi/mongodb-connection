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
#####################################################################################

# (b) Number of books with the keyword Android in their description
num_books_android_in_desc = db.books.count_documents({
    "$or": [
        {"shortDescription": {"$regex": "Android", "$options": "i"}},
        {"longDescription": {"$regex": "Android", "$options": "i"}}
    ]
})
pprint("Books with 'Android' in description:")
pprint(num_books_android_in_desc)
#####################################################################################

# (c) Display distinct category lists using aggregation
distinct_categories = db.books.aggregate([
    {
        "$group": {
            "_id": {
                "category1": {"$arrayElemAt": ["$categories", 0]},
                "category2": {"$arrayElemAt": ["$categories", 1]}
            }
        }
    }
])
categories_list = list(distinct_categories)
pprint(categories_list)
#####################################################################################

# (d) Number of books containing language names in their descriptions
num_books_with_languages = db.books.count_documents({
    "$or": [
        {"longDescription": {"$regex": "Python|Java|C\\+\\+|Scala", "$options": "i"}}
    ]
})
pprint(f"Books with specified languages in description:")
pprint(num_books_with_languages)
#####################################################################################

# (e) Statistical info: max, min, avg number of pages per category
categories_stats = db.books.aggregate([
    {"$unwind": "$categories"},
    {
        "$group": {
            "_id": "$categories",
            "maxPages": {"$max": "$pageCount"},
            "minPages": {"$min": "$pageCount"},
            "avgPages": {"$avg": "$pageCount"}
        }
    }
])
pprint(list(categories_stats))
#####################################################################################

# (f) Extract year, month, day from publication date, filtering books published after 2009
publication_years = db.books.aggregate([
    {
        "$match": {
            "publishedDate": {"$gt":  datetime.datetime(2009, 1, 1)}
        }
    },
    {
        "$project": {
            "title": 1,
            "year": {"$year": "$publishedDate"},
            "month": {"$month": "$publishedDate"},
            "day": {"$dayOfMonth": "$publishedDate"}
        }
    },
    {"$limit": 20}
])
pprint('publication_years\n')
pprint(list(publication_years))
#####################################################################################

# (g) Create new attributes (author_1, author_2, ...) for the first 20 authors
authors_projection = db.books.aggregate([
    {
        "$project": {
            "authors": 1,
            "author_1": {"$arrayElemAt": ["$authors", 0]},
            "author_2": {"$arrayElemAt": ["$authors", 1]},
            "author_3": {"$arrayElemAt": ["$authors", 2]},
            # Add more if needed
        }
    },
    {"$limit": 20}
])
pprint(list(authors_projection))
#####################################################################################

# (h) Count the number of publications by the first author
top_authors = db.books.aggregate([
    {
        "$project": {
            "first_author": {"$arrayElemAt": ["$authors", 0]}
        }
    },
    {
        "$group": {
            "_id": "$first_author",
            "count": {"$sum": 1}
        }
    },
    {"$sort": {"count": -1}},
    {"$limit": 10}
])
pprint(list(top_authors))
#####################################################################################

# (i) Optional: Distribution of the number of authors
authors_distribution = db.books.aggregate([
    {
        "$project": {
            "num_authors": {"$size": "$authors"}
        }
    },
    {
        "$group": {
            "_id": "$num_authors",
            "count": {"$sum": 1}
        }
    }
])
pprint('Number of authors per book')
pprint(list(authors_distribution))
#####################################################################################

# (j) Optional: Occurrence of each author by index
author_indices = db.books.aggregate([
    {"$unwind": "$authors"},
    {
        "$match": {
            "authors": {"$ne": ""}
        }
    },
    {
        "$group": {
            "_id": "$authors",
            "count": {"$sum": 1}
        }
    },
    {"$sort": {"count": -1}},
    {"$limit": 20}
])
pprint('Occurrence of each author by index')
pprint(list(author_indices))