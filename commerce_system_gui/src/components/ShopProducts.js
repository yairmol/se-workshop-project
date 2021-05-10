import {Fab, Paper, Typography} from "@material-ui/core";
import React, {useEffect, useState} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import {get_user_transactions, get_shop_transactions} from "../api";
import {Link} from "react-router-dom";
import AddIcon from '@material-ui/icons/Add';
import ShopProduct from "./ShopProduct";

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

export default function Products({products, remove_product_func, edit_product_func, permissions, add_product_func}) {
  const classes = useStyles();
  return (
      <>
        <Grid item lg={6} >
          <Typography className={classes.heading}>Products &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
                <Fab color="primary" onClick={() => add_product_func()}
                     aria-label="add" style={{ height:'15px', width:'35px' }} >
                  <AddIcon/>
                </Fab>
          </Typography>
          {(products && products.length > 0) ?
              products.map((product, index) => <div style={{width:'200%'}}>
                <ShopProduct
                    permissions={permissions}
                    edit_product_func={edit_product_func}
                    remove_product_func={remove_product_func}
                    key={index} product={product}/></div>)
              : <Paper><Typography className={classes.empty_msg} />Shop has no products</Paper>
          }
        </Grid></>
  );
}

