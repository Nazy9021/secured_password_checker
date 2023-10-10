import requests
import hashlib
import sys


def api_data(query):
  url = 'https://api.pwnedpasswords.com/range/' + query
  resp = requests.get(url)
  if resp.status_code != 200:
  	raise RuntimeError(f'Error fetching:{resp.status_code}, check the api and try again')
  return resp


def password_leak_count(hashes, hash_check):
	hashes = (line.split(':') for line in hashes.text.splitlines())
	for h, count in hashes:
	  if h == hash_check:
	  	return count
	return 0 



def check_pwned_api(pswd):
  k = hashlib.sha1(pswd.encode('utf-8')).hexdigest().upper()
  first,tail = k[:5],k[5:]
  res = api_data(first)
 
  # print(res)
  return password_leak_count(res, tail)


def main(argv):
	for pswd in argv:
		count = check_pwned_api(pswd)
		if count:
			print(f'{pswd} was found {count} times... you should change your password')
		else:
			print(f'{pswd} was not found.. carry on!')
	return "done"

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))


  