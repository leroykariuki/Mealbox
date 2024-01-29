import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
  const navigate = useNavigate();
  const [isSignUp, setIsSignUp] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [error, setError] = useState(null);

  const toggleAuthMode = () => {
    setIsSignUp((prevIsSignUp) => !prevIsSignUp);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleLogin = (token) => {
    localStorage.setItem('token', token);
    navigate('/homepage');
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    fetch('http://127.0.0.1:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Login failed');
        }
      })
      .then((data) => {
        console.log(data.message);
        setError(null);
        handleLogin(data.token);
      })
      .catch((error) => {
        setError(error.message);
      });
  };

  return (
    <div className="auth-container">
      <div className="auth-form">
        <h2 className="auth-heading">{isSignUp ? 'Sign Up' : 'Log In'}</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <input
              type="text"
              id="username"
              name="username"
              placeholder="Username"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <input
              type="password"
              id="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>
          <button className="auth-button" type="submit">
            {isSignUp ? 'Sign Up' : 'Login'}
          </button>
        </form>
        {error && <p className="auth-error">{error}</p>}
        <p className="auth-switch-text">
          {isSignUp ? 'Already have an account? ' : "Don't have an account? "}
          <button className="auth-switch-button" onClick={toggleAuthMode}>
            {isSignUp ? 'Log In' : 'Sign Up'}
          </button>
        </p>
      </div>
    </div>
  );
}

export default Login;
