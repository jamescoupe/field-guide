from PIL import Image
from PIL import ImageFont, ImageDraw
import subprocess, os, shutil, random
filepath = "/Users/jamescoupe/fieldGuide/"
fontPath_reg = "/Library/Fonts/OldNewspaperTypes.ttf"
bird_images = ["b2i_1.png", "b2i_2.png", "b2i_3.png", "b2i_4.png"]
birds = ["Marx Crescent", "Squawking Engels", "Factory Girl"]

sans36  =  ImageFont.truetype ( fontPath_reg, 36 )
sans30  =  ImageFont.truetype ( fontPath_reg, 30 )
sans20  =  ImageFont.truetype ( fontPath_reg, 20 )

w = 1275
h = 1650

def wrap_text(txt, font, max_width):
    lines = []
    if font.getsize(txt)[0]  <= max_width:
            lines.append(txt)
    else:
        words = txt.split()
        i = 0
        cap_flag = False
        while i < len(words):
            line = ''
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                #print(lines)
                if words[i].isupper():
                    if cap_flag==False:
                        #print("adding line")
                        lines.append(' ')
                        cap_flag = True
                        if i > 0:
                            #print("adding line")
                            #print(lines)
                            #lines.append(' ')
                            break
                else:
                    cap_flag = False
                line = line + words[i]+ " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)
    return(lines)

def reSize(imFile, newFile, basewidth):
    im = Image.open(imFile)
    old_size = im.size
    wpercent = (basewidth/float(im.size[0]))
    hsize = int((float(im.size[1])*float(wpercent)))
    img = im.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(newFile)
    return hsize

def make_title(pg_num, title_para, txt_in, title, family, latin, bird_pic, filename):
    intro = "The following is an enumeration of the genera and species more usually imported :- "
    if pg_num%2 != 0:
        colonies = ["INDIA.", "AFRICA.", "AUSTRALIA.", "BRITAIN."]
        txt1="THE BIRDS OF "+ random.choice(colonies)
    else:
        txt1 = "BIRDS OF THE BRITISH EMPIRE."
    txt2=str(pg_num)
    reSize_path = filepath+bird_pic.replace(".png", "_resized.png")
    im1 = Image.open(reSize_path, 'r')
    rgb = (im1.getpixel((1,1)))
    im  =  Image.new ( "RGB", (w,h), rgb )
    draw = ImageDraw.Draw(im)
    t1 = draw.textsize(txt1, font=sans30)
    t1_pos = w/2-t1[0]/2
    draw.text((t1_pos,70), txt1, font=sans30, fill="black")
    if pg_num%2 != 0:
        draw.text((w-180,70), txt2, font=sans30, fill="black")
    else:
        draw.text((120, 70), txt2, font=sans30, fill="black")
    t2 = draw.textsize(title, font=sans36)
    t2_pos = w/2-t2[0]/2
    draw.text((t2_pos,220), title, font=sans36, fill="black")
    lines = wrap_text(title_para, sans30, (w-180)-120)
    v_dist = 320
    for line in lines:
        draw.text((120,v_dist), line, font=sans30, fill="black")
        v_dist += 40
    lines = wrap_text(intro, sans30, (w-180)-120)
    v_dist += 60
    for line in lines:
        draw.text((120,v_dist), line, font=sans30, fill="black")
        v_dist += 40
    v_dist += 60
    draw.text((160,v_dist), "Family - " + family, font=sans30, fill="black")
    v_dist+= 60
    draw.text((160,v_dist), "Genus - ", font=sans30, fill="black")
    i = 1
    v_dist+= 60
    for name in latin:
        phrase = str(i)+'.  '+latin[name].split()[0]+'.'
        draw.text((160,v_dist), phrase, font=sans30, fill="black")
        phrase = latin[name].split()[0][0]+'.'
        draw.text((440,v_dist), phrase, font=sans30, fill="black")
        phrase = ' '.join(latin[name].split()[1:]) + "."
        draw.text((480,v_dist), phrase, font=sans30, fill="black")
        draw.text((800,v_dist), name+'.', font=sans30, fill="black")
        i+=1
        v_dist+= 40
    lines = wrap_text(txt_in, sans30, (w-180)-120)
    v_dist += 80
    upper = v_dist
    lower = h-180
    num_lines = int((lower-upper)/40)
    for line in lines[:num_lines]:
        draw.text((120,v_dist), line, font=sans30, fill="black")
        v_dist += 40 
        
    im.save(filepath+filename)
    return lines[num_lines:]

