import { useState } from 'react'
import {
  GaugeContainer,
  GaugeValueArc,
  GaugeReferenceArc,
  useGaugeState
} from '@mui/x-charts/Gauge';
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
  function GaugePointer() {
    const { valueAngle, outerRadius, cx, cy } = useGaugeState();

    if (valueAngle === null) {
      // No value to display
      return null;
    }

    const target = {
      x: cx + outerRadius * Math.sin(valueAngle),
      y: cy - outerRadius * Math.cos(valueAngle),
    };
    return (
      <g>
        <circle cx={cx} cy={cy} r={5} fill="red" />
        <path
          d={`M ${cx} ${cy} L ${target.x} ${target.y}`}
          stroke="red"
          strokeWidth={3}
        />
      </g>
    );
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
          <div style={{
            position: 'relative',
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center', 
            width: '100%', // Ensure it takes full width of parent to center properly
            height: '150px', // Give it enough height
            marginBottom: '20px' // Space below the gauge
          }}>
            <GaugeContainer
              width={300}
              height={150}
              startAngle={-110}
              endAngle={110}
              valueMin={-1}
              valueMax={1}
              value={result.score}>
              <GaugeReferenceArc />
              <GaugeValueArc />
              <GaugePointer />
            </GaugeContainer>
            <span style={{ position: 'absolute', bottom: '-20px', left: '20px', color: '#f87171', fontWeight: 'bold', fontSize: '12px' }}>
              BEARISH
            </span>
            <span style={{ position: 'absolute', bottom: '145px', left: '50%', transform: 'translateX(-50%)', color: '#626262ff', fontSize: '12px' }}>
              NEUTRAL
            </span>
            <span style={{ position: 'absolute', bottom: '-20px', right: '20px', color: '#4ade80', fontWeight: 'bold', fontSize: '12px' }}>
              BULLISH
            </span>
            
          </div>
          <h3>Score: {result.score.toFixed(2)}</h3>
          <h5>Score between -1 (Bearish) to 1 (Bullish)</h5>
        </div>
      )}
    </div>
  )
}

export default App

