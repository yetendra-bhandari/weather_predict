from .models import Data
from sklearn.feature_selection import chi2
from sklearn.preprocessing import LabelEncoder

precision = 5


def processCSV(data):
    X_encoded = list()
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
        X_encoded.append(list(x))
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

    chi2_score = calcChiSquare(X_encoded, Y)
    chi2_outlook = chi2_score[0][0]
    chi2_temp = chi2_score[0][1]
    chi2_humidity = chi2_score[0][2]
    chi2_windy = chi2_score[0][3]

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
        'chi2_outlook': chi2_outlook,
        'chi2_temp': chi2_temp,
        'chi2_humidity': chi2_humidity,
        'chi2_windy': chi2_windy,
        'is_outlook_selected': is_outlook_selected,
        'is_temp_selected': is_temp_selected,
        'is_humidity_selected': is_humidity_selected,
        'is_windy_selected': is_windy_selected
    }


def getProbability(data: Data, features, outlook, temp, humidity, windy):

    good, bad = data.good_weather, data.bad_weather
    features_used = getFeaturesToUse([data.chi2_outlook, data.chi2_temp,
                                      data.chi2_humidity, data.chi2_windy], int(features))

    # update in use flags
    if 1 not in features_used:
        data.is_outlook_selected = False
    if 2 not in features_used:
        data.is_temp_selected = False
    if 3 not in features_used:
        data.is_humidity_selected = False
    if 4 not in features_used:
        data.is_windy_selected = False
    data.save()

    if 1 in features_used:
        if outlook == 'sunny':
            good *= data.good_outlook_sunny
            bad *= data.bad_outlook_sunny
        elif outlook == 'overcast':
            good *= data.good_outlook_overcast
            bad *= data.bad_outlook_overcast
        else:
            good *= data.good_outlook_rainy
            bad *= data.bad_outlook_rainy

    if 2 in features_used:
        if temp == 'high':
            good *= data.good_temp_high
            bad *= data.bad_temp_high
        elif temp == 'mild':
            good *= data.good_temp_mild
            bad *= data.bad_temp_mild
        else:
            good *= data.good_temp_cool
            bad *= data.bad_temp_cool

    if 3 in features_used:
        if humidity == 'high':
            good *= data.good_humidity_high
            bad *= data.bad_humidity_high
        else:
            good *= data.good_humidity_normal
            bad *= data.bad_humidity_normal

    if 4 in features_used:
        if windy == 'true':
            good *= data.good_windy_true
            bad *= data.bad_windy_true
        else:
            good *= data.good_windy_false
            bad *= data.bad_windy_false

    good = round(good * 100/(good + bad))
    bad = 100 - good
    return good, bad


def getFeaturesToUse(chi2score, features_num):
    res_dct = {i: chi2score[i-1] for i in range(1, len(chi2score)+1)}
    sorted_features = {k: v for k, v in sorted(
        res_dct.items(), key=lambda item: item[1], reverse=True)}

    nums = 0
    features_used = []
    for feature in sorted_features:
        if nums == features_num:
            break
        features_used.append(feature)
        nums += 1
    return features_used


def calcChiSquare(X_encoded, Y):
    label_encoder = LabelEncoder()
    y = list(label_encoder.fit_transform(Y))

    chi2score = chi2(X_encoded, y)              # (ch2-value, p-value)
    return chi2score
