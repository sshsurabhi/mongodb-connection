mongoimport -d sample -c zips --authenticationDatabase admin --username datascientest --password dst123 --file /data/db/zips.json
mongosh -u datascientest -p dst123
use grades
db.grades.find().sort({"student_id":-1})
exit
mongoimport -d sample -c zips --authenticationDatabase admin --username datascientest --password dst123 --file /data/db/grades.json
db.grades.find().sort({"student_id":-1})
use sample
mongoimport -d sample -c zips --authenticationDatabase admin --username datascientest --password dst123 --file /data/db/zips.jsonuse sample
use sample
db.grades.findOne()
exit
mongoimport -d sample -c grades --authenticationDatabase admin -u datascientest -p dst123 --file /data/db/grades.json
mongosh -u datascientest -p dst123
exit
mongoimport -d sample -c grades --authenticationDatabase admin -u datascientest -p dst123 --file /data/db/zips.json
mongosh -u datascientest -p dst123
mongoimport -d sample -c cie --authenticationDatabase admin -u datascientest -p dst123 --file /data/db/companies.json
mongosh -u datascientest -p dst123
exit
mongoimport -d sample -c books --authenticationDatabase admin --username datascientest --password dst123 --file data/db/books.json
exit
