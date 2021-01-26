import cv2
import numpy as np
import math
from numpy.lib.shape_base import array_split


def resim_okuma(path):  # resim dosyasını okuma fonksiyonu
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    return image


def rgb_hist(image):  # girilen resmi red,blue,green histogramlarına ayırma ve normalizasyon yapma fonksiyonu
    [rows, cols, bit] = image.shape
    size = rows*cols
    red = np.zeros(256)
    green = np.zeros(256)
    blue = np.zeros(256)
    for i in range(rows):
        for j in range(cols):
            red[image[i][j][0]] += 1
            green[image[i][j][1]] += 1
            blue[image[i][j][2]] += 1
    # resmin histogramı resmin boyutuna bölünerek (pixellerin bulunma olasılıkları eldesi) normalizasyon yapılıyor.
    for i in range(0, 256):
        red[i] = red[i] / size
        green[i] = green[i] / size
        blue[i] = blue[i] / size
    return red, blue, green


Tüm resimler için oluşan histogramlar 3 boyutlu matriste tutmak için yazdığım kodu kısmı.Bunu her defasında programı çalıştırmamak için yaptım.
rgb_list = np.zeros(shape=(150, 3, 256))
def liste_olusturma(rgb_list, i):
    red, blue, green = rgb_hist(image1)
    rgb_list[i, 0, :] = red.copy()
    rgb_list[i, 1, :] = blue.copy()
    rgb_list[i, 2, :] = green.copy()


for i in range(0, 25):
    path = "dogtrain/" + str(i+1) + ".jpg"
    image1 = resim_okuma(path)
    red, blue, green = rgb_hist(image1)
    rgb_list[i, 0, :] = red.copy()
    rgb_list[i, 1, :] = blue.copy()
    rgb_list[i, 2, :] = green.copy()

for i in range(0, 25):
    path = "cameltrain/" + str(i+1) + ".jpg"
    image1 = resim_okuma(path)
    red, blue, green = rgb_hist(image1)
    rgb_list[(25+i), 0, :] = red.copy()
    rgb_list[(25+i), 1, :] = blue.copy()
    rgb_list[(25+i), 2, :] = green.copy()


for i in range(0, 25):
    path = "dolphin_egitim/" + str(i+1) + ".jpg"
    image1 = resim_okuma(path)
    red, blue, green = rgb_hist(image1)
    rgb_list[(50+i), 0, :] = red.copy()
    rgb_list[(50+i), 1, :] = blue.copy()
    rgb_list[(50+i), 2, :] = green.copy()


for i in range(0, 25):
    path = "giraffetrain/" + str(i+1) + ".jpg"
    image1 = resim_okuma(path)
    red, blue, green = rgb_hist(image1)
    rgb_list[(75+i), 0, :] = red.copy()
    rgb_list[(75+i), 1, :] = blue.copy()
    rgb_list[(75+i), 2, :] = green.copy()


for i in range(0, 25):
    path = "goosetrain/" + str(i+1) + ".jpg"
    image1 = resim_okuma(path)
    red, blue, green = rgb_hist(image1)
    rgb_list[(100+i), 0, :] = red.copy()
    rgb_list[(100+i), 1, :] = blue.copy()
    rgb_list[(100+i), 2, :] = green.copy()


for i in range(0, 25):
    path = "horsetrain/" + str(i+1) + ".jpg"
    image1 = resim_okuma(path)
    red, blue, green = rgb_hist(image1)
    rgb_list[(125+i), 0, :] = red.copy()
    rgb_list[(125+i), 1, :] = blue.copy()
    rgb_list[(125+i), 2, :] = green.copy()

np.save('list', rgb_list) #save dosyam

def findmin(a, b, c):  # rgb-hsv dönüşümü için gerekli olan min ve max fonksiyonu
    if(a <= b and a <= c):
        return a
    elif(b <= a and b <= c):
        return b
    else:
        return c


def findmax(a, b, c):
    if(a >= b and a >= c):
        return a
    elif(b >= a and b >= c):
        return b
    else:
        return c


# red,blue,green listesinden hsv uzayın hue ya çevirme fonksiyonu,Bu fonksiyona rgb_list matrisinin sadeece 1 elemanı giriyor
def rgb_to_hsv(r, b, g):
    cmax = findmax(r, g, b)    # r, g, b arasında en büyüğü
    cmin = findmin(r, g, b)    # r, g, b arasında en küçüğü
    diff = cmax-cmin       # en büyük ile en küçüğü arasındaki fark
    # fark 0 ise hue=0'dır
    if cmax == cmin:
        h = 0
    # cmax=r ise hue formulü
    elif cmax == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    # cmax=g ise hue formulü
    elif cmax == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    # cmax=b ise hue formulü
    elif cmax == b:
        h = (60 * ((r - g) / diff) + 240) % 360
    return h


