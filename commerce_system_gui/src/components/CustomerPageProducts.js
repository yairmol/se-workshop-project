import {Fab, Paper, Typography} from "@material-ui/core";
import React, {useEffect, useState} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import {get_user_transactions, get_shop_transactions} from "../api";
import {Link} from "react-router-dom";
import AddIcon from '@material-ui/icons/Add';
import ShopProduct from "./ShopProduct";
import Button from "@material-ui/core/Button";
import BuyProductPopup from "./PopUps/BuyProductPopup";

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
  secondaryHeading: {
        fontSize: theme.typography.pxToRem(15),
        color: theme.palette.text.secondary,
    },
  empty_msg: {
        fontSize: theme.typography.pxToRem(30),
        color: theme.palette.text.secondary,
        padding:50,
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
}))

export default function CustomerPageProducts({products, buy_product_popup}) {
  const classes = useStyles();

  return (
     <Grid>
        {products.map((product) => {
          return <Button onClick={() => {
                  buy_product_popup(product)
          }}>
                <Typography className={classes.heading}>{product.product_name}</Typography>
                <Typography className={classes.secondaryHeading}>{product.price}</Typography>
              </Button>
        })}
      </Grid>
  )
}

