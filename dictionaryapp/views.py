from django.shortcuts import render
import requests
from .models import WordoftheDay
from datetime import timedelta
from django.utils import timezone
# Create your views here.


def getRandomword():

    url = "https://wordsapiv1.p.rapidapi.com/words/"

    querystring = {"random":"true"}

    headers = {
        'x-rapidapi-key': "43a36074a4mshc32fb43f3febbbfp15bf05jsnf08fe0672f3a",
        'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()


def wordoftheday():
    current_word =WordoftheDay.objects.last()
    if current_word != None:
        deadline=current_word.timestamp+timedelta(24)

        if deadline > timezone.now():
            word = current_word.word
            definition=current_word.definitions

            return {
                "word": word,
                "definition": definition
            }
        else:
            current_word.delete()

            random_word=getRandomword()
            word = random_word['word']
            definition=random_word['results'][0]['definition']

            WordoftheDay.objects.create(word=word,definition=definition)

            return {
                "word": word,
                "definition": definition
            }
    else:
        random_word=getRandomword()
        word = random_word['word']
        definition=random_word['results'][0]['definition']

        WordoftheDay.objects.create(word=word,definitions=definition)

        return {
            "word": word,
            "definition": definition
        }



def index(request):
    word_of_day = wordoftheday()

    context = {
        "method":'GET',
        "word": word_of_day['word'],
        "definition":word_of_day['definition']
    }

    if request.method == "POST":
        user_word = request.POST.get('user_word')
        print(user_word)
        url = f"https://wordsapiv1.p.rapidapi.com/words/{user_word}"

        headers = {
            'x-rapidapi-key': '43a36074a4mshc32fb43f3febbbfp15bf05jsnf08fe0672f3a',
            'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers)

        result = response.json()
        
        try:
            search_word = result['word']
            word_definition = result['results']
            pronunciations = result['pronunciation']

            context={
                "method":'POST',
                'search_word':search_word,
                'results':word_definition,
                'pronunciations':pronunciations
            }
        except KeyError:
            context={
                'error':result['message'],
                'failure':True
            }


    return render(request, "dictionaryapp/index.html", context=context)