import os
import pyotp

TOKEN = os.environ.get("OTP", "JBSWY3DPEHPK3PXP")


hotp = pyotp.HOTP(TOKEN)
