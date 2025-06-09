Here's the bug ticket based on the informal report:

**Title:** Logout Button Unresponsive on Safari

**Description:**
The "Logout" button on the application is not functioning when accessed via the Safari browser. Users are unable to log out of their accounts, as clicking the button yields no response.

**Steps to Reproduce:**
1. Open the application in **Safari browser**.
2. Log in with any valid user credentials.
3. Navigate to the page where the "Logout" button is displayed (e.g., header, user profile dropdown).
4. Click the **"Logout" button**.

**Expected vs Actual Behavior:**
* **Expected:** Upon clicking the "Logout" button, the user should be logged out of their account and redirected to the login page or a logged-out state.
* **Actual:** Clicking the "Logout" button produces no visible reaction or change in the application. The user remains logged in.

**Environment (if known):**
* **Browser:** Safari (Specific version unknown, but latest stable is preferred for testing)
* **Operating System:** Unknown (Mac OS is likely, but not specified)
* **Device:** Unknown

**Severity or Impact:**
**High.** Users are unable to log out of their accounts on Safari, which can lead to security concerns (e.g., if a shared computer is used) and prevents users from switching accounts or ending their session properly.