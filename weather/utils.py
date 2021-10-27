from .models import Data
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectKBest
from sklearn.preprocessing import LabelEncoder

precision = 5


def processCSV(data):
    X = list()
    Y = list()

    rows = data.read().decode('UTF-8').split('\n')
    total_good, total_bad = 0, 0
    good_outlook_sunny, good_outlook_overcast, good_outlook_rainy, good_temp_high, good_temp_mild, good_temp_cool, good_humidity_high, good_humidity_normal, good_windy_true, good_windy_false = [
        0] * 10
    bad_outlook_sunny, bad_outlook_overcast, bad_outlook_rainy, bad_temp_high, bad_temp_mild, bad_temp_cool, bad_humidity_high, bad_humidity_normal, bad_windy_true, bad_windy_false = [
        0] * 10
    is_outlook_selected, is_temp_selected, is_humidity_selected, is_windy_selected = [
        True] * 4

    label_encoder = LabelEncoder()

    for row in rows[1:]:
        try:
            outlook, temp, humidity, windy, weather = row.split(',')
        except(Exception):
            continue

        x = label_encoder.fit_transform([outlook, temp, humidity, windy])
        X.append(list(x))
        Y.append(weather)

        if weather == 'good':
            total_good += 1

            # Outlook
            if outlook == 'sunny':
                good_outlook_sunny += 1
            elif outlook == 'overcast':
                good_outlook_overcast += 1
            else:
                good_outlook_rainy += 1

            # Temperature
            if temp == 'high':
                good_temp_high += 1
            elif temp == 'mild':
                good_temp_mild += 1
            else:
                good_temp_cool += 1

            # Humidity
            if humidity == 'high':
                good_humidity_high += 1
            else:
                good_humidity_normal += 1

            # Windy
            if windy == 'true':
                good_windy_true += 1
            else:
                good_windy_false += 1

        else:
            total_bad += 1

            # Outlook
            if outlook == 'sunny':
                bad_outlook_sunny += 1
            elif outlook == 'overcast':
                bad_outlook_overcast += 1
            else:
                bad_outlook_rainy += 1

            # Temperature
            if temp == 'high':
                bad_temp_high += 1
            elif temp == 'mild':
                bad_temp_mild += 1
            else:
                bad_temp_cool += 1

            # Humidity
            if humidity == 'high':
                bad_humidity_high += 1
            else:
                bad_humidity_normal += 1

            # Windy
            if windy == 'true':
                bad_windy_true += 1
            else:
                bad_windy_false += 1
    total = total_good + total_bad

    chi2_score = calcChiSquare(X, Y)

    return {
        'chi2_score': chi2_score,
        'good_weather': total_good/total,
        'good_outlook_sunny': good_outlook_sunny/total_good,
        'good_outlook_overcast': good_outlook_overcast/total_good,
        'good_outlook_rainy': good_outlook_rainy/total_good,
        'good_temp_high': good_temp_high/total_good,
        'good_temp_mild': good_temp_mild/total_good,
        'good_temp_cool': good_temp_cool/total_good,
        'good_humidity_high': good_humidity_high/total_good,
        'good_humidity_normal': good_humidity_normal/total_good,
        'good_windy_true': good_windy_true/total_good,
        'good_windy_false': good_windy_false/total_good,
        'bad_weather': total_bad/total,
        'bad_outlook_sunny': bad_outlook_sunny/total_bad,
        'bad_outlook_overcast': bad_outlook_overcast/total_bad,
        'bad_outlook_rainy': bad_outlook_rainy/total_bad,
        'bad_temp_high': bad_temp_high/total_bad,
        'bad_temp_mild': bad_temp_mild/total_bad,
        'bad_temp_cool': bad_temp_cool/total_bad,
        'bad_humidity_high': bad_humidity_high/total_bad,
        'bad_humidity_normal': bad_humidity_normal/total_bad,
        'bad_windy_true': bad_windy_true/total_bad,
        'bad_windy_false': bad_windy_false/total_bad,
        'is_outlook_selected': is_outlook_selected,
        'is_temp_selected': is_temp_selected,
        'is_humidity_selected': is_humidity_selected,
        'is_windy_selected': is_windy_selected
    }


def getProbability(data: Data, outlook, temp, humidity, windy):

    good, bad = data.good_weather, data.bad_weather

    if data.is_outlook_selected:
        if outlook == 'sunny':
            good *= data.good_outlook_sunny
            bad *= data.bad_outlook_sunny
        elif outlook == 'overcast':
            good *= data.good_outlook_overcast
            bad *= data.bad_outlook_overcast
        else:
            good *= data.good_outlook_rainy
            bad *= data.bad_outlook_rainy

    if data.is_temp_selected:
        if temp == 'high':
            good *= data.good_temp_high
            bad *= data.bad_temp_high
        elif temp == 'mild':
            good *= data.good_temp_mild
            bad *= data.bad_temp_mild
        else:
            good *= data.good_temp_cool
            bad *= data.bad_temp_cool

    if data.is_humidity_selected:
        if humidity == 'high':
            good *= data.good_humidity_high
            bad *= data.bad_humidity_high
        else:
            good *= data.good_humidity_normal
            bad *= data.bad_humidity_normal

    if data.is_windy_selected:
        if windy == 'true':
            good *= data.good_windy_true
            bad *= data.bad_windy_true
        else:
            good *= data.good_windy_false
            bad *= data.bad_windy_false

    return round(good, precision), round(bad, precision)


def calcChiSquare(X, Y):
    label_encoder = LabelEncoder()
    y = list(label_encoder.fit_transform(Y))

    chi2score = chi2(X, y)              # (ch2-value, p-value)
    # chi2_features = SelectKBest(chi2, k='all')
    # X_kbest_features = chi2_features.fit_transform(X, y)
    return chi2score
