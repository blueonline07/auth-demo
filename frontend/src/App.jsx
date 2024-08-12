// src/App.js
import React from 'react';
import { useEffect, useState } from 'react';
import axios from 'axios';

const App = () => {
  const [msg, setMsg] = useState('not logged in yet');
  useEffect(() => {
    async function fetchData() {
      const accessTokenRegex = /access_token=([^&]+)/;
      const isMatch = window.location.href.match(accessTokenRegex);

      if (isMatch) {
        const accessToken = isMatch[1];
        const resp = await axios.post('http://localhost:8000/api/google/login/', {
          access_token: accessToken
        })
        console.log(resp.data);
        localStorage.setItem('access', resp.data.access);
        localStorage.setItem('refresh', resp.data.refresh);
      }
    }
    async function auth() {
      if (localStorage.getItem('access')) {
        const resp = await axios.get('http://localhost:8000/api/hello/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access')}`
          }
        })
        setMsg(resp.data);
      } else {
        fetchData();
      }
    }
    auth();
  }, []);
  const handleLogin = () => {
    const callbackUrl = `${window.location.origin}`;
    const googleClientId = "776839518387-uge8lkql0kv3p8jnnpejv1r3gi7jjlmr.apps.googleusercontent.com";
    const targetUrl = `https://accounts.google.com/o/oauth2/auth?redirect_uri=${encodeURIComponent(
      callbackUrl
    )}&response_type=token&client_id=${googleClientId}&scope=openid%20email%20profile`;

    window.location.href = targetUrl;
  };
  const handleLogout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    setMsg('logged out');
  };
  const sendCode= (e) => {
    e.preventDefault();
    console.log(e.target.email.value);
    axios.post('http://localhost:8000/api/password_reset/',{
      email: e.target.email.value
    })
  }
  const restorePassword = (e) => {
    e.preventDefault();
    console.log(e.target.code.value);
    axios.post('http://localhost:8000/api/password_reset/confirm/',{
      code: e.target.code.value
    })
  }
  return (
    <>
      <h1>{msg}</h1>
      <button onClick={handleLogin}>Login</button>
      <button onClick={handleLogout}>Logout</button>
      <br />
      <h1>Forgot password? enter ur email:</h1>
      <form onSubmit={sendCode}>
        <input type="email" name="email" placeholder="email" />
        <input type="submit" value="submit" />
      </form>
      <form onSubmit={restorePassword}>
        <input type='text' name='code' placeholder='your reset code'></input>
        <input type='submit' value='submit'></input>
      </form>
      
    </>
  );
};

export default App;
