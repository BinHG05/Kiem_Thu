# Buổi 8 — Kiểm thử đăng nhập với Selenium, pytest và Page Object Model

## 1. Mô tả bài toán

Dự án tự động hóa kiểm thử trang đăng nhập của Văn phòng điện tử UTC:

<https://vanphongdientu.utc.edu.vn/Login>

Mục tiêu là kiểm tra các thành phần và luồng chính của trang Login bằng
Python, Selenium WebDriver, pytest và mô hình Page Object Model (POM).
Chrome chạy ở chế độ headless để test có thể chạy trên máy cá nhân hoặc môi
trường CI mà không cần mở cửa sổ trình duyệt.

Các test tương tác với website thật. Kết quả pass/fail phản ánh DOM, URL và
phản hồi thực tế của website tại thời điểm chạy.

## 2. Phạm vi kiểm thử

Bộ test hiện gồm 11 test case:

| Mã | Nội dung |
| --- | --- |
| TC01 | Trang Login mở được và form hiển thị |
| TC02 | Username và password rỗng khi mới mở trang |
| TC03 | Username nhận dữ liệu |
| TC04 | Password nhận dữ liệu |
| TC05 | Password sử dụng kiểu input được che ký tự |
| TC06 | Nút đăng nhập có nhãn đúng |
| TC07 | Checkbox “Giữ tôi luôn đăng nhập” tắt mặc định |
| TC08 | Có thể chọn checkbox “Giữ tôi luôn đăng nhập” |
| TC09 | Link quên mật khẩu trỏ đến trang khôi phục |
| TC10 | Link đăng nhập Google trỏ đến Google Accounts |
| TC11 | Đăng nhập thành công với thông tin xác thực hợp lệ |

TC11 cần tài khoản UTC thật. Nếu server vẫn giữ trình duyệt ở `/Login`, test
sẽ fail vì chưa chứng minh được đăng nhập thành công. Đây có thể là do tài
khoản, quyền truy cập hoặc phản hồi của hệ thống UTC.

## 3. Kiến trúc dự án

```text
tests/
├── conftest.py              # Fixture Chrome headless và Allure evidence
├── test_login.py            # Các test case và assertion
└── pages/
    ├── base_page.py         # WebDriverWait và helper dùng chung
    └── login_page.py        # URL, locator và nghiệp vụ Login
requirements.txt
README.md
```

Selector chỉ nằm trong Page Object. Test case chỉ gọi các thao tác nghiệp vụ
như mở trang, nhập dữ liệu, chọn checkbox và đăng nhập.

## 4. Công nghệ và yêu cầu môi trường

- Python 3.10 trở lên
- Google Chrome
- Selenium WebDriver
- pytest
- allure-pytest
- Allure Commandline để dựng giao diện báo cáo

Selenium Manager tự xử lý ChromeDriver khi chạy Selenium phiên bản hiện tại;
không cần tải `chromedriver.exe` thủ công.

## 5. Cài đặt dependency Python

Mở PowerShell tại thư mục dự án:

```powershell
cd "D:\Năm 4 - Kỳ 1\Kiểm Thử\Code"
python -m pip install -r requirements.txt
```

## 6. Cấu hình tài khoản cho TC11

Không ghi username hoặc password thật vào source code. Đặt chúng trong biến
môi trường của PowerShell:

```powershell
$env:UTC_USER="your_username"
$env:UTC_PASS="your_password"
```

Kiểm tra nhanh biến đã được thiết lập:

```powershell
if (-not $env:UTC_USER -or -not $env:UTC_PASS) { Write-Host "Missing UTC credentials" }
```

## 7. Chạy test

Chạy toàn bộ test:

```powershell
pytest -v
```

Chạy một test cụ thể:

```powershell
pytest -v tests/test_login.py::test_password_field_is_masked
```

TC01 đến TC10 không cần tài khoản UTC. TC11 cần cả `UTC_USER` và `UTC_PASS`.

## 8. Tạo và xem Allure report

### Tạo dữ liệu report

```powershell
pytest --alluredir=allure-results --clean-alluredir
```

Lệnh này chạy test thật và ghi dữ liệu kết quả vào thư mục `allure-results`.

### Cài Allure Commandline trên Windows

Allure Commandline cần Java 8 trở lên. Có thể cài Java bằng:

```powershell
winget install EclipseAdoptium.Temurin.17.JDK
```

Sau đó cài Scoop và Allure:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
scoop install allure
```

Kiểm tra cài đặt:

```powershell
java -version
allure --version
```

### Mở report tương tác

```powershell
allure serve allure-results
```

### Tạo report tĩnh

```powershell
allure generate allure-results -o allure-report --clean
allure open allure-report
```

Mỗi test có title, epic, feature, story và severity. Khi test fail, report có
thêm screenshot Chrome headless và page source tại thời điểm lỗi.

## 9. Explicit Wait và headless browser

`BasePage` sử dụng `WebDriverWait` cùng Selenium Expected Conditions cho việc
chờ phần tử, click và phản hồi form. Code không sử dụng `time.sleep()`.

Chrome được cấu hình trong `tests/conftest.py` với:

```text
--headless=new
--window-size=1920,1080
--no-sandbox
--disable-dev-shm-usage
```

Driver được đóng trong `finally` sau mỗi test.

## 10. Git workflow

Mỗi test case được thêm trong một commit riêng. Phần POM và Allure là các
commit hạ tầng dùng chung. Kiểm tra lịch sử:

```powershell
git log --oneline
git status
```

Không commit password, file `.env`, `allure-results` hoặc `allure-report`.

## 11. Chạy CI trên GitHub Actions

Workflow nằm tại `.github/workflows/tests.yml`.

- Mỗi `push` và Pull Request chạy nhóm smoke test TC01–TC10.
- TC11 không chạy tự động trên Pull Request vì cần tài khoản thật.
- Có thể chạy TC11 bằng tab **Actions** → **Selenium tests** → **Run workflow**.

Trước khi chạy TC11 trên GitHub, tạo hai Repository Secrets:

```text
UTC_USER
UTC_PASS
```

Kết quả pytest và dữ liệu Allure được lưu dưới dạng artifact ở mỗi workflow,
kể cả khi test fail. Có thể tải `allure-results` về máy và mở bằng:

```powershell
allure serve allure-results
```
