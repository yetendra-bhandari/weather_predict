def processCSV(data):
    rows = data.read().decode('UTF-8').split('\n')
    total_good, total_bad = 0, 0
    good_outlook_sunny, good_outlook_overcast, good_outlook_rainy, good_temp_high, good_temp_mild, good_temp_cool, good_humidity_high, good_humidity_normal, good_windy_true, good_windy_false = [
        0] * 10
    bad_outlook_sunny, bad_outlook_overcast, bad_outlook_rainy, bad_temp_high, bad_temp_mild, bad_temp_cool, bad_humidity_high, bad_humidity_normal, bad_windy_true, bad_windy_false = [
        0] * 10
    is_outlook_selected, is_temp_selected, is_humidity_selected, is_windy_selected = [
        True] * 4
    for row in rows[1:]:
        try:
            outlook, temp, humidity, windy, weather = row.split(',')
        except(Exception):
            continue

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
    return {
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
