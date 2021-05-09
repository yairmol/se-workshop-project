import {Transaction} from "./Transaction";
import {Typography} from "@material-ui/core";
import React, {useEffect, useState} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import {get_user_transactions, get_shop_transactions} from "../api";
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
  heading: {
      fontSize: theme.typography.pxToRem(20),
      flexBasis: '33.33%',
      flexShrink: 0,
      fontWeight: 530,
      padding: theme.spacing(1)
  },
}));

function Transactions(transactions_getter) {
  const classes = useStyles();
  const [transactions, setTransactions] = useState([]);
  const auth = useAuth();

  useEffect(() => {
    auth.getToken().then(transactions_getter)
        .then((res) => {
          setTransactions(res || [])
        })
        .catch((err) => setTransactions([]))
  }, [])

  return (
      <>
        <Grid item lg={6} >
          <Typography className={classes.heading}>Transactions</Typography>
          {(transactions && transactions.length > 0) ?
              transactions.map((transaction, index) => <div style={{width:'200%'}}><Transaction key={index} transaction={transaction}/></div>)
              : <Typography align="center">You currently have no transactions, start shopping <Link to="/">here</Link></Typography>
          }
        </Grid></>
  );
}

export function UserTransactions() {
  return Transactions((res) => get_user_transactions(res))
}

export function ShopTransactions({shop_id}) {
  return Transactions((res) => get_shop_transactions(res, shop_id))
}
