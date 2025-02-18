import requests
import csv

API_KEY = "YOUR_API_KEY"  # Thay bằng API Key của bạn
LOCATION_NAME = "huyện Dương Kinh, Hải Phòng"  # Đổi thành tên khu vực bạn muốn tìm
RADIUS = 5000  # Phạm vi tìm kiếm (đơn vị: mét)
TYPE = "restaurant"  # Loại địa điểm (có thể đổi: hospital, cafe, shop...)

# Bước 1: Lấy tọa độ của khu vực
geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={LOCATION_NAME}&key={API_KEY}"
geo_response = requests.get(geocode_url).json()

if geo_response["status"] == "OK":
    location = geo_response["results"][0]["geometry"]["location"]
    lat, lng = location["lat"], location["lng"]
    print(f"Tọa độ của {LOCATION_NAME}: {lat}, {lng}")
else:
    print("Không tìm thấy tọa độ của khu vực.")
    exit()

# Bước 2: Tìm địa điểm xung quanh khu vực đó
search_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={RADIUS}&type={TYPE}&key={API_KEY}"
places_response = requests.get(search_url).json()
places = places_response.get("results", [])

# Bước 3: Lấy số điện thoại và lưu vào file CSV
with open("google_maps_phones.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Tên địa điểm", "Số điện thoại", "Địa chỉ"])

    for place in places:
        place_id = place["place_id"]
        details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_phone_number,formatted_address&key={API_KEY}"
        details_response = requests.get(details_url).json()
        details = details_response.get("result", {})

        name = details.get("name", "N/A")
        phone = details.get("formatted_phone_number", "Không có số")
        address = details.get("formatted_address", "Không có địa chỉ")

        print(f"{name} - {phone} - {address}")
        writer.writerow([name, phone, address])  # Ghi vào file CSV

print("Dữ liệu đã được  lưu vào google_maps_phones.csv")