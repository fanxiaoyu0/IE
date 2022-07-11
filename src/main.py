import json
import pickle
from tqdm import tqdm
import math
import matplotlib.pyplot as plt

def get_frequency_of_chinese_characters():
    with open('../data/translation2019zh_train.json','r',encoding='utf-8') as f:
        chineseCharacters=[]
        characterFrequency={}
        lines=f.readlines()
        for index,line in enumerate(tqdm(lines)):
            # if (index+1)%20000==0:
            #     print(chineseCharacters)
            #     print(characterFrequency)
            #     break
            jsonLine=json.loads(line)
            chineseString=jsonLine['chinese']
            for character in chineseString:
                if character >= u'\u4e00' and character <= u'\u9fff':
                    if character not in chineseCharacters:
                        chineseCharacters.append(character)
                        characterFrequency[character]=1
                    else:
                        characterFrequency[character]+=1
        pickle.dump(chineseCharacters,open('../result/chineseCharacters.pkl','wb'))
        json.dump(chineseCharacters,open('../result/chineseCharacters.json','w',encoding='utf-8'),ensure_ascii=False,indent=4)
        pickle.dump(characterFrequency,open('../result/characterFrequency.pkl','wb'))
        json.dump(characterFrequency,open('../result/characterFrequency.json','w',encoding='utf-8'),ensure_ascii=False,indent=4)

def get_frequency_of_english_letter():
    with open('../data/translation2019zh_train.json','r',encoding='utf-8') as f:
        letters="abcdefghijklmnopqrstuvwxyz"
        letterFrequency={}
        for letter in letters:
            letterFrequency[letter]=0
        lines=f.readlines()
        for index,line in enumerate(tqdm(lines)):
            # if (index+1)%100000==0:
            #     print(letterFrequency)
            #     break
            jsonLine=json.loads(line)
            englishString=jsonLine['english'].lower()
            for letter in letters:
                letterFrequency[letter]+=englishString.count(letter)
        print(letterFrequency)
        pickle.dump(letterFrequency,open('../result/letterFrequency.pkl','wb'))
        json.dump(letterFrequency,open('../result/letterFrequency.json','w',encoding='utf-8'),indent=4)

def calculate_information_entropy_of_chinese_characters():
    with open('../result/characterFrequency.json','r',encoding='utf-8') as f:
        characterFrequency=json.load(f)
        totalCharacterCount=sum(characterFrequency.values())
        print(totalCharacterCount)

        informationEntropy=0
        pDict={}
        for character in characterFrequency.keys():
            p=characterFrequency[character]/totalCharacterCount
            informationEntropy+=(-p*math.log(p,2))
            pDict[character]=p
        print(informationEntropy)

        pList=sorted(pDict.items(), key=lambda x: x[1], reverse=True)
        # 下面两行用于显示中文
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar([x[0] for x in pList[:80]], [x[1] for x in pList[:80]],width = 0.8)
        plt.ylabel("Frequency")
        plt.title("不同汉字的出现频率")
        plt.show() 

def calculate_information_entropy_of_english_letters():
    with open('../result/letterFrequency.json','r',encoding='utf-8') as f:
        letterFrequency=json.load(f)
        totalLetterCount=sum(letterFrequency.values())
        print(totalLetterCount)
        
        informationEntropy=0
        pDict={}
        for letter in letterFrequency.keys():
            p=letterFrequency[letter]/totalLetterCount
            print(letter,":",round(p,4))
            informationEntropy+=(-p*math.log(p,2))
            pDict[letter]=p
        print(informationEntropy)

        # 下面两行用于显示中文
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(list(pDict.keys()), list(pDict.values()),width = 0.8)
        plt.ylabel("Frequency")
        plt.title("不同英文字母的出现频率")
        plt.show() 

if __name__ == '__main__':
    # get_frequency_of_chinese_characters()
    # get_frequency_of_english_letter()
    calculate_information_entropy_of_chinese_characters()
    calculate_information_entropy_of_english_letters()
    print("All is well!")