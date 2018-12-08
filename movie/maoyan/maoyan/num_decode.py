import requests
from fontTools.ttLib import TTFont

headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) " 
                          "Chrome/66.0.3359.139 Safari/537.36 " }

def getNumber(url, encrypt_number):

    woff_url = 'https:' + url
    response_woff = requests.get(woff_url, headers = headers).content

    with open('fonts.woff','wb') as f:
        f.write(response_woff)

    baseFonts = TTFont('base.woff')
    base_nums = ['5', '3', '0', '2', '7', '6', '4', '1', '9', '8']
    base_fonts = ['uniE6EC', 'uniEB3E', 'uniF538', 'uniEC6C', 'uniEB22', 'uniF72B', 'uniE1FC', 'uniF1F8', 'uniF63B', 'uniE19E']
    onlineFonts = TTFont('fonts.woff')

    baseGlyphName_number = {
            'uniE6EC': '5', 'uniEB3E': '3',
            'uniF538': '0', 'uniEC6C': '2',
            'uniEB22': '7', 'uniF72B': '6',
            'uniE1FC': '4', 'uniF1F8': '1',
            'uniF63B': '9', 'uniE19E': '8'
            }

    def transform_single_enc(enc):
        onlineForm = onlineFonts['glyf']['uni' + '%X' % ord(enc)]
        print('onlineForm', onlineForm)
        for name, num in baseGlyphName_number.items():
            if onlineForm == baseFonts['glyf'][name]:
                return num

    result = []
    for each in encrypt_number:
        result.append(''.join(transform_single_enc(c) if ord(c) > 256 else c for c in each))
    
    return result



