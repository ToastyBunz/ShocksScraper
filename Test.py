import pickle
car_pickle = open("./Favorites.pk", "rb")
car_contents = pickle.load(car_pickle)
print(car_contents)
