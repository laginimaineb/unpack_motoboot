import sys, struct, os

HEADER_SIZE = 1024
BLOCK_SIZE = 512
DWORD_SIZE = struct.calcsize("I")
IMAGE_NAME_LEN = 24

def read_dword(f):
	return struct.unpack("<I", f.read(DWORD_SIZE))[0]

def main():
	
	#Reading the arguments
	if len(sys.argv) != 3:
		print "USAGE: %s <MOTOBOOT_IMAGE> <UNPACK_DIR>" % sys.argv[0]
		return
	script_name, motoboot_path, unpack_dir = sys.argv

	#Reading the header
	motoboot_file = open(motoboot_path, "rb")
	num_images = read_dword(motoboot_file)
	images = []
	for i in range(0, num_images):
		image_name = motoboot_file.read(IMAGE_NAME_LEN).rstrip("\x00")
		start_off = read_dword(motoboot_file) * BLOCK_SIZE + HEADER_SIZE
		end_off = (read_dword(motoboot_file) + 1) * BLOCK_SIZE + HEADER_SIZE - 1
		print "[+] Detected image: %s [0x%08X - 0x%08X]" % (image_name, start_off, end_off)
		images.append((image_name, start_off, end_off))

	#Dumping each image
	for (image_name, start_off, end_off) in images:
		print "[+] Dumping image: %s" % image_name
		motoboot_file.seek(start_off, os.SEEK_SET)
		image_file = open(os.path.join(unpack_dir, image_name), "wb")
		image_file.write(motoboot_file.read(end_off - start_off + 1))
		image_file.close()

	motoboot_file.close()

if __name__ == "__main__":
	main()
