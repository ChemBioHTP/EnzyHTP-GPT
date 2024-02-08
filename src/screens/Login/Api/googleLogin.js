import Cookies from 'js-cookie';
export async function googlelogin() {
    await fetch('/api/auth/oauth/google/login', {
        method: 'POST',
        mode: 'cors',
      })
      .then(response => {
            
        return response.json();
      })
      .then(data => {         
          console.log("success");
      })
      .catch(error => {
          console.error('Error sending data:', error);
      });
}