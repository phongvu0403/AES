from PIL import Image 
from Crypto.Cipher import AES 
    
filename = "test_encrypted ecb.BMP" 
filename1 = "test_encrypted cbc.BMP"
filename_out = "test_decrypted ecb"
filename_out1 = "test_decrypted cbc" 
format = "BMP" 
key = "aaaabbbbccccdddd" 
    
# AES requires that plaintexts be a multiple of 16, so we have to pad the data 
def pad(data): 
    return data + b"\x00"*(16-len(data)%16)  
    
# Maps the RGB  
def convert_to_RGB(data): 
    r, g, b = tuple(map(lambda d: [data[i] for i in range(0,len(data)) if i % 3 == d], [0, 1, 2])) 
    pixels = tuple(zip(r,g,b)) 
    return pixels 
        
def process_image_ecb_mode(filename): 
    # Opens image and converts it to RGB format for PIL 
    im = Image.open(filename) 
    data = im.convert("RGB").tobytes()  
    
    # Since we will pad the data to satisfy AES's multiple-of-16 requirement, we will store the original data length and "unpad" it later. 
    original = len(data)  
    
    # Encrypts using desired AES mode (we'll set it to ECB by default) 
    new = convert_to_RGB(aes_ecb_decrypt(key, pad(data))[:original])  
        
    # Create a new PIL Image object and save the old image data into the new image. 
    im2 = Image.new(im.mode, im.size) 
    im2.putdata(new) 
        
    #Save image 
    im2.save(filename_out+"."+format, format)
     
# ECB 
def aes_ecb_decrypt(key, data, mode=AES.MODE_ECB): 
    aes = AES.new(key, mode) 
    new_data = aes.decrypt(data) 
    return new_data 
    
process_image_ecb_mode(filename) 

def process_image_cbc_mode(filename): 
    # Opens image and converts it to RGB format for PIL 
    im = Image.open(filename) 
    data = im.convert("RGB").tobytes()  
    
    # Since we will pad the data to satisfy AES's multiple-of-16 requirement, we will store the original data length and "unpad" it later. 
    original = len(data)  
    
    # Encrypts using desired AES mode (we'll set it to ECB by default) 
    new = convert_to_RGB(aes_cbc_decrypt(key, pad(data))[:original])  
        
    # Create a new PIL Image object and save the old image data into the new image. 
    im2 = Image.new(im.mode, im.size) 
    im2.putdata(new) 
        
    #Save image 
    im2.save(filename_out1+"."+format, format) 
    
# CBC 
def aes_cbc_decrypt(key, data, mode=AES.MODE_CBC): 
    IV = "A"*16  #We'll manually set the initialization vector to simplify things 
    aes = AES.new(key, mode, IV) 
    new_data = aes.decrypt(data) 
    return new_data 

process_image_cbc_mode(filename1)