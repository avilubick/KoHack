import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Globe from "react-globe.gl";

const Page = () => {
  const navigate = useNavigate();
  const [data, setData] = useState<any[]>([]);
  const [error, setError] = useState("");
  const [selectedPoint, setSelectedPoint] = useState<any | null>(null); // Track clicked point

  const fetchData = async () => {
    try {
      console.log("Fetching data...");
      const dataResponse = await fetch("http://127.0.0.1:5000/getdata", {
        method: "GET",
        credentials: "include",
      });

      const coordData = await dataResponse.json();

      if (Array.isArray(coordData)) {
        setData(coordData);
      } else {
        setError("Data not found");
        console.log("Data fetch failed");
      }
    } catch (err) {
      setError("Server error. Please try again later.");
      console.log("Data fetch error:", err);
    }
  };

  useEffect(() => {
    const checkSession = async () => {
      try {
        console.log("Checking session...");
        const sessionResponse = await fetch("http://127.0.0.1:5000", {
          method: "GET",
          credentials: "include",
        });
        const sessionData = await sessionResponse.json();

        if (sessionData.data = "Logged in") {
          console.log("Session active for:", sessionData.user_id);
          fetchData(); // Fetch data immediately if session exists
        }
      } catch (err) {
        console.log("Session check failed:", err);
        setError("Session check failed");
      }
    };

    checkSession();
  }, [navigate]);

  const handleClick = async () => {
    try {
      console.log("Logging out...");
      const logoutResponse = await fetch("http://127.0.0.1:5000/logout", {
        method: "GET",
        credentials: "include",
      });

      const sessionData = await logoutResponse.json();
      console.log("Logout successful:", sessionData);
      navigate("/login");
    } catch (err) {
      console.log("Logout failed:", err);
    }
  };

  const upload = async () => {
    navigate("/");
  }

  return (
    <div>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button onClick={handleClick}>Logout</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button onClick={upload}>Upload GED</button>
      <Globe
        globeImageUrl="//unpkg.com/three-globe/example/img/earth-day.jpg"
        pointsData={data}
        pointLat="lat"
        pointLng="lng"
        pointLabel="label"
        pointColor={() => "red"}
        onPointClick={(point) => setSelectedPoint(point)} // Handle point click
      />

      {selectedPoint && (
        <div
          style={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            backgroundColor: "white",
            padding: "10px",
            borderRadius: "5px",
            boxShadow: "0px 0px 10px rgba(0,0,0,0.2)",
            zIndex: 1000,
          }}
        >
          <h3>Location Details</h3>
          <p><strong>Latitude:</strong> {selectedPoint.lat}</p>
          <p><strong>Longitude:</strong> {selectedPoint.lng}</p>
          <p><strong>Label:</strong> {selectedPoint.label}</p>
          <button onClick={() => setSelectedPoint(null)}>Close</button>
        </div>
      )}
    </div>
  );
};

export default Page;
