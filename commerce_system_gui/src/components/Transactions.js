import {Transaction} from "./Transaction";
import {Typography} from "@material-ui/core";
import React, {useEffect, useState} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import {get_user_transactions} from "../api";
import {useAuth} from "./use-auth";
import {Link} from "react-router-dom";

const useStyles = makeStyles((theme) => ({
  mainFeaturedPost: {
    position: 'relative',
    // backgroundColor: theme.palette.grey[800],
    // color: theme.palette.common.white,
    marginBottom: theme.spacing(4),
    // backgroundImage: 'url(https://source.unsplash.com/random)',
    backgroundSize: 'cover',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
    width: "100%",
  },
  overlay: {
    position: 'absolute',
    top: 0,
    bottom: 0,
    right: 0,
    left: 0,
    // backgroundColor: 'rgba(0,0,0,.3)',
  },
  mainFeaturedPostContent: {
    position: 'relative',
    padding: theme.spacing(3),
    [theme.breakpoints.up('md')]: {
      padding: theme.spacing(6),
      paddingRight: 0,
    },
  },
}));

export default function Transactions() {
  const classes = useStyles();
  const [transactions, setTransactions] = useState([]);
  const auth = useAuth();

  useEffect(async () => {
    get_user_transactions(await auth.getToken())
        .then((res) => {
          setTransactions(res || [])
        })
        .catch((err) => setTransactions([]))
  }, [])

  return (
      <>
        <Grid item lg={6}>
          {(transactions && transactions.length > 0) ?
              transactions.map((transaction, index) => <Transaction key={index} transaction={transaction}/>)
              : <Typography align="center">You currently have no transactions, start shopping <Link to="/">here</Link></Typography>
          }
        </Grid></>
  );
}