def hue_train_hist(rgb_list):  # kaydettiğimiz hue liste için gerekli kod

    hue_list = np.zeros(shape=(150, 256))
    for i in range(0, 150):
        for j in range(0, 256):
            hue_list[i, j] = rgb_to_hsv(
                rgb_list[i, 0, j], rgb_list[i, 1, j], rgb_list[i, 2, j])

    return hue_list


# hue_list = np.zeros(shape=(150, 256))
# hue_list = hue_hist(rgb_list)
# np.save('huelist', hue_list)
# uzaklık listesini sıralama ve enküçük 5 indisi alma fonksiyonu bubble sort kullandım
def bubblesort(distance):
    indis = []
    for i in range(0, 150):
        indis.append(i)
    n = len(distance)
    for i in range(n):
        for j in range(0, n-i-1):
            if distance[j] >= distance[j+1]:
                distance[j], distance[j+1] = distance[j+1], distance[j]
                indis[j], indis[j+1] = indis[j+1], indis[j]
    return indis[:5]

# t grup sayısı


def rgb_test(rgb_list, t):  # rgb için test fonksiyonum öklid distance formülü kodun içinde anlattı
    acc = []
    c = 0
    for i in range(0, 5):
        # tüm test grupları aynı anda test etmekiçin for döngüsü
        path0 = "test" + str(t) + "/"+str(i+1)+".jpg"
        image1 = resim_okuma(path0)
        red, blue, green = rgb_hist(image1)
        dtlist = np.zeros(150)
        for k in range(0, 150):
            # öklid distance yaptığım yer.Öncelikle test resmi için oluşan r,g,b histogramları listedeki oluşan r,g,b histogramlarıyla tek tek uzaklığını hesaplayıp distance listeme kayıt ediyorum.uzaklık için formül: sqrt((rt-ri)^2+(bt-bi)^2+(gt-gi)^2) dir.
            for j in range(0, 256):
                dtlist[k] += math.sqrt(((red[j]-rgb_list[k, 0, j])**2)+(
                    (blue[j]-rgb_list[k, 1, j])**2)+((green[j]-rgb_list[k, 2, j])**2))
        # test için gerekli olan en yakın 5 uzaklık indisini aldım
        min = bubblesort(dtlist)
        for j in range(0, 5):
            if(int(min[j]/25)+1 == t):  # indis gruba uygun mu kontrolü yaptım
                acc.append(True)
            else:
                acc.append(False)
    newarr = array_split(acc, 5)
    p = []
    for i in range(0, 5):  # kaçtane true kaçtane yanlış yakınlık
        for j in range(0, 5):
            if(newarr[i][j] == True):
                c += 1
        p.append(c)
        c = 0
    return p

# t grup sayısı


def hue_test(hue_list, t):  # hue test fonksiyonum gidişat şekli rgb ye benzer ama öklid için sadece bir özelliği kullandım(hue)
    acc = []
    for i in range(0, 5):
        path0 = "test" + str(t) + "/"+str(i+1)+".jpg"
        image = resim_okuma(path0)
        red, blue, green = rgb_hist(image)
        h = np.zeros(256)
        distance = np.zeros(150)
        for j in range(0, 256):
            h[j] = rgb_to_hsv(red[j], blue[j], green[j])
        for j in range(0, 150):
            for k in range(0, 256):
                distance[j] = math.sqrt((h[k]-hue_list[j, k])**2)
        mint = bubblesort(distance)
        for j in range(0, 5):
            if(math.floor(mint[j]/25)+1 == t):
                acc.append(True)
            else:
                acc.append(False)
    newarr = array_split(acc, 5)
    p = []
    c = 0
    for i in range(0, 5):
        for j in range(0, 5):
            if(newarr[i][j] == True):
                c += 1
        p.append(c)
        c = 0
    return p


a = 0
p = 0
rgb_list = np.load('rgblist.npy')  # kayıtlı numpy dosylarını okuma
hue_list = np.load('huelist.npy')
#c = hue_test(hue_list, 2)
c = rgb_test(rgb_list, 2)
for j in range(0, 5):
    if(c[j] == 0):
        p += 1
p = 5-p
p = (p/5)*100
print('Seçilen test grubu için accurancy yüzdesi', p)
for i in range(1, 7):
    p = 0
    # c = rgb_test(rgb_list, i)
    c = hue_test(hue_list, i)
    for j in range(0, 5):
        if(c[j] == 0):
            p += 1
    p = 5-p
    p = (p/5)*100
    print(i, '. test grubu için accurancy yüzdesi', p)
    a += p
print('Bütün test için accurancy yüzdesi', a/6)
