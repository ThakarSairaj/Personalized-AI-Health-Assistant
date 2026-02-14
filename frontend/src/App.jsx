import { BrowserRouter, Routes, Route } from 'react-router-dom'
import AuthForm from './components/AuthForm'
import Register from './components/Register'
import HealthInfo from './components/HealthInfo'
import UploadReport  from './components/UploadReport'
import Landing from './components/Landing'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<AuthForm />} />
        <Route path="/register" element={<Register />} />
        <Route path="/health-info" element={<HealthInfo />} />
        <Route path="/upload-report" element={<UploadReport />} />

      </Routes>
    </BrowserRouter>
  )
}

export default App
