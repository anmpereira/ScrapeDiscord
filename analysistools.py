import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


def linear_regression(times, weights):
    times = np.array(times)[:, np.newaxis]
    reg = LinearRegression().fit(times, weights)
    return {'slope': reg.coef_[0], 'intercept': reg.intercept_, 'score': reg.score(times, weights),
            'regressor': reg}


def plot_data(dates, times, weights, regressor):
    fig = plt.figure(figsize=(16, 9))
    plt.grid()
    plt.xlabel('date')
    plt.ylabel('weight (Kg)')

    plt.scatter(dates, weights)

    points = np.array([[times[0]], [times[-1]]])
    plt.plot(points, regressor.predict(points))

    plt.title('Change: {:.2f} Kg/month'.format(regressor.coef_[0]*30), fontdict={'size': 20})
