import util.mongo_utility
import util.constants

# id_string = "603d99433f4f13f03e9d02a6"
id_string = "603d99443f4f13f03e9d02a7"

rs = mongo_utility.delete_with_id(constants.DATABASE_NAME_MAIN, constants.COLLECTION_NAME_BOOK, id_string)
print(rs)