def make_page1(pg_num, txt_in, bird_name, bird_pic, filename):
    if pg_num%2 != 0:
        colonies = ["INDIA.", "AFRICA.", "AUSTRALIA.", "BRITAIN."]
        txt1="THE BIRDS OF "+ random.choice(colonies)
    else:
        txt1 = "BIRDS OF THE BRITISH EMPIRE."
    txt2=str(pg_num)
    txt4 = "FIG. "+str(random.randint(1,100))+" - "+bird_name
    reSize_path = filepath+bird_pic.replace(".png", "_resized.png")
    bw = (w-240)-180
    img_h = reSize(filepath+bird_pic, reSize_path, bw)
    im1 = Image.open(reSize_path, 'r')
    rgb = (im1.getpixel((1,1)))
    im  =  Image.new ( "RGB", (w,h), rgb )
    draw = ImageDraw.Draw(im)
    t1 = draw.textsize(txt1, font=sans30)
    t1_pos = w/2-t1[0]/2
    draw.text((t1_pos,70), txt1, font=sans30, fill="black")
    if pg_num%2 != 0:
        draw.text((w-180,70), txt2, font=sans30, fill="black")
    else:
        draw.text((120, 70), txt2, font=sans30, fill="black")
    #lines = wrap_text(txt_in, sans30, (w-180)-120)
    v_dist = 180
    v_center = h/2-img_h/2
    line_h = sans30.getsize("test")
    upper = 180
    lower = v_center
    num_lines = int((lower-upper)/40)
    using_rem = True
    if len(txt_in) < num_lines:
        using_rem = False
        diff = num_lines-len(txt_in)
        for line in txt_in:
            draw.text((120,v_dist), line, font=sans30, fill="black")
            v_dist += 40
        txt_in = txt_inputs.pop(0)
        lines = wrap_text(txt_in, sans30, (w-180)-120)
        for line in lines[:diff]:
            draw.text((120,v_dist), line, font=sans30, fill="black")
            v_dist += 40
    elif len(txt_in) >= num_lines:
        print(2)
        #print(txt_in)
        for line in txt_in[:num_lines]:
            draw.text((120,v_dist), line, font=sans30, fill="black")
            v_dist += 40                
    v_dist = v_dist+20
    im.paste(im1, (180, int(v_center)))
    t4 = draw.textsize(txt4, font=sans20)
    t4_pos = w/2-t4[0]/2
    v_dist = v_dist+img_h
    caption_h = h/2+img_h/2+10
    draw.text((t4_pos,caption_h), txt4, font=sans20, fill="black")
    upper = v_dist + 20
    lower = h-180
    num_lines2 = int((lower-upper)/40)
    v_dist = v_dist+50
    if using_rem:
        if len(txt_in[num_lines:]) < num_lines2:
            using_rem = False
            print(3)
            diff = num_lines2-len(txt_in[num_lines:])
            for line in txt_in[num_lines:]:
                draw.text((120,v_dist), line, font=sans30, fill="black")
                v_dist += 40
            if len(txt_inputs) > 0:
                txt_in = txt_inputs.pop(0)
            else:
                print('exit')
                im.save(filepath+filename)
                return []
            lines = wrap_text(txt_in, sans30, (w-180)-120)
            for line in lines[:diff]:
                draw.text((120,v_dist), line, font=sans30, fill="black")
                v_dist += 40
            lines = lines[diff:]
        elif len(txt_in[num_lines:]) >= num_lines2:
            print(4)
            #print(txt_in)
            for line in txt_in[num_lines:]:
                draw.text((120,v_dist), line, font=sans30, fill="black")
                v_dist += 40
            lines = txt_in[num_lines:]
    else:
        print(5)
        for line in lines[diff:diff+num_lines2]:
            draw.text((120,v_dist), line, font=sans30, fill="black")
            v_dist += 40
        lines = lines[diff+num_lines2:]
    im.save(filepath+filename)
    return lines

