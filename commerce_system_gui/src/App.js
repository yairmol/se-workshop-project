import React, {useState} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Container from '@material-ui/core/Container';
import Header from './components/Header'
import Transactions from "./components/Transactions";
import {Transaction} from "./components/Transaction";
import {Typography} from "@material-ui/core";

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
  user_transactions: {
    name: "User Transactions",
  },
}


export default function Blog() {
  const classes = useStyles();
  const [selected, setSelected] = useState(pages.user_transactions);

  return (
      <React.Fragment>
        <CssBaseline/>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"/>
        <Container maxWidth="lg">
          <Header title={selected.name} categories={categories}/>
          <main>
            <Grid alignItems="center" container spacing={5} className={classes.mainGrid}>
              {
                selected === pages.user_transactions ? <Transactions transactions={transactions}/> :
                    //insert more options here
                    <Typography>oops</Typography>
              }
            </Grid>
          </main>
        </Container>
      </React.Fragment>
  );
}
