import { useState } from "react"
import { uploadPdf } from "../services/api"

const UploadReport = () => {
  const [file, setFile] = useState(null)
  const [text, setText] = useState("")
  const [loading, setLoading] = useState(false)

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF file")
      return
    }

    try {
      setLoading(true)
      const res = await uploadPdf(file)
      setText(res.text)
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

      {text && (
        <>
          <h3>Extracted Text</h3>
          <pre style={{ whiteSpace: "pre-wrap" }}>
            {text}
          </pre>
        </>
      )}
    </div>
  )
}

export default UploadReport
