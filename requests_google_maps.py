import requests
import time
import csv
import pandas as pd
from stem.control import Controller
from fake_useragent import UserAgent

# Cấu hình proxy SOCKS5 cho Tor
proxies = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

# API Key của Google Places API (thay bằng API Key của bạn)
API_KEY = "YOUR_GOOGLE_PLACES_API_KEY"

# Tìm kiếm doanh nghiệp trong khu vực cụ thể
def search_google_places(location, radius=5000, keyword="công ty"):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&keyword={keyword}&key={API_KEY}"
    headers = {"User-Agent": UserAgent().random}
    
    response = requests.get(url, headers=headers, proxies=proxies)
    data = response.json()
    
    if "results" in data:
        return data["results"]
    return []

# Lấy số điện thoại từ chi tiết doanh nghiệp
def get_phone_number(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_phone_number,formatted_address&key={API_KEY}"
    headers = {"User-Agent": UserAgent().random}

    response = requests.get(url, headers=headers, proxies=proxies)
    data = response.json()
    
    if "result" in data:
        return {
            "name": data["result"].get("name", "Không có tên"),
            "phone": data["result"].get("formatted_phone_number", "Không có số điện thoại"),
            "address": data["result"].get("formatted_address", "Không có địa chỉ"),
        }
    return None

# Đổi IP bằng Tor sau mỗi request
def new_tor_identity():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()  # Không cần mật khẩu nếu đã chỉnh file torrc
        controller.signal(2)  # Gửi lệnh NEWNYM để đổi IP
        print("✅ Đã đổi IP!")

# Tìm doanh nghiệp trong khu vực "Hải Phòng"
location = "20.8449,106.6881"  # Tọa độ Hải Phòng
businesses = search_google_places(location, keyword="nhà hàng")

# Lưu dữ liệu vào file CSV
csv_file = "business_data.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Tên Doanh Nghiệp", "Số Điện Thoại", "Địa Chỉ"])  # Header
    
    for index, business in enumerate(businesses):
        place_id = business["place_id"]
        details = get_phone_number(place_id)

        if details:
            writer.writerow([details["name"], details["phone"], details["address"]])
            print(f"🏢 {details['name']} - 📞 {details['phone']} - 📍 {details['address']}")

        # Đổi IP sau mỗi 3 request để tránh bị chặn
        if index % 3 == 0:
            new_tor_identity()
            time.sleep(5)  # Đợi 5s để Tor cập nhật IP mới

print(f"✅ Đã lưu dữ liệu vào {csv_file}")

# Chuyển CSV sang Excel (nếu cần)
df = pd.read_csv(csv_file)
df.to_excel("business_data.xlsx", index=False)
print("✅ Đã lưu dữ liệu vào business_data.xlsx")