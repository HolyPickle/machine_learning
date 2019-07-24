from snowballstemmer import TurkishStemmer

snow = TurkishStemmer()

s1 = "değiştir"

s2 = "istemiyorum"

print(snow.stemWord(s1))

print(snow.stemWord(s2))
import multiprocessing
