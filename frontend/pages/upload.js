import { useState } from 'react'

export default function Upload() {
  const [job, setJob] = useState("")
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)

  const submit = async () => {
    const form = new FormData()
    form.append("resume", file)
    form.append("job_description", job)

    const res = await fetch("https://YOUR_RENDER_BACKEND_URL/parse", {
      method: "POST",
      body: form
    })

    const data = await res.json()
    setResult(data)
  }

  return (
    <div className="container">
      <h2>Upload Resume</h2>

      <textarea 
        placeholder="Enter Job Description"
        onChange={e => setJob(e.target.value)}
      />

      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <button onClick={submit}>Analyze</button>

      {result && (
        <div className="result">
          <p><b>Match Score:</b> {result.match_score}</p>
          <p><b>Roles:</b> {result.roles.join(", ")}</p>
          <p><b>Experience:</b> {result.experience.join(", ")}</p>
        </div>
      )}
    </div>
  )
}
