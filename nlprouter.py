import os
import sys
import json

import dotenv


dotenv.load_dotenv(os.path.realpath('./.env'))

def main():
  _, payload = sys.argv()
  payload = json.loads(payload)

if __name__ == "__main__":
  main()
  