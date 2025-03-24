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
