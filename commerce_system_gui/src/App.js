import React, {useState, useEffect, useLayoutEffect} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Container from '@material-ui/core/Container';
import Header from './components/Header';
import Transactions from "./components/Transactions";
import {Typography} from "@material-ui/core";
import SignIn from "./components/SignIn";
import {enter, logout} from "./api";

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
  const [user, setUser] = useState();

  const setSelectedPage = (page) => {
    localStorage.setItem("page", page.name)
    setSelected(page)
  }

  const onSignInClick = () => setSelectedPage(pages.signIn);
  const onSignUpClick = () => setSelectedPage(pages.signUp);

  useEffect(() => {
    // localStorage.clear();
    const userToken = localStorage.getItem("token");
    alert(userToken);
    if (!userToken){
      enter().then((token) => localStorage.setItem("token", token))
    }
    const loggedInUser = localStorage.getItem("user");
    if (loggedInUser) {
      setUser(loggedInUser);
    }
  }, []);

  useLayoutEffect(() => {
    const page = localStorage.getItem("page")
    if (page){
      for (const obj1 in pages) {
        if (pages[obj1].name === page) {
          setSelected(pages[obj1]);
        }
      }
    }
  })
  // logout the user
  const handleLogout = () => {
    logout(localStorage.getItem("token")).then((res) => {
      alert(JSON.stringify(res))
      if (res.status) {
        setUser(null);
        localStorage.removeItem('user');
        setSelectedPage(pages.signIn);
      }
    })
  };

  // login the user
  // const handleSubmit = async e => {
  //   e.preventDefault();
  //   const user = { username, password };
  //   // send the username and password to the server
  //   const response = await axios.post(
  //     "http://blogservice.herokuapp.com/api/login",
  //     user
  //   );
  //   // set the state of the user
  //   // store the user in localStorage
  //   localStorage.setItem("user", JSON.stringify(response.data));
  // };
  
  const setLoggedIn = (username) => {
    localStorage.setItem('user', username);
    setUser((username));
    setSelectedPage(pages.userTransactions);
  }

  return (
      <React.Fragment>
        <CssBaseline/>
        {/*<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"/>*/}
        <Container maxWidth="lg">
          <Header title={selected.name} categories={categories} signedIn={user}
                  onSignInClick={onSignInClick} onSignUpClick={onSignUpClick} onSignOut={handleLogout}/>
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
