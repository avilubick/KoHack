"use client";
import * as React from "react";
import styles from "./Home.module.css";
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import Box from '@mui/material/Box' 
import BG from '../assets/home_background.png'
import Link from  '@mui/material/Link'

function Home() {
  return (
    <div>
      <Box
        sx={{
          backgroundImage: `url(${BG})`,
          backgroundSize: 'cover', // or 'contain', 'auto', etc.
          backgroundRepeat: 'no-repeat', // or 'repeat', 'repeat-x', 'repeat-y'
          backgroundPosition: 'top', // or 'top', 'bottom', 'left', 'right' or combinations
          height: '900px', // Adjust as needed
          width: '100%', // Adjust as needed
          // Add other styling as necessary
        }}
      > {
        <ButtonGroup
          sx={{
            position: "fixed",
            top: 20,
            left: "50%",
            transform: "translateX(-50%)",
            zIndex: 100,
          }}
          variant="contained"
          aria-label="Basic button group"
        >
          <Button sx={{ fontSize: "1.2rem", padding: "12px 24px" }}>
            <Link color="#ffffff" href="/register" underline="none">Sign up</Link>
          </Button>
          <Button sx={{ fontSize: "1.2rem", padding: "12px 24px" }}>
            <Link color="#ffffff" href="/login" underline="none">Login</Link>
          </Button>
        </ButtonGroup>
        }     
      </Box>
    </div>
  );
}

export default Home;