import {Input} from "@material-ui/core";
import React, {useEffect, useState} from "react";
import Button from "@material-ui/core/Button";
import ButtonBase from '@material-ui/core/ButtonBase';
import Typography from '@material-ui/core/Typography';

import {useAuth} from "./use-auth";
import {get_all_shops_info, get_user_transactions} from "../api";
import {Link} from "react-router-dom";

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    minWidth: 300,
    width: '100%',
  },
  shopImage: {
    position: 'relative',
    height: 200,
    [theme.breakpoints.down('xs')]: {
      width: '100% !important', // Overrides inline-style
      height: 100,
    },
    '&:hover, &$focusVisible': {
      zIndex: 1,
      '& $imageBackdrop': {
        opacity: 0.15,
      },
      '& $imageMarked': {
        opacity: 0,
      },
      '& $imageTitle': {
        border: '4px solid currentColor',
      },
    },
  },
  focusVisible: {},
  imageButton: {
    position: 'absolute',
    left: 0,
    right: 0,
    top: 0,
    bottom: 0,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: theme.palette.common.white,
  },
  imageSrc: {
    position: 'absolute',
    left: 0,
    right: 0,
    top: 0,
    bottom: 0,
    backgroundSize: 'cover',
    backgroundPosition: 'center 40%',
  },
  imageBackdrop: {
    position: 'absolute',
    left: 0,
    right: 0,
    top: 0,
    bottom: 0,
    backgroundColor: theme.palette.common.black,
    opacity: 0.4,
    transition: theme.transitions.create('opacity'),
  },
  imageTitle: {
    position: 'relative',
    padding: `${theme.spacing(2)}px ${theme.spacing(4)}px ${theme.spacing(1) + 6}px`,
  },
  imageMarked: {
    height: 3,
    width: 18,
    backgroundColor: theme.palette.common.white,
    position: 'absolute',
    bottom: -2,
    left: 'calc(50% - 9px)',
    transition: theme.transitions.create('opacity'),
  },
}));

export const Main_page = () => {
  const [shops, setShops] = useState([]);
  const auth = useAuth();

  useEffect(() => {
    get_all_shops_info(auth.token)
        .then((res) => {
          setShops(res.data || [])
        })
        .catch((err) => setShops([]))
  }, [])

  return (
      <div>
        <Grid item lg = {6}>
          {shops.length > 0 ? shops.map((shop, index) => <ButtonBases shops = shops />) :
           <Typography align="center">There ar no shops :( </Typography>}
        </Grid>
      </div>
  );
};
export default function ButtonBases(shops) {
  const classes = useStyles();
  const defaultImageUrl = "https://p1.hiclipart.com/preview/33/96/19/shopping-cart-red-line-material-property-logo-circle-vehicle-rectangle-png-clipart.jpg";
  return (
    <div className={classes.root}>
      {shops.map((shop) => (
        <ButtonBase
          focusRipple
          key={shop.shop_id}
          className={classes.shopImage}
          focusVisibleClassName={classes.focusVisible}
          style={{
            width: '30%',
          }}
        >
          <span
            className={classes.imageSrc}
            style={{
              backgroundImage: `url(${shop.shopImage === "" ? defaultImageUrl : shop.shopImage})`,
            }}
          />
          <span className={classes.imageBackdrop} />
          <span className={classes.imageButton}>
            <Typography
              component="span"
              variant="subtitle1"
              color="inherit"
              className={classes.imageTitle}
            >
              {shop.shop_name}
              <span className={classes.imageMarked} />
            </Typography>
          </span>
        </ButtonBase>
      ))}
    </div>
  );
}
