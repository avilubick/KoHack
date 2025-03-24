import React from 'react';
import { useNavigate } from 'react-router-dom';
import Globe from 'react-globe.gl';
import globeImage from '../assets/earth-day.jpg';
import CoordData from '../assets/getdata.json';

const Page = () => {
  const navigate = useNavigate(); // Hook for navigation

  /*
  const [coords, setCoords] = useState([]); // Define state for coordinates

  useEffect(() => {
    const url = "127.0.0.1"; //Local host

    fetch(url)
      .then(response => response.json())
      .then(data => setCoords(data)) // Ensure data format matches expected structure
      .catch(error => console.error('Error fetching data:', error));
  }, []);
  */
  
  const myData = [
    {
      "lat": 42.5226219,
      "lng": -83.6756,
      "altitude": 0.4,
      "color": "#00ff33"
    },
    {
      "lat": 40.7127281,
      "lng": -74.0060,
      "altitude": 0.4,
      "color": "#ff0000"
    },
    {
      "lat": 37.5867433,
      "lng": -122.3212,
      "altitude": 0.4,
      "color": "#ffff00"
    },
    {
      "lat": 34.052235,
      "lng": -118.243683,
      "altitude": 0.5,
      "color": "#0000ff"
    },
    {
      "lat": 51.507351,
      "lng": -0.127758,
      "altitude": 0.6,
      "color": "#ff1493"
    },
    {
      "lat": 48.856613,
      "lng": 2.352222,
      "altitude": 0.3,
      "color": "#8a2be2"
    },
    {
      "lat": 35.689487,
      "lng": 139.691711,
      "altitude": 0.4,
      "color": "#ff6347"
    },
    {
      "lat": 39.904202,
      "lng": 116.407396,
      "altitude": 0.7,
      "color": "#32cd32"
    },
    {
      "lat": 40.730610,
      "lng": -73.935242,
      "altitude": 0.5,
      "color": "#dda0dd"
    },
    {
      "lat": 34.052235,
      "lng": -118.243683,
      "altitude": 0.8,
      "color": "#ff4500"
    },
    // Middle East and Europe entries (excluding Asia)
    {
      "lat": 31.768319,
      "lng": 35.21371,
      "altitude": 0.5,
      "color": "#ff8c00"
    },
    {
      "lat": 33.6844,
      "lng": 73.0479,
      "altitude": 0.6,
      "color": "#3cb371"
    },
    {
      "lat": 41.902782,
      "lng": 12.496366,
      "altitude": 0.3,
      "color": "#ffd700"
    },
    {
      "lat": 40.748817,
      "lng": -73.985428,
      "altitude": 0.5,
      "color": "#800080"
    },
    {
      "lat": 51.165691,
      "lng": 10.451526,
      "altitude": 0.4,
      "color": "#dc143c"
    },
    {
      "lat": 55.755825,
      "lng": 37.617298,
      "altitude": 0.4,
      "color": "#7fff00"
    },
    {
      "lat": 40.73061,
      "lng": 29.94712,
      "altitude": 0.5,
      "color": "#6a5acd"
    },
    {
      "lat": 43.65107,
      "lng": 23.45485,
      "altitude": 0.5,
      "color": "#c71585"
    },
    {
      "lat": 41.0115,
      "lng": 28.9784,
      "altitude": 0.6,
      "color": "#add8e6"
    }
];


  return (
    <div className="cursor-move" style={{ position: 'relative', width: '100vw', height: '100vh' }}>
      {/* Bigger Back Button with Blue Color */}
      <button
        onClick={() => navigate('/')} // Navigate to home page
        style={{
          position: 'absolute',
          top: '20px',
          left: '20px',
          padding: '15px 25px',  // Bigger button
          fontSize: '1.5rem',     // Bigger text
          fontWeight: 'bold',     // Bold text for emphasis
          backgroundColor: '#0096FF', // Bright blue
          color: '#fff',
          border: 'none',
          borderRadius: '10px',
          cursor: 'pointer',
          zIndex: 1000,
        }}
      >
        ← Back
      </button>

      <Globe globeImageUrl={globeImage} pointsData={CoordData} pointAltitude="altitude" pointColor="color" />
    </div>
  );
};

export default Page;
