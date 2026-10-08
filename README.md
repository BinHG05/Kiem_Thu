# Buổi 8 — Selenium & Page Object Model

Các bài kiểm thử trang đăng nhập dùng Python, Selenium, pytest và Chrome Headless.
Chúng bao phủ form đăng nhập, các trường nhập liệu, nút đăng nhập, tuỳ chọn
giữ đăng nhập, các liên kết hỗ trợ và luồng đăng nhập hợp lệ.

## Cài đặt

```powershell
python -m pip install -r requirements.txt
```

## Thiết lập tài khoản

Đăng nhập thành công cần tài khoản UTC hợp lệ. Trong PowerShell, đặt thông tin qua biến môi trường:

```powershell
$env:UTC_USER="your_username"
$env:UTC_PASS="your_password"
```

## Chạy bài kiểm thử

```powershell
pytest
```

Test đăng nhập hợp lệ cần cả `UTC_USER` và `UTC_PASS`. Selenium Manager sẽ tự
xử lý ChromeDriver khi cần.
