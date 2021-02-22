from passlib.hash import sha256_crypt
import os

ALLOWED_EXTENSIONS = {'jpg'}
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')

class Encryption:
  LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  def encrypt(key, message):
      return Encryption.translate(key, message, 'encrypt')
  def decrypt(key, message):
      return Encryption.translate(key, message, 'decrypt')
  def translate(key, message, mode):
      translated = [] # stores the encrypted/decrypted message string
      keyIndex = 0
      key = key.upper()

      for symbol in message:
          num = Encryption.LETTERS.find(symbol.upper())
          if num != -1:
              if mode == 'encrypt':
                  num += Encryption.LETTERS.find(key[keyIndex])
              elif mode == 'decrypt':
                  num -= Encryption.LETTERS.find(key[keyIndex])
              num %= len(Encryption.LETTERS)

              if symbol.isupper():
                  translated.append(Encryption.LETTERS[num])
              elif symbol.islower():
                  translated.append(Encryption.LETTERS[num].lower())
                  keyIndex += 1

              if keyIndex == len(key):
                  keyIndex = 0
          else:
              translated.append(symbol)
      return ''.join(translated)

# check if the username and password from registration form is unique in all users
def is_unique(form,table):
    username = form.username.data
    encrypted_username = Encryption.encrypt(ENCRYPTION_KEY,username)
    password = form.password.data
    users = table.query.filter_by(encrypted_username=encrypted_username).all()
    for user in users:
        if user.username == username and sha256_crypt.verify(password,user.password):
            return False
    return True

#checks if there is a period in filename and it is in jpg format
#only allows images in jpg format    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
