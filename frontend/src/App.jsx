import { useState } from 'react'
import './App.css'

function App() {
  // Setting variables to track
  const [url, setUrl] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleAnalyse = async () => {
    // Reset for new request
    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await fetch('http://127.0.0.1:8000/analyse', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url }),
      })

      if(!response.ok) {
        throw new Error("Failed to analyse URL")
      }

      const data = await response.json()

      setResult(data)
    }
    catch (err) {
      setError(err.message)       
    }
    finally {
      //After all is done loading off
      setLoading(false)
    }
  }
  return (
    <div className='Container'>
      <h1>Market Signal</h1>
      <div className='card'>
        <input type='text' placeholder='Enter URL Here' value={url} onChange={(e) => setUrl(e.target.value)}/> 
        <button onClick={handleAnalyse} disabled={loading}>{loading ? 'Analysing...' : 'Get Signal'}</button>
      </div>
      {error && <p className='error'>{error}</p>} {/*Error && means only show if error is not empty*/}
      {result && (
        <div className='result'>
          <h2>{result.sentiment.toUpperCase()}</h2>
          <p>Confidence: {(parseFloat(result.score) * 100).toFixed(1)}%</p>
        </div>
      )}
    </div>
  )
}

export default App

