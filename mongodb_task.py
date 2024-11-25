from pymongo import MongoClient
from pprint import pprint
import json
import datetime
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

# Output the available databases
available_databases = client.list_database_names()

# Output the available collections
collections = db.list_collection_names()

# Get one document
one_document = db.books.find_one()

total_documents = db.books.count_documents({})
print('available databases',available_databases)
pprint('available dbs are:')
pprint(available_databases)
print('total colections are:', collections)
print('one of the documents in the books collection',one_document)
print('total number of documents in the books collection',total_documents)

# Books with more than 400 pages
books_over_400 = db.books.count_documents({"pageCount": {"$gt": 400}})

# Books with more than 400 pages and published
published_books_over_400 = db.books.count_documents({
    "pageCount": {"$gt": 400},
    "status": "PUBLISH"
})

print(f"Books with more than 400 pages: {books_over_400}")
print(f"Books with more than 400 pages and published: {published_books_over_400}")

pprint('published_books_over_400')
pprint(published_books_over_400)
pprint('books_over_400')
pprint(books_over_400)

#books with "Android" in their description
android_books = db.books.count_documents({
    "$or": [
        {"shortDescription": {"$regex": ".*Android.*", "$options": "i"}},
        {"longDescription": {"$regex": ".*Android.*", "$options": "i"}}
    ]
})

pprint('books with "Android" in their description')
pprint(android_books)

# (b) Number of books with the keyword Android in their description
num_books_android_in_desc = db.books.count_documents({
    "$or": [
        {"shortDescription": {"$regex": "Android", "$options": "i"}},
        {"longDescription": {"$regex": "Android", "$options": "i"}}
    ]
})

print(f"Books with 'Android' in description: {num_books_android_in_desc}")

#########################################

#Displaying distinct categories
categories = list(db.books.aggregate([
    {"$group": {
        "_id": None,
        "Category1": {"$addToSet": {"$arrayElemAt": ["$categories", 0]}},
        "Category2": {"$addToSet": {"$arrayElemAt": ["$categories", 1]}}
    }}
]))

print('distint category books list', categories)
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

# Collecting categories for display
categories_list = list(distinct_categories)
pprint(categories_list)

###################################################################
#books with specific programming languages
languages_count = db.books.count_documents({
    "longDescription": {
        "$regex": ".*(Python|Java|C\+\+|Scala).*",
        "$options": "i"
    }
})
print('books with specific programming languages', languages_count)


# (d) Number of books containing language names in their descriptions
num_books_with_languages = db.books.count_documents({
    "$or": [
        {"longDescription": {"$regex": "Python|Java|C\\+\\+|Scala", "$options": "i"}}
    ]
})

print(f"Books with specified languages in description: {num_books_with_languages}")
#####################################################################
#Statistical information about pages per category

stats_per_category = list(db.books.aggregate([
    {"$unwind": "$categories"},
    {"$group": {
        "_id": "$categories",
        "max_pages": {"$max": "$pageCount"},
        "min_pages": {"$min": "$pageCount"},
        "avg_pages": {"$avg": "$pageCount"}
    }}
]))

print('Statistical information about pages per category list:', stats_per_category)

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

##############################################
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
print('Extract year, month, day from the publication date', date_info)

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

# Display results as a list using list comprehension instead of a loop
pprint('publication_years\n')
pprint(list(publication_years))
#########################################################
#new attributes for authors
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

print('new attributes for authors', authors_info)


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

# Display results as a list using list comprehension instead of a loop
pprint(list(authors_projection))
###################################################
#publication counts per first author
author_publications = list(db.books.aggregate([
    {"$project": {"first_author": {"$arrayElemAt": ["$authors", 0]}}},
    {"$group": {"_id": "$first_author", "publications": {"$sum": 1}}},
    {"$sort": {"publications": -1}},
    {"$limit": 10}
]))

print('publications per first author', author_publications)


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

# Display results as a list using list comprehension instead of a loop
pprint(list(top_authors))
#################################################

"""
Optional
"""
#Count number of authors per book
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

print('Number of authors per book', author_count)

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

# Display results as a list using list comprehension instead of a loop
pprint('Number of authors per book')
pprint(list(authors_distribution))
##############################################
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


# print('Count occurrence of each author by index', author_occurrence)

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

# Display results as a list using list comprehension instead of a loop
pprint('Occurrence of each author by index')
pprint(list(author_indices))



with open("result_1.txt", "w") as file:
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