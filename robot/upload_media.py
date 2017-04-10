from robot import client


first = open('music/1.mp3', 'r')
second = open('music/2.mp3', 'r')

r1 = client.upload_permanent_media('voice', first)
r2 = client.upload_permanent_media('voice', second)

print r1
print r2

