import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Box,
  LinearProgress,
} from '@mui/material';
import {
  People as PeopleIcon,
  ShoppingCart as ProductsIcon,
  Category as CategoryIcon,
  AttachMoney as MoneyIcon,
} from '@mui/icons-material';
import { usersAPI, productsAPI, categoriesAPI } from '../services/api';

const Dashboard = () => {
  const [stats, setStats] = useState({
    users: 0,
    products: 0,
    categories: 0,
    totalValue: 0,
    loading: true,
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [usersResponse, productsResponse, categoriesResponse] = await Promise.all([
          usersAPI.getAll(),
          productsAPI.getAll(),
          categoriesAPI.getAll(),
        ]);

        const users = usersResponse.data;
        const products = productsResponse.data;
        const categories = categoriesResponse.data;

        const totalValue = products.reduce((sum, product) => sum + (product.price * product.stock_quantity), 0);

        setStats({
          users: users.length,
          products: products.length,
          categories: categories.length,
          totalValue: totalValue,
          loading: false,
        });
      } catch (err) {
        console.error('Error fetching stats:', err);
        setStats(prev => ({ ...prev, loading: false }));
      }
    };

    fetchStats();
  }, []);

  if (stats.loading) {
    return (
      <Container>
        <LinearProgress />
        <Typography>Loading dashboard...</Typography>
      </Container>
    );
  }

  const StatCard = ({ icon, title, value, subtitle, color = 'primary' }) => (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <Box
            sx={{
              backgroundColor: `${color}.main`,
              color: 'white',
              borderRadius: 1,
              p: 1,
              mr: 2,
            }}
          >
            {icon}
          </Box>
          <Box>
            <Typography variant="h4" component="div" fontWeight="bold">
              {value}
            </Typography>
            <Typography color="textSecondary">{title}</Typography>
            {subtitle && (
              <Typography variant="body2" color="textSecondary">
                {subtitle}
              </Typography>
            )}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" component="h1" gutterBottom>
        Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            icon={<PeopleIcon />}
            title="Total Users"
            value={stats.users}
            color="primary"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            icon={<ProductsIcon />}
            title="Total Products"
            value={stats.products}
            color="secondary"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            icon={<CategoryIcon />}
            title="Categories"
            value={stats.categories}
            color="success"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            icon={<MoneyIcon />}
            title="Inventory Value"
            value={`$${stats.totalValue.toFixed(2)}`}
            subtitle="Total stock value"
            color="warning"
          />
        </Grid>
      </Grid>

      <Box mt={4}>
        <Typography variant="h5" gutterBottom>
          Quick Overview
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Recent Users
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Manage user accounts and permissions
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Product Catalog
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  View and manage your product inventory
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Dashboard;