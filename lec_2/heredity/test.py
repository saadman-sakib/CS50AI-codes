from heredity import*


# if len(sys.argv) != 2:
#     sys.exit("Usage: python heredity.py data.csv")
people = load_data('data/family0.csv')

# Keep track of gene and trait probabilities for each person
# probabilities = {
#     person: {
#         "gene": {
#             2: 0,
#             1: 0,
#             0: 0
#         },
#         "trait": {
#             True: 0,
#             False: 0
#         }
#     }
#     for person in people
# }

# import pprint
# pprint.pprint(people)

print(joint_probability({
  'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
  'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
  'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
}, {'James'}, {'Harry', 'Lily'}, {'James'})) 