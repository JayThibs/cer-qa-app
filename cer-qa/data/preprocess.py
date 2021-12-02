from bs4 import BeautifulSoup
import re


def splitText(text):
    return text.split("\n\n")

def cleanText(text):
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("\r", " ")
    text = text.replace("\xa0", " ")
    text = text.replace("\u200b", " ")
    text = text.replace("\u200c", " ")
    text = BeautifulSoup(text, "html.parser").get_text(separator=' ') # remove html tags
    text = re.sub('\w{25,}', ' ',text) # remove long words
    text = re.sub('cid\d+', ' ',text) # remove cids
    text = re.sub(' s ', ' ',text) # remove s because of s tags
    text = re.sub(r'\s+',' ',text) # remove extra spaces
    return text