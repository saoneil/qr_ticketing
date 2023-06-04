import qrcode

# Set the URL of the Google Form
form_url = "https://forms.gle/45oqZ5orCxipq7iE9"

qr = qrcode.QRCode(
  version=1,
  error_correction=qrcode.constants.ERROR_CORRECT_L,
  box_size=10,
  border=4,
)

# Add the form URL to the QR code
qr.add_data(form_url)
qr.make(fit=True)

# Create an image of the QR code
img = qr.make_image(fill_color="black", back_color="white")

# Save the image of the QR code
img.save("C:\\Users\\saone\\Desktop\\signup_qr.png")