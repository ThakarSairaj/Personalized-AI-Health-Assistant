// Register.jsx
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './Register.css'
import { registerUser } from '../services/api'

const Register = () => {
  const navigate = useNavigate()
  const [error, setError] = useState('') // ✅ store error messages

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    dob: '',
    gender: '',
    phone: '',
    email: '',
    password: '',
    country: '',
    state: '',
    city: '',
  })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('') // reset error

    try {
      const res = await registerUser(formData)

      // ✅ save user_id for health form
      localStorage.setItem('user_id', res.user_id)

      // ✅ navigate to health info page
      navigate('/health-info')

    } catch (err) {
      // ✅ show proper error message
      setError(err.message)
      console.error(err)
    }
  }

  return (
    <div className="container register-page">
      <div className="form-box register">

        <h1>Create Account</h1>

        <form onSubmit={handleSubmit}>
          {/* Inputs for first_name, last_name, etc. */}
          <div className="input-box">
            <input placeholder="First Name" required
              onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
            />
          </div>
          <div className="input-box">
            <input placeholder="Last Name" required
              onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
            />
          </div>
          <div className="input-box">
            <input type="date" required
              onChange={(e) => setFormData({ ...formData, dob: e.target.value })}
            />
          </div>
          <div className="input-box">
            <select required
              onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
            >
              <option value="">Select Gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </div>
          <div className="input-box">
            <input placeholder="Phone" required
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
            />
          </div>
          <div className="input-box">
            <input type="email" placeholder="Email" required
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            />
          </div>
          <div className="input-box full">
            <input type="password" placeholder="Password" required
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            />
          </div>
          <div className="input-box">
            <input placeholder="Country"
              onChange={(e) => setFormData({ ...formData, country: e.target.value })}
            />
          </div>
          <div className="input-box">
            <input placeholder="State"
              onChange={(e) => setFormData({ ...formData, state: e.target.value })}
            />
          </div>
          <div className="input-box">
            <input placeholder="City"
              onChange={(e) => setFormData({ ...formData, city: e.target.value })}
            />
          </div>

          <button className="btn">Register</button>

          {/* ✅ show error message below form */}
          {error && <p className="error">{error}</p>}
        </form>
      </div>
    </div>
  )
}

export default Register
