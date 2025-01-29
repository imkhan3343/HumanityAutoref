# HumanityAutoref

How to Run
Install Dependencies:

bash
Copy
pip install requests fake-useragent bip-utils
Prepare Files:

Create proxies.txt with your proxies (one per line):

Copy
http://user1:pass123@1.1.1.1:8080
http://user2:pass456@2.2.2.2:8080
Replace YOUR_REFERRAL_CODE_HERE in the code with your actual referral code.

Run the Script:

bash
Copy
python referral_bot.py
Output:

Successfully created wallets appear in the wallets/ folder.

Console logs show proxy usage and success/failure messages.

Troubleshooting
Proxy Errors:

Ensure proxies in proxies.txt are valid and authenticated.

Test proxies manually with curl -x <proxy> http://ipinfo.io/ip.

API Changes:

Use browser dev tools (Network tab) to inspect actual API endpoints and request formats for Humanity Protocol.

CAPTCHA Issues:

If CAPTCHAs are encountered, you’ll need to integrate a solving service (e.g., 2Captcha).

Rate Limiting:

Increase REQUEST_DELAY in the configuration.


Ethical & Legal Note
This code demonstrates automation concepts and may violate the Humanity Protocol's terms of service. Use only for educational purposes on platforms where you have explicit permission to automate actions. Unauthorized use could result in legal action or account bans.
