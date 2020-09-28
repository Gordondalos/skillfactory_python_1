import math
import json


def corr(data_x, data_y):
    sx, sy, sxy, sx2, sy2, n = 0.0, 0.0, 0.0, 0.0, 0.0, 0
    for x, y in zip(data_x, data_y):
        sx += x
        sx2 += x * x
        sy += y
        sy2 += y * y
        sxy += x * y
        n += 1
    dd = math.sqrt((sx2 / n - (sx / n * sx / n)) * (sy2 / n - (sy / n * sy / n)))
    if abs(dd) < 1e-5:
        return None
    return (sxy / n - sx / n * sy / n) / dd


def correlation_cases_tests(country_code):
    with open("covid.json") as file:
        arr = json.loads(file.read())
        total_new_cases = []
        total_new_test = []
        for item in arr[country_code]['data']:
            if item['date'].split('-')[1] == '08':
                if 'new_cases' not in item:
                    total_new_cases.append(0)
                    continue
                if 'new_tests' not in item:
                    total_new_test.append(0)
                    continue

                total_new_cases.append(float(item['new_cases']))
                total_new_test.append(float(item['new_tests']))

        return corr(total_new_cases, total_new_test)