def make_page2(pg_num, txt_in, bird_name, bird_pic, filename):
    if pg_num%2 != 0:
        colonies = ["INDIA.", "AFRICA.", "AUSTRALIA.", "BRITAIN."]
        txt1="THE BIRDS OF "+ random.choice(colonies)
    else:
        txt1 = "BIRDS OF THE BRITISH EMPIRE."
    txt2=str(pg_num)
    txt4 = "FIG. "+str(random.randint(1,100))+" - "+bird_name
    reSize_path = filepath+bird_pic.replace(".png", "_resized.png")
    bw = 480
    img_h = reSize(filepath+bird_pic, reSize_path, bw)
    im1 = Image.open(reSize_path, 'r')
    rgb = (im1.getpixel((1,1)))
    im  =  Image.new ( "RGB", (w,h), rgb )
    draw = ImageDraw.Draw(im)
    t1 = draw.textsize(txt1, font=sans30)
    t1_pos = w/2-t1[0]/2
    draw.text((t1_pos,70), txt1, font=sans30, fill="black")
    if pg_num%2 != 0:
        draw.text((w-180,70), txt2, font=sans30, fill="black")
    else:
        draw.text((120, 70), txt2, font=sans30, fill="black")

    
    #lines = wrap_text(txt_in, sans30, (w-180)-120)
    v_dist = 180
    v_center = h/2-img_h/2
    line_h = sans30.getsize("test")
    upper = 180
    lower = v_center
    num_lines = int((lower-upper)/40)
    using_rem = True
    if len(txt_in) < num_lines:
        print('a')
        using_rem = False
        diff = num_lines-len(txt_in)
        for line in txt_in:
            draw.text((120,v_dist), line, font=sans30, fill="black")
            v_dist += 40
        if len(txt_inputs) > 0:
            txt_in = txt_inputs.pop(0)
        else:
            im.save(filepath+filename)
            return []
        #print(txt_in)
        lines = wrap_text(txt_in, sans30, (w-180)-120)
        for line in lines[:diff]:
            draw.text((120,v_dist), line, font=sans30, fill="black")
            v_dist += 40
    elif len(txt_in) >= num_lines:
        print('b')
        for line in txt_in[:num_lines]:
            draw.text((120,v_dist), line, font=sans30, fill="black")
            v_dist += 40 
    im.paste(im1, (120, int(v_center)))
    t4 = draw.textsize(txt4, font=sans20)
    t4_pos = bw/2-t4[0]/2 + 120
    t4_h = h/2+img_h/2+10
    draw.text((t4_pos,t4_h), txt4, font=sans20, fill="black")
    upper = v_dist
    lower = t4_h+60
    num_lines2 = int((lower-upper)/40)
    if using_rem:
        #print(txt_in[)
        txt_remainder = ' '.join(txt_in[num_lines:])
        #print(txt_remainder)
        lines = wrap_text(txt_remainder, sans30, 490)
        if len(lines) < num_lines2:
            using_rem = False
            diff = num_lines2-len(lines)
            for line in lines:
                draw.text((620,v_dist), line, font=sans30, fill="black")
                v_dist += 40
            txt_in = txt_inputs.pop(0)
            lines = wrap_text(txt_in, sans30, 490)
            for line in lines[:diff]:
                draw.text((620,v_dist), line, font=sans30, fill="black")
                v_dist += 40
            lines = lines[diff:]
        elif len(lines) >= num_lines2:
            print(3)
            for line in lines[:num_lines2]:
                draw.text((620,v_dist), line, font=sans30, fill="black")
                v_dist += 40
            lines = lines[num_lines2:]
    else:
        txt_remainder = ' '.join(lines[diff:])
        lines = wrap_text(txt_remainder, sans30, 490)
        for line in lines[:num_lines2]:
            draw.text((620,v_dist), line, font=sans30, fill="black")
            v_dist += 40
        lines = lines[num_lines2:]

    txt_remainder = ' '.join(lines)
    lines = wrap_text(txt_remainder, sans30, (w-180)-120)
    upper = v_dist
    lower = h-180
    num_lines3 = int((lower-upper)/40)
    for line in lines[:num_lines3]:
        draw.text((120,v_dist), line, font=sans30, fill="black")
        v_dist += 40
    if len(txt_inputs) > 0:
        txt_in = txt_inputs.pop(0)
        lines = wrap_text(txt_in, sans30, (w-180)-120)
        upper = v_dist
        lower = h-180
        num_lines4 = int((lower-upper)/40)
        for line in lines[:num_lines4]:
            draw.text((120,v_dist), line, font=sans30, fill="black")
            v_dist += 40
        lines = lines[num_lines4:]
    else:
        lines = []
    im.save(filepath+filename)
    return lines

