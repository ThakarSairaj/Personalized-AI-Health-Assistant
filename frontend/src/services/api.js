// services/api.js
const BASE_URL = 'http://127.0.0.1:8000'

export const loginUser = async (data) => {
  const res = await fetch(`${BASE_URL}/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  const result = await res.json()
  if (!res.ok) throw new Error(result.detail || 'Login failed')
  return result
}

export const registerUser = async (data) => {
  const res = await fetch(`${BASE_URL}/createUser/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })

  const result = await res.json()

  if (!res.ok) {
    // Show the error from backend
    throw new Error(result.detail || 'Registration failed')
  }

  return result
}

export const submitHealthInfo = async (healthData) => {
  const userId = localStorage.getItem('user_id')

  const res = await fetch(`${BASE_URL}/addUser/${userId}/healthDetails/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(healthData),
  })

  const result = await res.json()
  if (!res.ok) throw new Error(result.detail || 'Health info submission failed')
  return result
}


// ================== PDF Extractor ===============
export const uploadPdf = async (file) => {
  const token = localStorage.getItem("access_token")
  if (!token) throw new Error("User not logged in")

  const formData = new FormData()
  formData.append("file", file)

  const res = await fetch("http://127.0.0.1:8000/upload-report", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`, // <-- this is required!
    },
    body: formData,
  })

  const result = await res.json()
  if (!res.ok) {
    throw new Error(result.detail || "PDF extraction failed")
  }

  return result
}


