import pandas as pd
from surprise import Reader, Dataset, KNNWithMeans
from RecommedationEngine import Constants


#  https://realpython.com/build-recommendation-engine-collaborative-filtering/#how-to-find-similar-users-on-the-basis-of-ratings


class Rater:
    def __init__(self, ratings):
        self.classifier = KNNWithMeans(sim_options={"name": "cosine", "user_based": False})
        self.training_set = None
        self.ratings_dict = None
        self._prepare_data_(ratings)
        self._train_()

    def _prepare_data_(self, ratings):
        self.ratings_dict = {
            "user_id": [item.user_id for item in ratings],
            "movie_id": [item.movie_id for item in ratings],
            "mark": [item.mark for item in ratings]
        }
        df = pd.DataFrame(self.ratings_dict)
        data = Dataset.load_from_df(df[["user_id", "movie_id", "mark"]], Reader(rating_scale=Constants.RATING_SCALE))
        self.training_set = data.build_full_trainset()

    def _train_(self):
        self.classifier.fit(self.training_set)

    def get_ratings(self, user_id):
        predicted_ratings = {}
        for movie_id in self.ratings_dict["movie_id"]:
            prediction = self.classifier.predict(user_id, movie_id)
            predicted_ratings[movie_id] = prediction.est
        return predicted_ratings