def make_page3(pg_num, txt_in, bird_name, bird_pic, filename):
    if pg_num%2 != 0:
        colonies = ["INDIA.", "AFRICA.", "AUSTRALIA.", "BRITAIN."]
        txt1="THE BIRDS OF "+ random.choice(colonies)
    else:
        txt1 = "BIRDS OF THE BRITISH EMPIRE."
    txt2=str(pg_num)
    txt4 = "FIG. "+str(random.randint(1,100))+" - "+bird_name
    reSize_path = filepath+bird_pic.replace(".png", "_resized.png")
    bw = 480
    img_h = reSize(filepath+bird_pic, reSize_path, bw)
    im1 = Image.open(reSize_path, 'r')
    rgb = (im1.getpixel((1,1)))
    im  =  Image.new ( "RGB", (w,h), rgb )
    draw = ImageDraw.Draw(im)
    t1 = draw.textsize(txt1, font=sans30)
    t1_pos = w/2-t1[0]/2
    draw.text((t1_pos,70), txt1, font=sans30, fill="black")
    if pg_num%2 != 0:
        draw.text((w-180,70), txt2, font=sans30, fill="black")
    else:
        draw.text((120, 70), txt2, font=sans30, fill="black")
    lines = wrap_text(txt_in, sans30, (w-180)-120)
    v_dist = 180
    v_center = h/2-img_h/2
    line_h = sans30.getsize("test")
    upper = 180
    lower = v_center
    num_lines = int((lower-upper)/40)
    for line in lines[:num_lines]:
        draw.text((120,v_dist), line, font=sans30, fill="black")
        v_dist += 40
    im.paste(im1, (620, int(v_center)))
    t4 = draw.textsize(txt4, font=sans20)
    t4_pos = bw/2-t4[0]/2 + 620
    t4_h = h/2+img_h/2+20
    draw.text((t4_pos,t4_h), txt4, font=sans20, fill="black")
    txt_remainder = ' '.join(lines[num_lines:])
    lines = wrap_text(txt_remainder, sans30, 490)
    upper = v_dist
    lower = t4_h+60
    num_lines2 = int((lower-upper)/40)
    for line in lines[:num_lines2]:
        draw.text((120,v_dist), line, font=sans30, fill="black")
        v_dist += 40
    txt_remainder = ' '.join(lines[num_lines2:])
    lines = wrap_text(txt_remainder, sans30, (w-180)-120)
    upper = v_dist
    lower = h-180
    num_lines3 = int((lower-upper)/40)
    for line in lines[:num_lines3]:
        draw.text((120,v_dist), line, font=sans30, fill="black")
        v_dist += 40
    im.save(filepath+filename)

txt_input = "PLEASURE GARDENS are those where the birds take possession of whatever they can find, and where they may find an \
abundance of insects, small birds, and. in the case of the emu, avifauna. For instance, it has been found in a pleasure garden in one \
of our large towns, and in a field in the country have I'ellows nest. In the case of the winter visitors from the north, the nest is \
often placed in a field by the side of the stream, which, of course, is no more than forty yards distant, and from there it is only a \
short step to the sea. In such a place the eggs are two or three in number, often laid on alternate days, and the young run about \
soon after being hatched. In such a situation the strong will survive, but the weaker soon get out of hand. It is not known to breed \
in confinement, but the practice is well-known, and there is no reason why it shouldn't take place in the most unfriendly circumstances. \
THE NUT-HATCH. Another small bird that might be heard of at the Grape or Fruit trees is the nut-hatcher, or rather nut-Hatch, as it is \
also called. It is to a height of seven or eight feet, and is planted with .slime, grass, and water. The eggs are four or five in \
number, pinky wdiite with purplish spots. It is to be fed on the same diet as the greenfinch, and it is to be seen, and not heard of, \
for it is thought to be very foolish. It has bred in confinement. The greenfinch lays from three to live greenish yellow eggs, with \
black spots and grey edging. It is a poor flyer, but does well in the cage, where it has bred. It is a pity it has not bred in more \
natural surroundings ; for it is very danoying in its preferences, and very active and variable in its movements. It should have its \
beaks and tail cut off at the commencement of April, and its head and breast lain open to the nape ; the eggs are white, with pale \
purplish spots and blotches."

