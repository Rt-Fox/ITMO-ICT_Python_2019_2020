def freq(str): 
    words_list = str.split() 
    unique_words = set(words_list) 
      
    result = dict()
    for words in unique_words : 
        result[words] = words_list.count(words)
    return result


file = open("text1.txt", "r")
i = 0
content = ""
for line in file: # итерация по строкам файла
    content += line.replace("\n", "")
    i += 1
file.close()

f = open("textDict.txt", "w")
f.write(str(freq(content)))
f.close()