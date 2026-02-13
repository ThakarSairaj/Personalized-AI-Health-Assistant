import { useState } from "react"
import { uploadPdf } from "../services/api"

const UploadReport = () => {
  const [file, setFile] = useState(null)
  const [message, setMessage] = useState("")
  const [loading, setLoading] = useState(false)

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF file")
      return
    }

    try {
      setLoading(true)
      const res = await uploadPdf(file)
      setMessage(`${res.message}, Report ID: ${res.report_id}`)
    } catch (err) {
      alert(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2>Upload Medical Report</h2>

      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br /><br />

      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Processing..." : "Upload & Extract"}
      </button>

      {message && (
        <>
          <h3>Result</h3>
          <p>{message}</p>
        </>
      )}
    </div>
  )
}

export default UploadReport
