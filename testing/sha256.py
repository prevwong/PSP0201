import hashlib

hash_obj = hashlib.sha256("hello World".encode())
print hash_obj
hash_obj = hash_obj.hexdigest()
print hash_obj

print "haha".encode()
