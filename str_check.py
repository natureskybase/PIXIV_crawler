title = 'ホシノ（水着）/?\\|泳装星野 MMD渲染图'


def title_pro(title):
    appeared_forbidden_str = ['|', '/', '*', '<', '>', '?', ':', '\\', '：', '？']
    for str in appeared_forbidden_str:
        if (str in title):
            title_last = title.replace(str,"")
            title = title_pro(title_last)
        if(str_checking(title) == True):
            return title
        
def str_checking(str):
    appeared_forbidden_str = ['|', '/', '*', '<', '>', '?', ':', '\\', '：', '？']
    counter = 0
    for i in appeared_forbidden_str:
        counter += 1
        if(i in str):
            return False
        elif(counter == len(appeared_forbidden_str)):
            return True
    
print (title_pro(title))

