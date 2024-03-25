import React, { useState, useEffect } from 'react';

const App = () => {
  const [drivers, setDrivers] = useState([]);

  useEffect(() => {
    // Fetch the data from the drivers.json file
    fetch('/data/drivers-championship-no-max.json')
      .then(response => response.json())
      .then(data => {
        // Convert the object to an array of key-value pairs
        const driversArray = Object.entries(data);

        // Sort the array based on points in descending order
        driversArray.sort((a, b) => b[1] - a[1]);

        // Add the position field to each driver
        const driversWithPosition = driversArray.map(([driver, points], index) => ({
          driver,
          points,
          position: index + 1,
        }));

        setDrivers(driversWithPosition);
      })
      .catch(error => console.error('Error fetching drivers data:', error));
  }, []);

  return (
    <div>
      <h1>Formula 1 Drivers</h1>
      <table>
        <thead>
          <tr>
            <th>Position</th>
            <th>Driver</th>
            <th>Points</th>
          </tr>
        </thead>
        <tbody>
          {drivers.map(({ driver, points, position }, index) => (
            <tr key={index}>
              <td>{position}</td>
              <td>{driver}</td>
              <td>{points}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default App;