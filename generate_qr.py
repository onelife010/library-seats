import qrcode

# Replace with your actual local IP address
url = "http://192.168.1.14:5000"

qr = qrcode.make(url)

# Save the QR code image
qr.save("library_qr.png")

print("✅ QR code saved as library_qr.png")
