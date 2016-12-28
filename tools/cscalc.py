#Checksum calculator
# import into python CLI to create checksum and test them

def calc(cmd):
    cb1 = 0xaa
    cb2 = 0x0
    for byte in cmd:
        cb1 = (cb1 + byte)%255
        cb2 = (cb2 + cb1)%255
    mscb = 255 - ((cb1+cb2)%255)
    lscb = 255 - ((cb1+mscb)%255)
    print '{0:02x} {1:02x}'.format(mscb,lscb)

def decode(cmd):
    cb1 = 0xaa
    cb2 = 0x0
    for byte in cmd:
        cb1 = (cb1 + byte)%255
        cb2 = (cb2 + cb1)%255
    if ((cb1 == 0) and (cb2==0)):
        print(1)
    else:
        print(0)

# Test code

x = [0x08,0x01,0x00,0x02,0x07,0x40]
calc(x)

y = x + [0x79,0x89]

decode(y)

y = x + [4,3]

decode(y)


    


    



