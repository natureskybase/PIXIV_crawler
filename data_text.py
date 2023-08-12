import re
import json
import jsonpath
from enum import Enum
# data = {'1':{'title':'牛逼','userid':'92'}, '3':{'title':'生产部','userid':'90'}, '2':{'title':'垃圾','userid':'29'}}

# data_main = [1,2,3]
# data2 = ['ss', 'll', 'jj']
# data3 = [89, 222, 1313]

# datadic = {}
# for key in range(len(data_main)):
#     for key1, key2 in zip(data2, data3):
#         datadic[f'{key}'] = {} 
#         datadic[f'{key}']['data2'] = key1
#         datadic[f'{key}']['data3'] = key2
# print(datadic)
# for key, value in dic.items():

# if('错误日志'in 'asafvn错误日志nsafa'):
#     print('yes')
# else:
#     print('no')

# with open('./data_integrated.json', 'r')as f:
#     data = json.load(f)

# with open('./log.txt', 'r', encoding='utf-8')as f:
#     lines = f.readlines()
#     line_last = lines[-1]
#     print(line_last)

# for i in data:
#     id = data[i]['id']
#     print(id)


class MyEnum(Enum):
    VALUE_1 = 'VALUE_1'
    VALUE_2 = 2
    VALUE_3 = 3

print (MyEnum.VALUE_1.name)
# class MyClass:
#     def __init__(self):
#         self.state = MyEnum.VALUE_1

#     def print_enum_value(self):
        
#         if self.state == MyEnum.VALUE_1:
#             print(self.state.value)
#             print(type(self.state.name))

# a =MyClass()
# a.print_enum_value()

# data={
#         "error": 'false',
#         "message": "",
#         "body": [
#             {
#                 "urls": {
#                     "thumb_mini": "https:\/\/i.pximg.net\/c\/128x128\/img-master\/img\/2023\/03\/07\/14\/23\/45\/105966110_p0_square1200.jpg",
#                     "small": "https:\/\/i.pximg.net\/c\/540x540_70\/img-master\/img\/2023\/03\/07\/14\/23\/45\/105966110_p0_master1200.jpg",
#                     "regular": "https:\/\/i.pximg.net\/img-master\/img\/2023\/03\/07\/14\/23\/45\/105966110_p0_master1200.jpg",
#                     "original": "https:\/\/i.pximg.net\/img-original\/img\/2023\/03\/07\/14\/23\/45\/105966110_p0.png"
#                 },
#                 "width": 1009,
#                 "height": 1160
#             },
#             {
#                 "urls": {
#                     "thumb_mini": "https:\/\/i.pximg.net\/c\/128x128\/img-master\/img\/2023\/03\/07\/14\/23\/45\/105966110_p1_square1200.jpg",
#                     "small": "https:\/\/i.pximg.net\/c\/540x540_70\/img-master\/img\/2023\/03\/07\/14\/23\/45\/105966110_p1_master1200.jpg",
#                     "regular": "https:\/\/i.pximg.net\/img-master\/img\/2023\/03\/07\/14\/23\/45\/105966110_p1_master1200.jpg",
#                     "original": "https:\/\/i.pximg.net\/img-original\/img\/2023\/03\/07\/14\/23\/45\/105966110_p1.png"
#                 },
#                 "width": 1024,
#                 "height": 1280
#             }
#         ]
#     }
# url = []
# url = jsonpath.jsonpath(data, '$..original')
# # for i in range(2):
# #     url.append(jsonpath.jsonpath(data, '$.body[?(@.i)].urls.original')[0])
# print (url)

