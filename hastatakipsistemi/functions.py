
from flask import request

def average_age_func(patients):
    average_age = 0
    for patient in patients:
        average_age += patient.age
    average_age = average_age / len(patients)
    return average_age

def number_of_provience(result):
    provience = {}
    liste = []
    for a in result:
        liste.append(a)
    provience = dict(liste)

    for a in range(1, 82):
        try:
            provience[a]
        except:
            provience[a] = 0
    return provience

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
