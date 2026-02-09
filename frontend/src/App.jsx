import { BrowserRouter, Routes, Route } from 'react-router-dom'
import AuthForm from './components/AuthForm'
import Register from './components/Register'
import HealthInfo from './components/HealthInfo'


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AuthForm />} />
        <Route path="/register" element={<Register />} />
        <Route path="/health-info" element={<HealthInfo />} />

      </Routes>
    </BrowserRouter>
  )
}

export default App
