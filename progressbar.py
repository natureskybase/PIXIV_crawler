import time

size = 0
content_size = 100
for i in range(10):
    size += 10
    time.sleep(1)
    print('\r', '[下载进度]:%s%.2f%%' % ('>'*int(size/10), float(size/content_size *100)), end=' ')
