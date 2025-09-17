import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
} from '@mui/material';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
  const location = useLocation();

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          E-Commerce Store
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            color="inherit"
            component={Link}
            to="/"
            variant={location.pathname === '/' ? 'outlined' : 'text'}
          >
            Home
          </Button>
          <Button
            color="inherit"
            component={Link}
            to="/dashboard"
            variant={location.pathname === '/dashboard' ? 'outlined' : 'text'}
          >
            Dashboard
          </Button>
          <Button
            color="inherit"
            component={Link}
            to="/users"
            variant={location.pathname === '/users' ? 'outlined' : 'text'}
          >
            Users
          </Button>
          <Button
            color="inherit"
            component={Link}
            to="/products"
            variant={location.pathname === '/products' ? 'outlined' : 'text'}
          >
            Products
          </Button>
          <Button
            color="inherit"
            component={Link}
            to="/categories"
            variant={location.pathname === '/categories' ? 'outlined' : 'text'}
          >
            Categories
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;