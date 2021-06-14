import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Container from '@material-ui/core/Container';
import Header from './components/Header';
import {UserTransactions} from "./components/Transactions";
import SignIn from "./components/SignIn";
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import Register from "./components/Register";
import {Product} from "./components/Product";
import {Shop} from "./components/Shop";
import {ShoppingBag} from "./components/ShoppingBag";
import {Cart} from "./components/Cart";
import {ProvideAuth} from "./components/use-auth.js";
import {MainPage} from "./components/MainPage";
import {Discounts} from "./components/Discounts";
import SystemManagerTransactionHistory from "./components/systemManagerTransactionHistory";
import SearchProducts from "./components/SearchProducts";
import {ShopForCustomer} from "./components/ShopForCustomer";
import ProfilePage from "./components/ProfilePage";
import {Checkout} from "./components/Checkout";
import {PurchasePolicies} from "./components/PurchasePolicies";
import {Offers} from "./components/Offers";

const useStyles = makeStyles((theme) => ({
  mainGrid: {
    marginTop: theme.spacing(3),
  },
}));

const categories = [
  {title: 'Main page', url: ''},
  {title: 'Search products', url: 'search'},
];


export default function Blog() {
  const classes = useStyles();

  return (
      <ProvideAuth>
      <Router>
        <React.Fragment>
          <CssBaseline/>
          <Container maxWidth="lg" className={`site-layout-wrapper=modal-active`}>
            <Header categories={categories} />
            <main>
              <Grid container justify="center" spacing={5} className={classes.mainGrid}>
                <Switch>
                  {/* Guest routes */}
                  <Route path="/shops/:shop_id/products/:product_id" exact>
                    <Product/>
                  </Route>
                  <Route path="/checkout">
                    <Checkout />
                  </Route>
                  <Route path="/register">
                    <Register />
                  </Route>
                  <Route path="/cart">
                    <Cart/>
                  </Route>
                  <Route path="/offers">
                    <Offers />
                  </Route>
                  <Route path="/cart/:shop_id">
                    <ShoppingBag/> {/* This means shopping bag of shop shop_id*/}
                  </Route>
                  <Route path="/shops/:shop_id/discounts">
                    <Discounts/>
                  </Route>
                  <Route path="/shops/:shop_id/purchase_policies">
                    <PurchasePolicies />
                  </Route>
                  <Route path="/shops/:shop_id">
                    <Shop/>
                  </Route>
                  <Route path="/Cshops/:shop_id">
                    <ShopForCustomer/>
                  </Route>
                  <Route path="/shops/:shop_id/products/:product_id">
                    <Product/>
                  </Route>
                  <Route path="/profile">
                    <ProfilePage/>
                  </Route>
                  <Route path="/login" exact>
                    <SignIn />
                  </Route>
                  <Route path="/transactions">
                    <UserTransactions/>
                  </Route>
                  <Route path="/" exact>
                    <MainPage />
                  </Route>
                  <Route path="/search" exact>
                    <SearchProducts/>
                  </Route>
                  <Route path="/system_transactions" exact>
                    <SystemManagerTransactionHistory />
                  </Route>
                  }
                </Switch>
              </Grid>
            </main>
            <div style={{width: "100%", height: "10rem"}}/>
          </Container>
        </React.Fragment>
      </Router>
      </ProvideAuth>
  );
}
