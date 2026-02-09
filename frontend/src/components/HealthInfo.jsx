import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './HealthInfo.css'
import { submitHealthInfo } from '../services/api'

const HealthInfo = () => {
  const navigate = useNavigate()

  const [healthData, setHealthData] = useState({
    height: '',
    weight: '',
    blood_group: '',
  })

  const handleSubmit = async (e) => {
    e.preventDefault()
    console.log(healthData) // debug
    const res = await submitHealthInfo(healthData)
    alert(res.message)
    navigate('/dashboard') // or wherever you want
  }

  return (
    <div className="container health-page">
      <div className="form-box health">

        <h1>Health Information</h1>

        <form onSubmit={handleSubmit}>

          <div className="input-box">
            <input
              type="number"
              placeholder="Height (cm)"
              required
              onChange={(e) =>
                setHealthData({ ...healthData, height: e.target.value })
              }
            />
          </div>

          <div className="input-box">
            <input
              type="number"
              placeholder="Weight (kg)"
              required
              onChange={(e) =>
                setHealthData({ ...healthData, weight: e.target.value })
              }
            />
          </div>

          <div className="input-box">
            <select
              required
              onChange={(e) =>
                setHealthData({ ...healthData, blood_group: e.target.value })
              }
            >
              <option value="">Select Blood Group</option>
              <option value="A+">A+</option>
              <option value="A-">A-</option>
              <option value="B+">B+</option>
              <option value="B-">B-</option>
              <option value="AB+">AB+</option>
              <option value="AB-">AB-</option>
              <option value="O+">O+</option>
              <option value="O-">O-</option>
            </select>
          </div>

          <button className="btn">Save & Continue</button>

        </form>
      </div>
    </div>
  )
}

export default HealthInfo
