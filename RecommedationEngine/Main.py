from Database import Database
from Rater import Rater
import Constants


class RecommendationEngine:
    def __init__(self):
        self.database = Database()
        self.rating = self.database.select_all("rating")[1]
        self.rater = None
        self.initialise_rater()

    def initialise_rater(self):
        print("Initialising Rater")
        self.rater = Rater(self.rating)

    def generate_all_recommendations(self):
        print("Counting user rating")
        user_likes = count_user_ratings(self.rating)
        print("Users for recommendations before trim: {}".format(len(user_likes)))
        user_likes = trim_users(user_likes)
        print("Users for recommendations after trim: {}".format(len(user_likes)))
        for user in user_likes:
            print("Generating recommendation for user with id {}".format(user))
            self.generate_recommendations_for_user(user)

    def generate_recommendations_for_user(self, user_id):
        recommendations = self.rater.get_ratings(user_id)
        recommendations = trim_watched_recommendations(user_id, recommendations, self.database)
        recommendations_keys = sorted(recommendations, key=recommendations.get,
                                      reverse=True)[:Constants.MIN_RATINGS_TO_RECOMMEND]
        new_recommendations = {}
        for key in recommendations_keys:
            new_recommendations[key] = recommendations[key]
        for movie_id in new_recommendations:
            self.database.insert({"user_id": user_id, "movie_id": movie_id,
                                  "predicted_rating": new_recommendations[movie_id]}, "recommendation")


def count_user_ratings(rating):
    # TODO store as a user field to save time PROBABLY
    user_likes = {}
    for item in rating:
        if item[0] in user_likes:
            user_likes[item[0]] += 1
        else:
            user_likes[item[0]] = 1
    return user_likes


def trim_users(user_likes):
    removal_candidates = []
    for user in user_likes:
        if user_likes[user] < Constants.MIN_RATINGS_TO_RECOMMEND:
            removal_candidates.append(user)
    for removal_candidate in removal_candidates:
        del user_likes[removal_candidate]
    return user_likes


def trim_watched_recommendations(user_id, recommendations, database):
    user_rating = database.select_eq({"user_id": user_id}, "rating")[1]
    liked_movies = [item[1] for item in user_rating]
    deletion_candidates = []
    for movie_id in recommendations:
        if movie_id in liked_movies:
            deletion_candidates.append(movie_id)
    for deletion_candidate in deletion_candidates:
        del recommendations[deletion_candidate]
    return recommendations


if __name__ == "__main__":
    re = RecommendationEngine()
    re.generate_all_recommendations()