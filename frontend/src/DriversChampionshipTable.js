import React, { useState, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
  tableContainer: {
    marginTop: '2rem',
  },
});

const App = () => {
  const classes = useStyles();
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
      <Typography variant="h3" component="h1" align="center" gutterBottom>
        Formula 1 Drivers
      </Typography>
      <TableContainer component={Paper} className={classes.tableContainer}>
        <Table className={classes.table} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Position</TableCell>
              <TableCell>Driver</TableCell>
              <TableCell>Points</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {drivers.map(({ driver, points, position }, index) => (
              <TableRow key={index}>
                <TableCell component="th" scope="row">
                  {position}
                </TableCell>
                <TableCell>{driver}</TableCell>
                <TableCell>{points}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default App;