from Database import Rating, session
from Rater import Rater

# put already made ratings into table except 10 results for some user
ratings = session.query(Rating).all()
real_results = ratings[:10]
data = ratings[10:]
rater = Rater(data)

total_error = 0
for real_result in real_results:
    real_mark = real_result.mark
    predicted_ratings = rater.get_ratings(real_result.user_id)
    predicted_mark = predicted_ratings[real_result.movie_id]
    print("diff: {}\t real: {}\tpredicted:{}".format(abs(real_mark - predicted_mark), real_mark, predicted_mark))
    total_error += abs(real_mark - predicted_mark)
print(total_error / 10)
# get estimates for those results
# compare them


# diff: 0.25050359362432895	 real: 2.5	predicted:2.249496406375671
# diff: 0.2309004004413966	 real: 3	predicted:2.7690995995586034
# diff: 0.3817095466514031	 real: 3	predicted:2.618290453348597
# diff: 0.39263823590422087	 real: 2	predicted:2.392638235904221
# diff: 0.7008890654176327	 real: 4	predicted:3.2991109345823673
# diff: 0.9507700997812201	 real: 2	predicted:2.95077009978122
# diff: 0.9878910080325669	 real: 2	predicted:2.987891008032567
# diff: 1.066646152501515	 real: 2	predicted:3.066646152501515
# diff: 1.159839242405503	 real: 3.5	predicted:2.340160757594497
# diff: 0.8414740114032355	 real: 2	predicted:2.8414740114032355
# 0.6963261356163024
# 0.4463261356163024 - excluding 0.25 error due to real mark 0.5 granularity
