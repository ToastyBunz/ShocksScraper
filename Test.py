import pickle

# carlist = ["Toyota", "AUDI", "Mercedes"]
# with open("carlist.pkl", 'ab') as carpickle:
#     pickle.dump(carlist, carpickle)

with open('carlist.pkl', 'rb+') as carpickle:
    mycar=pickle.load(carpickle)

    mycar.append('Bugatti')

# print(mycar)