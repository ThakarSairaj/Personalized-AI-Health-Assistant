import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './AuthForm.css'
import { loginUser } from '../services/api'

const AuthForm = () => {
  const navigate = useNavigate()
  const [loginData, setLoginData] = useState({
    email: '',
    password: '',
  })

  const handleLogin = async (e) => {
    e.preventDefault()
    const res = await loginUser(loginData)
    alert(res.message)
  }

  return (
    <div className="container">
      <div className="form-box login">
        <form onSubmit={handleLogin}>
          <h1>Login</h1>

          <div className="input-box">
            <input
              type="email"
              placeholder="Email"
              onChange={(e) =>
                setLoginData({ ...loginData, email: e.target.value })
              }
              required
            />
          </div>

          <div className="input-box">
            <input
              type="password"
              placeholder="Password"
              onChange={(e) =>
                setLoginData({ ...loginData, password: e.target.value })
              }
              required
            />
          </div>

          <button type="submit" className="btn">Login</button>

          <p style={{ marginTop: '15px' }}>
            Don’t have an account?{' '}
            <span
              style={{ color: '#7494ec', cursor: 'pointer' }}
              onClick={() => navigate('/register')}
            >
              Register
            </span>
          </p>
        </form>
      </div>
    </div>
  )
}

export default AuthForm