ip = "If there is one thing that the industrialists and landowners of this country can learn from the \
habits and customs of the peasantry it is that they should pay more attention to the needs of the agriculturist and less to the \
plasters and bugbears of the night, and they will soon see that the changes that are being made in their midst are for the better."

mc = "MARX CRESCENT. — Crowned with a bluish grey shade, this is the 'common' columbarium in Britain, but it can vary a good deal in \
colour. The head is white, with two black streaks on the crown ; the face, neck, and breast are black ; a black line, rising from the \
lower part of the abdomen, crosses the neck and reaches to the back of the neck ; the remaining upper parts are whitish grey, except \
the under tail coverts, which are grey. The bill is black, the eyes hazel, and the legs and feet grey. The female is smaller than the \
male, and her plumage is less vivid in all but the most marked contrast. In the winter it tends to be rather spotted than co- radiate. \
The nest is large and made of sticks, but it varies in make and quality. It is frequently placed in a low bush, but it is not in the \
habit of coming near a bush when it is convenient, but it does not seem to mind when it comes near a tree, though it does suffer a \
knock on the lower part of the breast when it does."

se = "SQUAWKING ENGELS. — These birds are very numerous, and are more numerous than is commonly supposed, rent or confiscated, as a \
punishment for crime, or out of cruelty to the weak. They can be kept pretty well in confinement, and if properly fed and treated, \
they may be useful creatures. They are monogamous in a state of nature, but become polygamous, and sometimes both, as a rule, in the \
state of nature. There is no doubt that this is the natural state of most birds kept in confinement, but that those, especially the \
ducks and hispanic water, which are so seldom converted into egg cases, are in the habit of occasionally being so, and it is certainly \
a mistake to destroy them when the season is over, for they never defile a cage or aviary, and never, in the opinion of many \
aviculturists, ever become so tame as to come to such a sign of irritation as to occasion a murder. There is no doubt that they are \
occasionally converted, and that in such a case the murder is committed by the owner or keeper, under the pretence of 'defending his \
duck,' or 'defending his chicken,' or some variation of such nonsense."

fg = "FACTORY GIRL. — An extremely pretty little creature, whose beautiful face and silky figure have been greatly magnified by the \
addition of a crest which almost obscures her iris. The upper parts are grey, but growing into a bluish grey are the long feathers of \
the tail, which are black, capped with white. The lower parts are grey, mottled with brown, and reaching to the middle of the breast \
are the iridescent hues of the seven china shades ; the under surface is white ; the bill is greyish black, and the legs and feet \
greyish black. The female is indistinguishable outwardly from her mate. These birds feed on other insects of the fields and gardens, \
and sometimes on the tops of tall trees. They are very shy and wary, and few of them venture to approach a house in the open. The \
nests are usually built in low cover, and the eggs are usually three in number. The young are easily brought up from the nest on \
bread and milk, and they should be protected from hunger and cold."

txt_inputs = [mc, se, fg]
title_input = "THE INDUSTRIAL PROLETARIAT."
family = "Ploceidae."
# add google translate api call
latin_names = {"Marx Crescent":"Lunata nusquam marx", "Squawking Engels":"Latijn ceteros ciens vadit", "Factory Girl":"Puella factory"}

random.shuffle(bird_images)

def make_pages(start):    
    rem = make_title(start, ip, txt_inputs.pop(0), title_input, family, latin_names, bird_images[0], "page0.png")
    #print(rem)
    rem2 = make_page1(start+1, rem, "Marx Crescent", bird_images.pop(), "page1.png")
    rem3 = make_page2(start+2, rem2, "Squawking Engels", bird_images.pop(), "page2.png")
    if len(rem3) > 0:
        print("pg3")
        make_page1(start+3, rem3, "Factory Girl", bird_images.pop(), "page3.png")

make_pages(300)
#print(txt_inputs)
