import requests
from fontTools.ttLib import TTFont

def main():
    encrypt_number = ['\ued82.\ueb28', '\uf3a1\uf5a3.\ued82', '\ued82\uf3a1\ue781\uf5a3']

    baseFonts = TTFont('base.woff')
    base_nums = ['5', '3', '0', '2', '7', '6', '4', '1', '9', '8']
    base_fonts = ['uniE6EC', 'uniEB3E', 'uniF538', 'uniEC6C', 'uniEB22', 'uniF72B', 'uniE1FC', 'uniF1F8', 'uniF63B', 'uniE19E']
    onlineFonts = TTFont('fonts.woff')
    """

    uni_list = onlineFonts.getGlyphNames()[1:-1]
    print(onlineFonts.getGlyphNames())
    temp = {}

    for i in range(10):
        onlineGlyph = onlineFonts['glyf'][uni_list[i]]
        for j in range(10):
            baseGlyph = baseFonts['glyf'][base_fonts[j]]
            if onlineGlyph == baseGlyph:
                temp['&#x' + uni_list[i][3:].lower()] = base_nums[j]
    print('uni_list', len(uni_list[0]), uni_list[0])
    """
    baseGlyphName_number = {
            'uniE6EC': '5', 'uniEB3E': '3',
            'uniF538': '0', 'uniEC6C': '2',
            'uniEB22': '7', 'uniF72B': '6',
            'uniE1FC': '4', 'uniF1F8': '1',
            'uniF63B': '9', 'uniE19E': '8'
            }
    print('uni' + '%X' % ord('\uec73'))
    print(onlineFonts.getGlyphNames())

    def transform_single_enc(enc):
        onlineForm = onlineFonts['glyf']['uni' + '%X' % ord(enc)]
        print('onlineForm', onlineForm)
        for name, num in baseGlyphName_number.items():
            if onlineForm == baseFonts['glyf'][name]:
                return num

    result = []
    for each in encrypt_number:
        result.append(''.join(transform_single_enc(c) if ord(c) > 256 else c for c in each))
    
    print(result)
    """
    print({a: b for a, b in zip(base_fonts, base_nums)})
    print(baseFonts.getGlyphNames())
    print(onlineFonts.getGlyphNames())
    glyph = onlineFonts.getGlyphName(ord('\uec73'))
    print(glyph)
    numid = baseFonts.getGlyphID(glyph)
    print(hex(numid))
    """

    """
    results = []
    for encrypt_num in encrypt_number:
        point_pos = encrypt_num.find('.')
        point_pos = point_pos + 1
        print('the position of the point:',point_pos)
        encrypt_num = encrypt_num.replace('.', '')

        numbers = encrypt_num.split('\\')
        print(numbers, len(numbers))
        for i in range(0, len(numbers)):
            numbers[i] = numbers[i][-4:]
            numbers[i] = temp[numbers[i]]

        numbers.insert(point_pos, '.')
        results.append(int(numbers.join('')))

        print(temp)
        for each in encrypt_num:
            numbers = [temp[char] for char in each.split('.')]

    return results
            """


if __name__ == '__main__':
    main()
