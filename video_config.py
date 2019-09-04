# -*- coding: utf-8 -*-
# main parameter
folder = "cache/"
output_file = "video_config.txt"

f = open(output_file, "w")

def write_picture(n, d):
    f.write("file '" + folder + n + "'\n")
    f.write("duration " + str(d) + "\n")

# cover
write_picture("cover_f.png", 5)
# pickup
write_picture("pickup.png", 15)
# comments
for i in range(15):
    write_picture("comment" + str(i+1) + ".png", 10)

f.close()