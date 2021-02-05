import os

try:
    os.mkdir("Data")
except FileExistsError:
    print('"Data" 디렉토리가 존재합니다, 생성단계를 건너뜁니다.')
try:
    os.mkdir("Token")
except FileExistsError:
    print('"Token" 디렉토리가 존재합니다, 생성단계를 건너뜁니다.')

with open("Token/Token", "w", encoding="utf-8") as File:
    File.write(input("봇 토큰을 입력해주십시오. \n> "))
