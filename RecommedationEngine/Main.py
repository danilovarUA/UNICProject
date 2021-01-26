from Database import session, Rating, Recommendation
from Rater import Rater
import Constants


class RecommendationEngine:
    def __init__(self):
        self.ratings = session.query(Rating).all()  # TODO rating changed
        self.rater = None
        self.initialise_rater()

    def initialise_rater(self):
        print("Initialising Rater")
        self.rater = Rater(self.ratings)

    def generate_all_recommendations(self):
        print("Counting user rating")
        user_likes = count_user_ratings(self.ratings)
        print("Users for recommendations before trim: {}".format(len(user_likes)))
        user_likes = trim_users(user_likes)
        print("Users for recommendations after trim: {}".format(len(user_likes)))
        for user in user_likes:
            print("Generating recommendation for user with id {}".format(user))
            self.generate_recommendations_for_user(user)

    def generate_recommendations_for_user(self, user_id):
        recommendations = self.rater.get_ratings(user_id)
        recommendations = trim_watched_recommendations(user_id, recommendations)
        recommendations_keys = sorted(recommendations, key=recommendations.get,
                                      reverse=True)[:Constants.RECOMMENDATIONS_PER_USER]
        new_recommendations = {}
        for key in recommendations_keys:
            new_recommendations[key] = recommendations[key]
        for movie_id in new_recommendations:
            session.add(Recommendation(
                user_id=user_id, movie_id=movie_id, expected_mark=new_recommendations[movie_id]))
            session.commit()


def count_user_ratings(ratings):
    user_likes = {}
    for rating in ratings:
        if rating.user_id in user_likes:
            user_likes[rating.user_id] += 1
        else:
            user_likes[rating.user_id] = 1
    return user_likes


def trim_users(user_likes):
    removal_candidates = []
    for user in user_likes:
        if user_likes[user] < Constants.MIN_RATINGS_TO_RECOMMEND:
            removal_candidates.append(user)
    for removal_candidate in removal_candidates:
        del user_likes[removal_candidate]
    return user_likes


def trim_watched_recommendations(user_id, recommendations):
    user_ratings = session.query(Rating).filter_by(user_id=user_id).all()
    liked_movie_ids = [user_rating.movie_id for user_rating in user_ratings]
    deletion_candidates = []
    for movie_id in recommendations:
        if movie_id in liked_movie_ids:
            deletion_candidates.append(movie_id)
    for deletion_candidate in deletion_candidates:
        del recommendations[deletion_candidate]
    return recommendations


if __name__ == "__main__":
    re = RecommendationEngine()
    re.generate_all_recommendations()