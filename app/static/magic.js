/* 2️⃣ Initialize Magic Instance */
      const magic = new Magic("pk_test_8CD827D09FEA11FE");

      /* 3️⃣ Implement Render Function */
      const render = async () => {
        const isLoggedIn = await magic.user.isLoggedIn();
        /* Show login form if user is not logged in */
        let html = `
          Login: 
          <form onsubmit="handleLogin(event)">
            <input type="email" name="email" required="required" placeholder="Enter your email" />
            <button type="submit">Send</button>
          </form>
        `;
        if (isLoggedIn) {
          /* Get user metadata including email */
          const userMetadata = await magic.user.getMetadata();
          html = `
            Hello ${userMetadata.email} 
            <button onclick="handleLogout()">Logout</button>
          `;
        }
        document.getElementById("app").innerHTML = html;
      };

      /* 4️⃣ Implement Login Handler */
      const handleLogin = async e => {
        e.preventDefault();
        const email = new FormData(e.target).get("email");
        if (email) {
          /* One-liner login 🤯 */
          await magic.auth.loginWithMagicLink({ email });
          render();
        }
      };

      /* 5️⃣ Implement Logout Handler */
      const handleLogout = async () => {
        await magic.user.logout();
        render();
      };
