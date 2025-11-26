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
      const response = await fetch('https://127.0.0.1:8000/analyse', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url }),
      })

      if(!response.ok) {
        throw new error("Failed to analyse URL")
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
}
