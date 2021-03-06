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

function Transactions({transactions_getter, width}) {
  const classes = useStyles();
  const [transactions, setTransactions] = useState([]);
  const auth = useAuth();

  useEffect(() => {
    auth.getToken().then((token) =>
      transactions_getter(token).then((res) => {
        setTransactions(res || [])
      }).catch((err) => setTransactions([])))
  }, [auth, transactions_getter])

  return (
    <Grid item xs={6}>
      <Typography className={classes.heading}>Transactions</Typography>
      {(transactions && transactions.length > 0) ?
        transactions.sort((t1, t2) => t1.date > t2.date ? -1 : t1.date === t2.date ? 0 : 1).map((transaction, index) =>
          <div style={{width: width}}><Transaction key={index} transaction={transaction}/></div>
        )
        :
        <Typography align="center">
          You currently have no transactions, start shopping <Link to={{pathname: "/", header: "Main"}}>
          here</Link>
        </Typography>
      }
    </Grid>
  );
}

export function UserTransactions() {
  return <Transactions transactions_getter={(token) => get_user_transactions(token)} widht="100%"/>
}

export function ShopTransactions({shop_id}) {
  return <Transactions transactions_getter={(token) => get_shop_transactions(token, shop_id)} width="200%"/>
}
