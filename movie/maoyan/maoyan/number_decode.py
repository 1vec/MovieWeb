##############################################
##       用于猫眼电影加密字符的解密         ##
##    输入：字符文件下载地址、加密的字符串  ##
##    输出：解密的字符串                    ##
##############################################

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

    uni_list = onlineFonts.getGlyphNames()[1:-1]
    temp = {}

    for i in range(10):
        onlineGlyph = onlineFonts['glyf'][uni_list[i]]
        for j in range(10):
            baseGlyph = baseFonts['glyf'][base_fonts[j]]
            if onlineGlyph == baseGlyph:
                temp['&#x' + uni_list[i][3:].lower()] = base_nums[j]

    results = []
    for encrypt_num in encrypt_number:
        point_pos = encrypt_num.find('.')
        point_pos = point_pos/8
        encrypt_num = encrypt_num.replace('.', '')

        numbers = encrypt_num.splite(';')
        for i in range(0, len(numbers)):
            numbers[i] = temp[numbers[i]]

        numbers.insert(point_pos, '.')
        results.append(int(numbers.join('')))

    return results
