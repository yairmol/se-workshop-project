import React, {useState} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Container from '@material-ui/core/Container';
import Header from './components/Header'
import Transactions from "./components/Transactions";
import {Transaction} from "./components/Transaction";
import {Typography} from "@material-ui/core";
import SignIn from "./components/SignIn";

const useStyles = makeStyles((theme) => ({
  mainGrid: {
    marginTop: theme.spacing(3),
  },
}));

const categories = [
  {title: 'Technology', url: '#'},
  {title: 'Design', url: '#'},
  {title: 'Culture', url: '#'},
  {title: 'Business', url: '#'},
  {title: 'Politics', url: '#'},
  {title: 'Opinion', url: '#'},
  {title: 'Science', url: '#'},
  {title: 'Health', url: '#'},
  {title: 'Style', url: '#'},
  {title: 'Travel', url: '#'},
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
    "price": 2.5
  },
  {
    id: 2,
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
}


export default function Blog() {
  const classes = useStyles();
  const [selected, setSelected] = useState(pages.userTransactions);
  const [signedIn, setSignedIn] = useState(false);
  const [activeUsername, setActiveUsername] = useState(null);

  const onSignUp = () => {
    // TODO: add sign in logic here
    setSignedIn(!signedIn)
  }

  const onSignInClick = () => setSelected(pages.signIn);
  const onSignUpClick = () => setSelected(pages.signUp);
  
  const setLoggedIn = (username) => {
    setSignedIn(true);
    setActiveUsername(username);
  }

  return (
      <React.Fragment>
        <CssBaseline/>
        {/*<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"/>*/}
        <Container maxWidth="lg">
          <Header title={selected.name} categories={categories} signedIn={signedIn}
                  onSignInClick={onSignInClick} onSignUpClick={onSignUpClick}/>
          <main>
            <Grid container justify="center" spacing={5} className={classes.mainGrid}>
              {
                selected === pages.userTransactions ? <Transactions transactions={transactions}/> :
                selected === pages.signIn ? <SignIn onSignUpClick={onSignUpClick} setLoggedIn={setLoggedIn}/> :
                    //insert more options here
                    <Typography>oops</Typography>
              }
            </Grid>
          </main>
        </Container>
      </React.Fragment>
  );
}
