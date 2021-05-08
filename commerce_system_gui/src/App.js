import React, {useState, useEffect, useLayoutEffect} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Container from '@material-ui/core/Container';
import Header from './components/Header';
import Transactions from "./components/Transactions";
import {Typography} from "@material-ui/core";
import SignIn from "./components/SignIn";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import Register from "./components/Register";
import {Product} from "./components/Product";
import {Shop} from "./components/Shop";
import {ShoppingBag} from "./components/ShoppingBag";
import {Cart} from "./components/Cart";
import { ProvideAuth } from "./components/use-auth.js";
import {Main} from "./components/Main";
import {Main_page} from "./components/Main_page";
import System_manager_transaction_history from "./components/system_manager_transaction_history";

const useStyles = makeStyles((theme) => ({
  mainGrid: {
    marginTop: theme.spacing(3),
  },
}));

const categories = [
  {title: 'Main page', url: ''},
  {title: 'Technology', url: 'technology'},
  {title: 'Design', url: 'design'},
  {title: 'Culture', url: 'culture'},
  {title: 'Business', url: 'business'},
  {title: 'Politics', url: 'political'},
  {title: 'Opinion', url: 'opinion'},
  {title: 'Science', url: 'science'},
  {title: 'Health', url: 'health'},
  {title: 'Style', url: 'style'},
  {title: 'Travel', url: 'travel'},
];

const transactions = [
  {
    id: 1,
    "shop": {
      "shop_id": 2,
      "shop_name": "shop2",
      "description": "shop2 desc"
    },
    "products": [
      {
        "product_id": 2,
        "product_name": "p2",
        "price": 2.5,
        "description": "a product",
        "amount": 1
      },
      {
        "product_id": 3,
        "product_name": "p3",
        "price": 3,
        "description": "a product",
        "amount": 2
      }
    ],
    "date": 1619448651.712134,
    "username" : "Moshe",
    "price": 2.5
  },
  {
    id: 2,
    "username" : "Moshe",
    "shop": {
      "shop_id": 2,
      "shop_name": "shop2",
      "description": "shop2 desc"
    },
    "products": [
      {
        "product_id": 6,
        "product_name": "p6",
        "price": 200,
        "description": "a product",
        "amount": 1
      }
    ],
    "date": 1619448651.712134,
    "price": 200
  },
  {
    id: 3,
    "username" : "Moshe",
    "shop": {
      "shop_id": 2,
      "shop_name": "shop2",
      "description": "shop2 desc"
    },
    "products": [
      {
        "product_id": 10,
        "product_name": "p10",
        "price": 96,
        "description": "a product",
        "amount": 1
      }
    ],
    "date": 1619448651.713111,
    "price": 96
  }
]

const pages = {
  userTransactions: {
    name: "User Transactions",
  },
  signIn: {
    name: "Sign In",
  },
  signUp: {
    name: "Sign Up",
  },
  mainPage: {
    name: "Main Page",
  },
}


export default function Blog() {
  const classes = useStyles();
  const [selected, setSelected] = useState(pages.userTransactions);
  const [searchQuery, setSearchQuery] = useState("");
  const setSelectedPage = (page) => {
    localStorage.setItem("page", page.name)
    setSelected(page)
  }
  function onSearchChange(event){
    // event.persist();
    console.log( event.target.value);
    setSearchQuery(event.target.value);
  }
  return (
      <ProvideAuth>
      <Router>
        <React.Fragment>
          <CssBaseline/>
          <Container maxWidth="lg" className={`site-layout-wrapper=modal-active`}>
            <Header title={selected.name} categories={categories} onSearchChange = {onSearchChange}/>
            <main>
              <Grid container justify="center" spacing={5} className={classes.mainGrid}>
                <Switch>
                  {/* Guest routes */}
                  <Route path="/register">
                    <Register />
                  </Route>
                  <Route path="/cart">
                    <Cart/>
                  </Route>
                  <Route path="/cart/:shop_id">
                    <ShoppingBag/> {/* This means shopping bag of shop shop_id*/}
                  </Route>
                  <Route path="/shops">
                    <Route path="/:shop_id">  {/* this means that in the shop component we can use UseParams()*/}
                      <Shop/>                 {/* to get the shop_id param and then get the proper shop info */}
                    </Route>
                    <Route path="/products">
                      <Route path="/:product_id">
                        <Product/>
                      </Route>
                    </Route>
                  </Route>
                  <Route path="/login" exact>
                    <SignIn />
                  </Route>
                  <Route path="/transactions">
                    <Transactions/>
                  </Route>
                  <Route path="/" exact>
                    <Main_page searchQuery = {searchQuery}/>
                  </Route>
                  <Route path="/system_transactions" exact>
                    <System_manager_transaction_history />
                  </Route>
                  }
                </Switch>
              </Grid>
            </main>
          </Container>
        </React.Fragment>
      </Router>
      </ProvideAuth>
  );
}
