import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import concurrent.futures
import argparse
from bs4 import BeautifulSoup
from colorama import init , Style, Back,Fore

parser = argparse.ArgumentParser(description="Check Fraud Ips")

parser.add_argument('-s','--single_ip',
                            help = "Single IP address",
                            type = str,
                            required = False)

parser.add_argument('-l','--list',
                            help = "list of IP",
                            type = str,
                            required = False)

args = parser.parse_args()


def IpCheck(_Ip_):

	headers = {
	'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
	}

	try:

		req = requests.get("https://scamalytics.com/ip/{}".format(_Ip_), headers=headers)
		
		soup = BeautifulSoup(req.content, 'html.parser')
		divs = soup.find_all("div", {"class": "score"})
		for div in divs:
			div2 = div.text
			div1 = div.text
			div2 = div2.split(":")
			score = div2[1]
			score = int(score)
			if score >= 50:
				print("[+] IP Adress: {}".format(_Ip_)+Style.BRIGHT+Fore.RED+" "+div1+Style.RESET_ALL)
				if args.list:
					outfile.write(_Ip_+"\n")
				
			if  50 > score > 25:
				print("[+] IP Adress: {}".format(_Ip_)+Style.BRIGHT+Fore.YELLOW+" "+div1+Style.RESET_ALL)
				if args.list:
					outfile2.write(_Ip_+"\n")

			
			if score <= 25:
				print("[+] IP Adress: {}".format(_Ip_)+Style.BRIGHT+Fore.GREEN+" "+div1+Style.RESET_ALL)
				if args.list:
					outfile3.write(_Ip_+"\n")
		
		if args.single_ip:
			print("--------------------------------")
			ipinfo = requests.get("http://ipinfo.io/{}".format(_Ip_))
			print(ipinfo.text)
			print("--------------------------------")

	except Exception as e:
		print(e)

if __name__ == '__main__':

	if args.single_ip:
		IpCheck(args.single_ip)

	if args.list:
		ips = []
		outfile = open("riskabove_50_ip.txt", "w")
		outfile2 = open("riskbelow_50_25_ip.txt", "w")
		outfile3 = open("riskbelow_25_ip.txt", "w")
		f = open(args.list, "r")

		for ip in f:
			ip = ip.strip()
			ips.append(ip)

		with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
			executor.map(IpCheck, ips)

		f.close()
		outfile.close()
		outfile2.close()
		outfile3.close()

		print("\n[+] OutFiles created \n 1. riskabove_50_ip.txt \n 2. riskbelow_50_25_ip.txt \n 3. riskbelow_25_ip.txt")
