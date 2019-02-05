from PIL import Image
import hashlib
import time
import math
import os
letters = []

def getpix(im):#验证码字符像素点
    his = im.histogram()
    values = {}
    for i in range(256):
        values[i] = his[i]

    for j,k in sorted(values.items(),key=lambda v:v[1],reverse=True)[:10]:
        print j,k
    

# pix = 220,227


    

# 取单个字符图片作为训练集合
def geticonset(im2):# 分割图片
    inletter = 0
    foundletter = 0
    start = 0
    end = 0

    for y in range(im2.size[0]):
        for x in range(im2.size[1]):
            pix = im2.getpixel((y,x))
            if pix != 255:
                inletter = 1
        if inletter == 1 and foundletter == 0:
            foundletter = 1
            start = y
        if inletter == 0 and foundletter == 1:
            foundletter = 0
            end = y
            letters.append((start,end))
        inletter = 0
    '''
    count = 0
    for letter in letters:
        m = hashlib.md5()
        im3 = im2.crop((letter[0],0,letter[1],im2.size[1]))
        m.update('%s%s'%(time.time(),count))
        im3.save('./%s.gif'%(m.hexdigest()))
        count += 1
        # os.mkdir('./iconset/%s/%s'%(text,imgname))
        '''
class VectorCompare:# 矢量空间搜索引擎http://ondoc.logand.com/d/2697/pdf

    def magnitude(self,concordance):
        total = 0
        for word,count in concordance.iteritems():
            total += count ** 2
        return math.sqrt(total)
    def relation(self,concordance1,concordance2):
        relevance = 0
        topvalue = 0
        for word,count in concordance1.iteritems():
            if concordance2.has_key(word):
                topvalue += count * concordance2[word]

        return topvalue / (self.magnitude(concordance1)*self.magnitude(concordance2))



def buildvector(im):# 图片转为矢量
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1

    return d1


if __name__=='__main__':
    im = Image.open('captcha.gif')
    im.convert("P")
    getpix(im)
    pix1 = int(input('input pix1: '))
    pix2 = int(input('input pix2: '))
    im2 = Image.new("P",im.size,255)
    for x in range(im.size[1]):
        for y in range(im.size[0]):
            pix = im.getpixel((y,x))
            if pix==pix1 or pix==pix2:
                im2.putpixel((y,x),0)
    geticonset(im2)
    
    iconset = ['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    imageset = []
    for letter in iconset:
        for img in os.listdir('./iconset/%s/'%(letter)):
            temp = []
            if img != "Thumbs.db" and img != ".DS_Store":
                temp.append(buildvector(Image.open("./220iconset/%s/%s"%(letter,img))))
            imageset.append({letter:temp})

    count = 0
    v = VectorCompare()
    for letter in letters:
        im3 = im2.crop((letter[0],0,letter[1],im2.size[1]))
        guess = []
        for image in imageset:
            for x,y in image.iteritems():
                if len(y) != 0:
                    guess.append((v.relation(y[0],buildvector(im3)),x))

        guess.sort(reverse=True)
        print "",guess[0]
        count += 1
    

        



